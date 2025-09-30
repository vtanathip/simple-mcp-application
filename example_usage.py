#!/usr/bin/env python3
"""
Example usage of the craft tool FastMCP application.

This script demonstrates how to use the various craft tool functions
to discover, search, and learn about craft projects.
"""

from craft_tool import (
    _list_craft_items,
    _get_craft_details,
    _search_crafts_by_category,
    _search_crafts_by_difficulty,
    _get_random_craft,
    _search_crafts_by_materials,
    _estimate_craft_time
)
import json


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_json(data, indent=2):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=indent))


def main():
    """Demonstrate the craft tool functionality."""
    
    print("🎨 Welcome to the Craft Tool Demo!")
    print("This demo showcases the various features of our craft discovery tool.")
    
    # 1. List all available crafts
    print_section("1. All Available Crafts")
    all_crafts = _list_craft_items()
    print(f"Found {len(all_crafts)} craft projects:")
    for craft in all_crafts:
        print(f"  • {craft['name']} ({craft['difficulty']}) - {craft['time_required']}")
    
    # 2. Get detailed information about a specific craft
    print_section("2. Detailed Craft Information")
    details = _get_craft_details("paper_airplane")
    print("Paper Airplane Details:")
    print(f"  Name: {details['item']['name']}")
    print(f"  Description: {details['item']['description']}")
    print(f"  Materials: {', '.join(details['item']['materials'])}")
    print(f"  Difficulty: {details['item']['difficulty']}")
    print(f"  Time Required: {details['item']['time_required']}")
    print(f"  Category: {details['item']['category']}")
    print(f"\n  Instructions ({len(details['instructions'])} steps):")
    for i, step in enumerate(details['instructions'], 1):
        print(f"    {i}. {step}")
    print(f"\n  Tips ({len(details['tips'])} tips):")
    for tip in details['tips']:
        print(f"    • {tip}")
    
    # 3. Search by category
    print_section("3. Search by Category")
    origami_crafts = _search_crafts_by_category("origami")
    print(f"Origami crafts ({len(origami_crafts)} found):")
    for craft in origami_crafts:
        print(f"  • {craft['name']} - {craft['description']}")
    
    # 4. Search by difficulty
    print_section("4. Search by Difficulty")
    easy_crafts = _search_crafts_by_difficulty("easy")
    print(f"Easy crafts ({len(easy_crafts)} found):")
    for craft in easy_crafts:
        print(f"  • {craft['name']} ({craft['time_required']})")
    
    # 5. Search by available materials
    print_section("5. Search by Available Materials")
    available_materials = ["paper", "scissors"]
    matching_crafts = _search_crafts_by_materials(available_materials)
    print(f"Crafts you can make with {', '.join(available_materials)} ({len(matching_crafts)} found):")
    for craft in matching_crafts:
        print(f"  • {craft['name']}")
        print(f"    Materials needed: {', '.join(craft['materials_needed'])}")
        print(f"    Difficulty: {craft['difficulty']}")
    
    # 6. Get random craft suggestion
    print_section("6. Random Craft Suggestion")
    random_craft = _get_random_craft()
    print("Here's a random craft suggestion for you:")
    print(f"  🎯 {random_craft['item']['name']}")
    print(f"     {random_craft['item']['description']}")
    print(f"     Difficulty: {random_craft['item']['difficulty']}")
    print(f"     Time: {random_craft['item']['time_required']}")
    
    # 7. Estimate time for multiple crafts
    print_section("7. Time Estimation for Craft Session")
    selected_crafts = ["paper_airplane", "origami_crane", "friendship_bracelet"]
    time_estimate = _estimate_craft_time(selected_crafts)
    print(f"Planning a craft session with {len(selected_crafts)} projects:")
    for item in time_estimate['valid_items']:
        print(f"  • {item['name']}: {item['time']}")
    print(f"\n  📊 Total estimated time:")
    print(f"     Minutes: {time_estimate['estimated_total_minutes']}")
    print(f"     Hours: {time_estimate['estimated_total_hours']}")
    
    # 8. Error handling demonstration
    print_section("8. Error Handling")
    invalid_craft = _get_craft_details("unicorn_craft")
    print("Trying to get details for 'unicorn_craft':")
    if "error" in invalid_craft:
        print(f"  ❌ {invalid_craft['error']}")
    
    invalid_difficulty = _search_crafts_by_difficulty("impossible")
    print("\nTrying to search with invalid difficulty 'impossible':")
    if "error" in invalid_difficulty:
        print(f"  ❌ {invalid_difficulty['error']}")
    
    print_section("Demo Complete!")
    print("This concludes the demonstration of the craft tool features.")
    print("You can now use these functions in your LLM applications!")
    print("\n🚀 To start the MCP server, run: python craft_tool.py")
    print("📖 For development mode, run: fastmcp dev craft_tool.py")


if __name__ == "__main__":
    main()