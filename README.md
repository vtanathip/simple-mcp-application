# Simple MCP Craft Tool Application

A comprehensive craft tool for Language Learning Models (LLMs) built using the [FastMCP](https://gofastmcp.com) library. This application provides a set of tools to help users discover, learn about, and plan craft projects.

## Features

- **Craft Discovery**: Browse available craft projects with detailed information
- **Search by Category**: Find crafts by category (paper_crafts, origami, jewelry, etc.)
- **Search by Difficulty**: Filter crafts by difficulty level (easy, medium, hard)
- **Material-based Search**: Find crafts you can make with available materials
- **Detailed Instructions**: Get step-by-step instructions for each craft
- **Expert Tips**: Access helpful tips for better crafting results
- **Time Estimation**: Calculate time needed for multiple craft projects
- **Random Suggestions**: Get inspiration with random craft recommendations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/vtanathip/simple-mcp-application.git
cd simple-mcp-application
```

2. Install dependencies using uv:
```bash
uv sync
```

Or install manually:
```bash
uv add fastmcp pydantic
uv add --dev pytest
```

## Usage

### Running the MCP Server

To start the FastMCP server:
```bash
python craft_tool.py
```

### Development Mode

For development with the MCP Inspector:
```bash
fastmcp dev craft_tool.py
```

### Inspect Available Tools

To see all available tools:
```bash
fastmcp inspect craft_tool.py
```

## Available Tools

The craft tool provides the following MCP tools:

1. **`list_craft_items()`** - List all available craft items
2. **`get_craft_details(item_id)`** - Get detailed information about a specific craft
3. **`search_crafts_by_category(category)`** - Search crafts by category
4. **`search_crafts_by_difficulty(difficulty)`** - Filter crafts by difficulty level
5. **`search_crafts_by_materials(materials)`** - Find crafts based on available materials
6. **`get_random_craft()`** - Get a random craft suggestion
7. **`estimate_craft_time(item_ids)`** - Calculate time needed for multiple crafts

## Available Crafts

The application includes the following craft projects:

- **Paper Airplane** (Easy, 5 minutes) - Simple flying paper craft
- **Origami Crane** (Medium, 15-20 minutes) - Traditional Japanese paper folding
- **Friendship Bracelet** (Medium, 30-45 minutes) - Colorful woven bracelet
- **Painted Rock** (Easy, 1-2 hours) - Decorative painted stone art
- **Macrame Plant Hanger** (Hard, 2-3 hours) - Elegant knotted plant holder

## Example Usage

```python
# List all available crafts
crafts = list_craft_items()

# Get details for a specific craft
details = get_craft_details("paper_airplane")

# Find easy crafts
easy_crafts = search_crafts_by_difficulty("easy")

# Find crafts you can make with paper
paper_crafts = search_crafts_by_materials(["paper"])

# Get a random craft suggestion
random_craft = get_random_craft()

# Estimate time for multiple crafts
time_estimate = estimate_craft_time(["paper_airplane", "origami_crane"])
```

## Integration with LangChain Ollama

This MCP server can be integrated with LangChain and Ollama to provide AI models with craft tool capabilities. Here's how to set up and use the integration:

### Prerequisites

First, install the required dependencies using `uv`:

```bash
# Install mcp-use library and LangChain Ollama
uv add mcp-use langchain-ollama
```

### Quick Start with Example File

We've included a working example at `langchain_mcp_example.py` that demonstrates proper MCP integration using mcp-use with LangChain and Ollama:

```bash
# 1. Make sure Ollama is running with a suitable model
ollama pull llama3.2

# 2. Install required dependencies
uv add mcp-use langchain-ollama

# 3. Run the example
uv run python langchain_mcp_example.py
```

The example provides both an interactive chat mode and a demo mode with sample queries.

**Features**:

- ✅ **Proper MCP Integration**: Uses `mcp-use` library for authentic MCP client communication
- ✅ **LangChain + Ollama**: Integrates with LangChain and Ollama for flexible LLM usage  
- ✅ **Tool Calling**: AI automatically uses appropriate craft tools based on queries
- ✅ **Async Support**: Full async/await support for better performance

### Setting Up the MCP Client with mcp-use

Create a Python script to connect to your MCP server using mcp-use:

```python
import asyncio
from mcp_use import MCPAgent, MCPClient
from langchain_ollama import ChatOllama

async def main():
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
    client = MCPClient.from_dict(config)
    
    # Create LLM
    llm = ChatOllama(model="llama3.1", temperature=0.3)
    
    # Create agent with the client
    agent = MCPAgent(
        llm=llm, 
        client=client, 
        max_steps=10,
        verbose=True
    )
    
    try:
        # Run a query - the AI will automatically use craft tools
        result = await agent.run("I have some paper and 20 minutes. What craft can I make?")
        print("AI Response:", result)
        
    finally:
        # Clean up resources
        await client.close_all_sessions()

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Usage with Streaming

Here's a more comprehensive example showing streaming responses:

```python
import asyncio
from mcp_use import MCPAgent, MCPClient
from langchain_ollama import ChatOllama

async def craft_assistant_with_streaming():
    """Create a craft assistant with streaming responses."""
    
    # Set up MCP configuration
    config = {
        "mcpServers": {
            "craft": {
                "command": "uv",
                "args": ["run", "python", "craft_tool.py"]
            }
        }
    }
    
    client = MCPClient.from_dict(config)
    llm = ChatOllama(model="llama3.1", temperature=0.3)
    
    agent = MCPAgent(
        llm=llm, 
        client=client, 
        max_steps=10,
        verbose=True
    )
    
    try:
        query = """
        I'm looking for craft projects. Can you help me find:
        1. All available crafts
        2. Easy crafts suitable for beginners  
        3. Something I can make with just paper
        """
        
        print("🤔 Processing your request...")
        print("-" * 50)
        
        # Stream the response
        async for chunk in agent.stream(query):
            if "messages" in chunk:
                print(chunk["messages"], end="", flush=True)
        
        print("\n" + "-" * 50)
        print("✅ Response completed!")
        
    finally:
        await client.close_all_sessions()

# Run the craft assistant
if __name__ == "__main__":
    asyncio.run(craft_assistant_with_streaming())
```

### Configuration Tips

1. **Server Startup**: Ensure your MCP server is properly configured to start. You can test this by running:

   ```bash
   uv run python craft_tool.py
   ```

2. **Model Selection**: Choose an Ollama model that supports function calling well. Recommended models:
   - `llama3.1` (8B or larger)
   - `mistral`
   - `codellama`

3. **Error Handling**: Add proper error handling for network issues and tool execution failures:

```python
import logging
from mcp_use import MCPAgent, MCPClient
from langchain_ollama import ChatOllama

async def robust_mcp_interaction():
    client = None
    try:
        config = {
            "mcpServers": {
                "craft": {
                    "command": "uv",
                    "args": ["run", "python", "craft_tool.py"]
                }
            }
        }
        
        client = MCPClient.from_dict(config)
        llm = ChatOllama(model="llama3.1")
        
        agent = MCPAgent(llm=llm, client=client, max_steps=10)
        
        result = await agent.run("What crafts are available?")
        print(f"Success: {result}")
        
    except Exception as e:
        logging.error(f"MCP integration error: {e}")
        print("Failed to connect to MCP server. Make sure craft_tool.py can be executed.")
    
    finally:
        if client:
            await client.close_all_sessions()
```

### Example Queries

Once integrated, you can ask the AI assistant natural language questions like:

- "What crafts can I make with paper and scissors?"
- "Show me all easy crafts that take less than 30 minutes"
- "I want to learn origami. What do you recommend?"
- "Give me step-by-step instructions for making a friendship bracelet"
- "What materials do I need for a painted rock project?"

The AI will automatically use the appropriate MCP tools to search, filter, and retrieve craft information to answer your questions.

## Integration with LangGraph

This MCP server can also be integrated with LangGraph for advanced conversational AI applications with state management and complex workflow orchestration.

### Prerequisites for LangGraph Integration

Install the additional LangGraph dependencies:

```bash
uv add langgraph langchain-core langchain-ollama mcp-use
```

### LangGraph Example Usage

We've included a working LangGraph example at `langgraph_mcp_simple.py` that demonstrates:

- **State Management**: Persistent conversation context across multiple interactions
- **Advanced Workflow**: Multi-step craft planning and consultation
- **Streaming Support**: Real-time response streaming for better user experience
- **Error Recovery**: Robust error handling and graceful degradation

```bash
# 1. Ensure Ollama is running with a suitable model
ollama pull llama3.2

# 2. Run the LangGraph example
uv run python langgraph_mcp_simple.py
```

The example provides both demo scenarios and an interactive chat mode.

### LangGraph Features

**State Persistence**: Conversations maintain context across multiple turns:

```python
# Example conversation flow
Human: "I'm new to crafting. What can I make?"
Assistant: [Uses MCP tools to list beginner-friendly crafts]
Human: "I have paper and scissors available"  
Assistant: [Remembers context, searches by materials]
Human: "Perfect! Give me instructions for the paper airplane"
Assistant: [Provides detailed step-by-step instructions]
```

**Advanced Planning Scenarios**:

**Multi-Project Planning Session**:
```
Human: I want to plan a 3-hour crafting session for this weekend
Agent: [Discovers available time and materials]
Human: I have paper, paint, and thread available
Agent: [Suggests compatible projects and estimates timing]
Human: That sounds perfect! Can you create a step-by-step plan?
Agent: [Provides detailed timeline and material preparation steps]
```

**Progressive Skill Development**:
```
Human: I've mastered paper airplanes, what's next?
Agent: [Analyzes skill progression and suggests origami crane]
Human: How difficult is the origami crane compared to what I know?
Agent: [Provides detailed comparison and learning pathway]
```

### LangGraph Architecture

The LangGraph integration uses a simple but powerful architecture:

```python
# Core components
class ConversationState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

class LangGraphCraftAgent:
    def __init__(self):
        self.mcp_agent = None  # mcp-use MCPAgent
        self.graph_app = None  # LangGraph compiled workflow
        
    async def _conversation_node(self, state):
        # Process messages through MCP agent
        response = await self.mcp_agent.run(user_message)
        return {"messages": [AIMessage(content=response)]}
```

**Key Benefits**:

- ✅ **Conversation Memory**: Maintains context across interactions
- ✅ **Tool Integration**: Seamlessly uses all FastMCP craft tools
- ✅ **Streaming Responses**: Real-time token streaming for better UX
- ✅ **Error Handling**: Graceful fallback when tools fail
- ✅ **Extensible**: Easy to add new nodes and conversation flows

### Advanced LangGraph Customization

For more complex workflows, you can extend the conversation graph:

```python
# Add specialized nodes for different conversation phases
workflow.add_node("discovery", discovery_node)      # Craft exploration
workflow.add_node("planning", planning_node)        # Project planning  
workflow.add_node("instruction", instruction_node)  # Step-by-step guidance
workflow.add_node("troubleshoot", troubleshoot_node) # Problem solving

# Define conversation flow
workflow.add_conditional_edges(
    "discovery",
    route_conversation,
    {
        "planning": "planning",
        "instruction": "instruction", 
        "end": END
    }
)
```

This allows for sophisticated conversation flows that adapt based on user needs and conversation context.

## Testing

## Advanced Integration with LangGraph + FastMCP HTTP Transport

For more sophisticated conversational AI with state management and streaming capabilities, we provide a LangGraph integration that communicates with FastMCP over HTTP transport. This enables advanced features like multi-step planning, conversation state persistence, and real-time streaming responses.

### Prerequisites for LangGraph Integration

```bash
# Install additional dependencies
uv add langgraph httpx aiohttp

# Ensure Ollama is running with a suitable model
ollama serve

# Start FastMCP server with HTTP transport (if not using the default stdio transport)
python craft_tool.py  # Default FastMCP server
```

### Quick Start with LangGraph Example

We've included a comprehensive LangGraph example at `langgraph_mcp_example.py`:

```bash
# Run the advanced LangGraph example
uv run python langgraph_mcp_example.py
```

**LangGraph Integration Features**:

- 🧠 **State Management**: Persistent conversation state across multiple interactions
- 🔄 **Multi-Step Planning**: Guides users through discovery → selection → planning → execution
- 📡 **HTTP Streaming**: Real-time streaming responses with FastMCP HTTP transport
- 💾 **Session Persistence**: Maintains context and progress across conversations
- 🎯 **Smart Stage Detection**: Automatically progresses conversation through crafting stages
- 🛠️ **Advanced Error Handling**: Robust error recovery and resource cleanup

### LangGraph Architecture Overview

The LangGraph integration uses a state machine approach:

1. **Discovery Stage**: Help users explore available crafts and preferences
2. **Selection Stage**: Narrow down choices based on materials, time, and skill
3. **Planning Stage**: Provide detailed instructions and material lists
4. **Execution Stage**: Offer tips and troubleshooting during crafting

```python
from langgraph_mcp_example import CraftPlanningAgent

# Initialize the advanced agent
agent = CraftPlanningAgent(model_name="llama3.2")
await agent.initialize()

# Start interactive session with state persistence
interface = CraftPlanningInterface(agent)
await interface.interactive_session()
```

### HTTP Transport Configuration

The LangGraph example communicates with FastMCP via HTTP transport:

```python
# FastMCP HTTP Client configuration
client = FastMCPHTTPClient("http://localhost:8000")

# Tool calling over HTTP with streaming support
response = await client.call_tool("list_craft_items", {})

# Streaming tool calls (if supported by server)
async for chunk in client.stream_tool_call("get_craft_details", {"item_id": "origami_crane"}):
    print(chunk)
```

### Advanced Usage Examples

**Multi-Project Planning Session**:
```
Human: I want to plan a 3-hour crafting session for this weekend
Agent: [Discovers available time and materials]
Human: I have paper, paint, and thread available
Agent: [Suggests compatible projects and estimates timing]
Human: That sounds perfect! Can you create a step-by-step plan?
Agent: [Provides detailed timeline and material preparation steps]
```

**Progressive Skill Development**:
```
Human: I've mastered paper airplanes, what's next?
Agent: [Analyzes skill progression and suggests origami crane]
Human: How difficult is the origami crane compared to what I know?
Agent: [Provides detailed comparison and learning pathway]
```

### Configuration Options

**LangGraph State Configuration**:
```python
# Custom state tracking
state = {
    "available_materials": ["paper", "scissors", "paint"],
    "time_budget": "2 hours",
    "difficulty_preference": "medium",
    "planning_stage": "discovery"
}
```

**Streaming Callback Setup**:
```python
def streaming_callback(token):
    print(token, end="", flush=True)

response, state = await agent.chat_stream(
    "What can I make?", 
    thread_id="session_123",
    streaming_callback=streaming_callback
)
```

### Error Handling and Recovery

The LangGraph integration includes comprehensive error handling:

```python
try:
    # Initialize with automatic retry logic
    if not await agent.initialize():
        print("Initialization failed - check server status")
        
    # Robust conversation handling
    response, state = await agent.chat_stream(message, thread_id)
    
except Exception as e:
    logger.error(f"Session error: {e}")
    # State is preserved for recovery
    
finally:
    # Automatic resource cleanup
    await agent.cleanup()
```

### Performance and Scalability

- **Async/Await**: Fully asynchronous for high concurrency
- **Connection Pooling**: Efficient HTTP connection reuse
- **State Checkpointing**: Persistent conversation state management
- **Streaming Responses**: Real-time user feedback
- **Resource Management**: Automatic cleanup and connection handling

This LangGraph integration demonstrates production-ready patterns for building sophisticated conversational AI applications with MCP tool integration.

## Testing

Run the comprehensive test suite:

```bash
uv run pytest test_craft_tool.py -v
```

The test suite includes:

- Basic functionality tests
- Data integrity tests
- Edge case handling
- FastMCP integration tests

## Project Structure

```text
simple-mcp-application/
├── craft_tool.py              # Main FastMCP server implementation
├── langchain_mcp_example.py   # LangChain integration example
├── test_craft_tool.py         # Comprehensive test suite
├── pyproject.toml            # Project configuration and dependencies
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## FastMCP

This project uses [FastMCP](https://gofastmcp.com) - the fast, Pythonic way to build MCP servers and clients. FastMCP provides:

- Easy-to-use decorators for tool creation
- Built-in development tools and inspector
- Comprehensive MCP protocol support
- Production-ready server implementation

For more information, visit [https://gofastmcp.com](https://gofastmcp.com).
