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

```
simple-mcp-application/
├── craft_tool.py          # Main FastMCP server implementation
├── test_craft_tool.py     # Comprehensive test suite
├── pyproject.toml         # Project configuration and dependencies
├── README.md             # This file
└── LICENSE               # MIT License
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
