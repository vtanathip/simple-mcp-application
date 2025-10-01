"""
Simple LangGraph with FastMCP Integration

This example demonstrates a basic LangGraph agent that uses FastMCP tools
via the mcp-use library for proper MCP protocol integration.

Features:
- Simple LangGraph conversation flow
- FastMCP integration via mcp-use
- Interactive chat with craft tools
- Streaming responses

Prerequisites:
- uv add langgraph langchain-core langchain-ollama mcp-use
- Ollama running with llama3.2 model
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, TypedDict, Annotated

try:
    from langgraph.graph import StateGraph, START, END
    from langgraph.graph.message import add_messages
    from langgraph.prebuilt import ToolNode, tools_condition
    from langgraph.checkpoint.memory import MemorySaver
except ImportError:
    print("❌ langgraph not found. Install with: uv add langgraph")
    exit(1)

try:
    from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
    from langchain_core.callbacks import BaseCallbackHandler
except ImportError:
    print("❌ langchain-core not found. Install with: uv add langchain-core")
    exit(1)

try:
    from langchain_ollama import ChatOllama
except ImportError:
    print("❌ langchain-ollama not found. Install with: uv add langchain-ollama")
    exit(1)

try:
    from mcp_use import MCPAgent, MCPClient
except ImportError:
    print("❌ mcp-use not found. Install with: uv add mcp-use")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConversationState(TypedDict):
    """Simple conversation state for LangGraph."""
    messages: Annotated[List[BaseMessage], add_messages]


class StreamingHandler(BaseCallbackHandler):
    """Handler for streaming LLM tokens."""

    def __init__(self):
        self.stream_callback = None

    def set_callback(self, callback):
        self.stream_callback = callback

    def on_llm_new_token(self, token: str, **kwargs):
        if self.stream_callback:
            self.stream_callback(token)


class LangGraphCraftAgent:
    """LangGraph agent with FastMCP craft tools."""

    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.mcp_agent = None
        self.llm = None
        self.graph_app = None
        self.checkpointer = MemorySaver()
        self.streaming_handler = StreamingHandler()

    async def initialize(self) -> bool:
        """Initialize the agent with MCP integration."""
        try:
            logger.info("Initializing LangGraph Craft Agent...")

            # Set up MCP configuration for FastMCP craft server
            mcp_config = {
                "mcpServers": {
                    "craft": {
                        "command": "uv",
                        "args": ["run", "python", "craft_tool.py"]
                    }
                }
            }

            # Create MCP client and agent
            mcp_client = MCPClient.from_dict(mcp_config)

            # Initialize LLM with streaming support
            self.llm = ChatOllama(
                model=self.model_name,
                temperature=0.3,
                callbacks=[self.streaming_handler]
            )

            # Create MCP agent
            self.mcp_agent = MCPAgent(
                llm=self.llm,
                client=mcp_client,
                max_steps=10,
                verbose=True
            )

            # Build LangGraph
            await self._build_graph()

            logger.info("✅ LangGraph Craft Agent initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize agent: {e}")
            return False

    async def _build_graph(self):
        """Build the LangGraph conversation flow."""

        # Create state graph
        workflow = StateGraph(ConversationState)

        # Add conversation node
        workflow.add_node("conversation", self._conversation_node)

        # Add edges
        workflow.add_edge(START, "conversation")
        workflow.add_edge("conversation", END)

        # Compile with memory
        self.graph_app = workflow.compile(checkpointer=self.checkpointer)

        logger.info("LangGraph workflow compiled")

    async def _conversation_node(self, state: ConversationState):
        """Main conversation node that uses MCP agent."""

        # Get the latest human message
        human_messages = [msg for msg in state["messages"]
                          if isinstance(msg, HumanMessage)]
        if not human_messages:
            return {"messages": []}

        latest_message = human_messages[-1].content

        # Use MCP agent to process the message
        try:
            if self.mcp_agent is None:
                raise RuntimeError("MCP agent not initialized")

            # Ensure message is a string
            message_text = str(latest_message) if not isinstance(
                latest_message, str) else latest_message

            response = await self.mcp_agent.run(message_text)
            return {"messages": [AIMessage(content=str(response))]}
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            return {"messages": [AIMessage(content=error_msg)]}

    async def chat(self, message: str, thread_id: str = "default", stream_callback=None):
        """
        Process a chat message with optional streaming.

        Args:
            message: User's message
            thread_id: Thread ID for conversation persistence
            stream_callback: Optional callback for streaming tokens

        Returns:
            AI response
        """

        if stream_callback:
            self.streaming_handler.set_callback(stream_callback)

        if not self.graph_app:
            return "Agent not initialized"

        config = {"configurable": {"thread_id": thread_id}}

        # Process through LangGraph
        try:
            result = await self.graph_app.ainvoke(
                {"messages": [HumanMessage(content=message)]},
                config  # type: ignore
            )

            # Extract AI response
            ai_messages = [msg for msg in result["messages"]
                           if isinstance(msg, AIMessage)]
            if ai_messages:
                return ai_messages[-1].content
            else:
                return "No response generated"

        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Error processing message: {str(e)}"

    async def cleanup(self):
        """Clean up resources."""
        if self.mcp_agent and hasattr(self.mcp_agent, 'client') and self.mcp_agent.client:
            try:
                await self.mcp_agent.client.close_all_sessions()
            except Exception as e:
                logger.error(f"Cleanup error: {e}")


class InteractiveCraftChat:
    """Interactive chat interface for the craft agent."""

    def __init__(self, agent: LangGraphCraftAgent):
        self.agent = agent

    async def run(self):
        """Run the interactive chat session."""

        print("\n🎨 LangGraph + FastMCP Craft Assistant 🎨")
        print("=" * 50)
        print("Advanced conversation flow with craft planning capabilities")
        print("\nAvailable features:")
        print("• Multi-turn conversations with memory")
        print("• Craft discovery and planning")
        print("• Detailed instructions and tips")
        print("• Material-based recommendations")
        print("\nType 'quit' to exit\n")

        thread_id = f"session_{asyncio.get_event_loop().time()}"

        try:
            while True:
                user_input = input("You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Happy crafting!")
                    break

                if not user_input:
                    continue

                print("🤖 Assistant: ", end="", flush=True)

                # Stream the response
                def stream_token(token):
                    print(token, end="", flush=True)

                response = await self.agent.chat(
                    user_input,
                    thread_id=thread_id,
                    stream_callback=stream_token
                )

                print("\n")  # New line after response

        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            await self.agent.cleanup()


async def demo_scenarios():
    """Run demonstration scenarios."""

    agent = LangGraphCraftAgent()

    if not await agent.initialize():
        print("❌ Failed to initialize agent")
        return

    print("\n🎨 LangGraph + FastMCP Demo Scenarios 🎨")
    print("=" * 50)

    scenarios = [
        "Hi! I'm new to crafting. What can I make?",
        "I have paper and scissors. What projects are possible?",
        "Show me something easy that takes less than 30 minutes",
        "Can you give me step-by-step instructions for a paper airplane?"
    ]

    try:
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n[Scenario {i}] Human: {scenario}")
            print(f"[Scenario {i}] Assistant: ", end="", flush=True)

            def demo_stream(token):
                print(token, end="", flush=True)

            response = await agent.chat(
                scenario,
                thread_id=f"demo_{i}",
                stream_callback=demo_stream
            )

            print()  # New line
            await asyncio.sleep(1)  # Pause between scenarios

    except Exception as e:
        print(f"Demo error: {e}")
    finally:
        await agent.cleanup()


async def main():
    """Main function."""

    print("LangGraph + FastMCP Craft Assistant")
    print("===================================")

    print("\nChoose mode:")
    print("1. Interactive chat session")
    print("2. Demo scenarios")
    print("3. Both (demo then interactive)")

    try:
        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            agent = LangGraphCraftAgent()
            if await agent.initialize():
                chat = InteractiveCraftChat(agent)
                await chat.run()

        elif choice == "2":
            await demo_scenarios()

        elif choice == "3":
            await demo_scenarios()
            print("\n" + "=" * 50)
            print("Starting interactive session...")
            agent = LangGraphCraftAgent()
            if await agent.initialize():
                chat = InteractiveCraftChat(agent)
                await chat.run()

        else:
            print("Invalid choice")

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
