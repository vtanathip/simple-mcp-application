"""
LangChain MCP Integration with mcp-use and Ollama

This script demonstrates how to create a craft assistant using mcp-use
to connect to our MCP craft server with LangChain and Ollama.

Prerequisites:
- Install dependencies: uv add mcp-use langchain-ollama
- Have Ollama running with a suitable model (e.g., llama3.1)
- Ensure craft_tool.py MCP server can be started

This example shows proper MCP client integration using the mcp-use library.
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any

try:
    from mcp_use import MCPAgent, MCPClient
except ImportError:
    print("Error: mcp-use package not found. Install it with: uv add mcp-use")
    exit(1)

try:
    from langchain_ollama import ChatOllama
except ImportError:
    print("Error: langchain-ollama package not found. Install it with: uv add langchain-ollama")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CraftAssistant:
    """AI Assistant that uses MCP craft tools via mcp-use with LangChain and Ollama."""

    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialize the craft assistant.

        Args:
            model_name: Name of the Ollama model to use
        """
        self.model_name = model_name
        self.client = None
        self.agent = None

    async def setup(self) -> bool:
        """
        Set up the MCP client and agent.

        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            logger.info("Setting up MCP client and agent...")

            # Create MCP server configuration for our craft tool
            config = {
                "mcpServers": {
                    "craft": {
                        "command": "uv",
                        "args": ["run", "python", "craft_tool.py"]
                    }
                }
            }

            # Create MCP client
            self.client = MCPClient.from_dict(config)

            # Create LLM
            llm = ChatOllama(model=self.model_name, temperature=0.3)

            # Create agent with the client
            self.agent = MCPAgent(
                llm=llm,
                client=self.client,
                max_steps=10,
                verbose=True
            )

            logger.info("Successfully set up MCP agent with craft tools")
            return True

        except Exception as e:
            logger.error(f"Setup failed: {e}")
            print(f"\nSetup Error: {e}")
            print("Make sure:")
            print("1. Ollama is running with the specified model")
            print(
                f"2. Model {self.model_name} is installed (try: ollama pull {self.model_name})")
            print("3. craft_tool.py can be executed")
            return False

    async def chat(self, user_input: str) -> str:
        """
        Process user input and return AI response using MCP tools.

        Args:
            user_input: User's question or request

        Returns:
            str: AI assistant's response
        """
        if not self.agent:
            return "Error: Assistant not properly initialized. Please run setup() first."

        try:
            logger.info(f"Processing query: {user_input}")

            # Run the agent with the user input
            result = await self.agent.run(user_input)

            return result

        except Exception as e:
            logger.error(f"Chat processing failed: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    async def cleanup(self):
        """Clean up resources."""
        if self.client:
            try:
                await self.client.close_all_sessions()
            except Exception as e:
                logger.error(f"Cleanup error: {e}")

    async def interactive_session(self):
        """Run an interactive chat session with the craft assistant."""
        print("\n🎨 Welcome to the MCP Craft Assistant! 🎨")
        print("I can help you discover crafts, find projects by materials, difficulty, and more!")
        print("Type 'quit', 'exit', or 'bye' to end the session.\n")

        try:
            while True:
                try:
                    user_input = input("You: ").strip()

                    if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                        print("\n👋 Happy crafting! Goodbye!")
                        break

                    if not user_input:
                        continue

                    print("🤔 Assistant is thinking...")
                    response = await self.chat(user_input)
                    print(f"\n🎨 Assistant: {response}\n")

                except KeyboardInterrupt:
                    print("\n\n👋 Session interrupted. Goodbye!")
                    break
                except Exception as e:
                    print(f"\nError: {e}")
                    continue
        finally:
            await self.cleanup()


async def demo_queries():
    """Demonstrate various craft assistant capabilities with sample queries."""

    assistant = CraftAssistant()

    if not await assistant.setup():
        return

    # Sample queries to demonstrate capabilities
    demo_questions = [
        "List all available craft items",
        "What crafts can I make with paper?",
        "Show me easy crafts for beginners",
        "Give me details about making a paper airplane",
        "Suggest a random craft project",
        "What crafts can I do in 30 minutes or less?",
        "How do I make an origami crane?"
    ]

    print("\n🎨 MCP Craft Assistant Demo 🎨")
    print("=" * 50)

    try:
        for i, question in enumerate(demo_questions, 1):
            print(f"\n{i}. Question: {question}")
            print("-" * 40)

            try:
                response = await assistant.chat(question)
                print(f"Answer: {response}")

            except Exception as e:
                print(f"Error: {e}")

            # Small delay between questions
            await asyncio.sleep(1)

        print("\n" + "=" * 50)
        print("Demo completed! Try the interactive session for more exploration.")

    finally:
        await assistant.cleanup()


async def main():
    """Main function to run the craft assistant."""

    print("LangChain MCP Craft Assistant")
    print("============================")
    print("Using mcp-use with Ollama")

    # Choose mode
    print("\nChoose mode:")
    print("1. Interactive chat session")
    print("2. Demo with sample queries")

    try:
        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice == "1":
            assistant = CraftAssistant()
            if await assistant.setup():
                await assistant.interactive_session()

        elif choice == "2":
            await demo_queries()

        else:
            print("Invalid choice. Please run again and select 1 or 2.")

    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
