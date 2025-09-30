"""
A simple craft tool for LLM using FastMCP library.

This module provides craft-related tools and utilities for language model interactions.
"""

from fastmcp import FastMCP
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import random

# Initialize FastMCP server
mcp = FastMCP("Craft Tool Server")

class CraftItem(BaseModel):
    """Represents a craft item with its properties."""
    name: str
    description: str
    materials: List[str]
    difficulty: str  # "easy", "medium", "hard"
    time_required: str
    category: str

class CraftRecipe(BaseModel):
    """Represents a complete crafting recipe."""
    item: CraftItem
    instructions: List[str]
    tips: List[str]

# Sample craft data
CRAFT_DATABASE = {
    "paper_airplane": CraftItem(
        name="Paper Airplane",
        description="A simple flying paper craft perfect for beginners",
        materials=["A4 paper", "steady hands"],
        difficulty="easy",
        time_required="5 minutes",
        category="paper_crafts"
    ),
    "origami_crane": CraftItem(
        name="Origami Crane",
        description="Traditional Japanese paper folding creating an elegant crane",
        materials=["Square origami paper"],
        difficulty="medium",
        time_required="15-20 minutes",
        category="origami"
    ),
    "friendship_bracelet": CraftItem(
        name="Friendship Bracelet",
        description="Colorful woven bracelet made with embroidery thread",
        materials=["Embroidery thread (3-4 colors)", "scissors", "tape"],
        difficulty="medium",
        time_required="30-45 minutes",
        category="jewelry"
    ),
    "painted_rock": CraftItem(
        name="Painted Rock",
        description="Decorative rock painted with creative designs",
        materials=["Smooth rock", "acrylic paints", "paintbrushes", "sealant"],
        difficulty="easy",
        time_required="1-2 hours (including drying time)",
        category="painting"
    ),
    "macrame_plant_hanger": CraftItem(
        name="Macrame Plant Hanger",
        description="Elegant plant hanger made with knotted cord",
        materials=["Macrame cord", "metal ring", "scissors", "measuring tape"],
        difficulty="hard",
        time_required="2-3 hours",
        category="home_decor"
    )
}

CRAFT_INSTRUCTIONS = {
    "paper_airplane": [
        "Take an 8.5 x 11 inch piece of paper",
        "Fold the paper in half lengthwise, then unfold",
        "Fold the top corners down to the center crease",
        "Fold the angled edges down to the center crease again",
        "Fold the plane in half along the center crease",
        "Create wings by folding each side down to align with the bottom",
        "Your paper airplane is ready to fly!"
    ],
    "origami_crane": [
        "Start with a square piece of paper, colored side down",
        "Fold diagonally both ways and unfold",
        "Fold horizontally and vertically, then unfold",
        "Bring the three corners down to the bottom corner using creases as guides",
        "Fold the top flaps into the center, repeat on back",
        "Fold the top triangle down, repeat on back",
        "Pull the sides apart gently and flatten to create a diamond",
        "Fold the top points down to create the head and tail",
        "Pull the wings apart gently while holding the body"
    ],
    "friendship_bracelet": [
        "Cut 4 strands of thread, each about 24 inches long",
        "Tie all strands together with a knot, leaving 2 inches of tail",
        "Tape the knot to a flat surface",
        "Separate strands into pairs (A, B, C, D from left to right)",
        "Take strand A over and under strand B, then pull tight",
        "Repeat the knot with strand A over strand B",
        "Move to strand C, repeat the double knot process",
        "Continue pattern until bracelet is desired length",
        "Tie off with a secure knot"
    ],
    "painted_rock": [
        "Find a smooth, clean rock",
        "Wash and dry the rock thoroughly",
        "Apply a base coat of paint if desired, let dry",
        "Sketch your design lightly with pencil",
        "Paint your design with acrylic paints",
        "Allow each color to dry before adding details",
        "Apply a clear sealant to protect the paint",
        "Let dry completely before handling"
    ],
    "macrame_plant_hanger": [
        "Cut 8 cords, each 3 feet long",
        "Fold all cords in half and attach to metal ring with lark's head knots",
        "Measure 6 inches down and tie square knots with groups of 4 cords",
        "Measure 4 inches down and tie another round of square knots",
        "Separate each group of 4 into 2 groups of 2",
        "Take 2 cords from adjacent groups and tie together 4 inches down",
        "Repeat around to create the basket shape",
        "Measure 8 inches down and tie all cords together with a large knot",
        "Trim excess cord to desired length"
    ]
}

CRAFT_TIPS = {
    "paper_airplane": [
        "Use crisp folds for better flight performance",
        "Make sure both wings are even for straight flight",
        "Throw with a firm, level motion"
    ],
    "origami_crane": [
        "Use proper origami paper for best results",
        "Make sharp, precise creases",
        "Be patient - it takes practice to master"
    ],
    "friendship_bracelet": [
        "Keep tension consistent for even knots",
        "Use a clipboard to hold your work steady",
        "Choose colors that complement each other"
    ],
    "painted_rock": [
        "Prime the rock with white paint for brighter colors",
        "Use small brushes for detailed work",
        "Work in thin layers to avoid paint drips"
    ],
    "macrame_plant_hanger": [
        "Keep cord lengths consistent",
        "Practice basic macrame knots before starting",
        "Choose a pot that fits snugly in the hanger"
    ]
}

# Core functions (not decorated for direct testing)
def _list_craft_items() -> List[Dict]:
    """List all available craft items with their basic information."""
    return [
        {
            "id": item_id,
            "name": item.name,
            "description": item.description,
            "difficulty": item.difficulty,
            "time_required": item.time_required,
            "category": item.category
        }
        for item_id, item in CRAFT_DATABASE.items()
    ]

def _get_craft_details(item_id: str) -> Dict:
    """Get detailed information about a specific craft item.
    
    Args:
        item_id: The ID of the craft item to retrieve details for
    """
    if item_id not in CRAFT_DATABASE:
        return {"error": f"Craft item '{item_id}' not found"}
    
    item = CRAFT_DATABASE[item_id]
    return {
        "item": item.model_dump(),
        "instructions": CRAFT_INSTRUCTIONS.get(item_id, []),
        "tips": CRAFT_TIPS.get(item_id, [])
    }

def _search_crafts_by_category(category: str) -> List[Dict]:
    """Search for craft items by category.
    
    Args:
        category: The category to search for (e.g., 'paper_crafts', 'origami', 'jewelry')
    """
    results = []
    for item_id, item in CRAFT_DATABASE.items():
        if item.category.lower() == category.lower():
            results.append({
                "id": item_id,
                "name": item.name,
                "description": item.description,
                "difficulty": item.difficulty,
                "time_required": item.time_required
            })
    return results

def _search_crafts_by_difficulty(difficulty: str) -> List[Dict]:
    """Search for craft items by difficulty level.
    
    Args:
        difficulty: The difficulty level ('easy', 'medium', 'hard')
    """
    if difficulty.lower() not in ['easy', 'medium', 'hard']:
        return {"error": "Difficulty must be 'easy', 'medium', or 'hard'"}
    
    results = []
    for item_id, item in CRAFT_DATABASE.items():
        if item.difficulty.lower() == difficulty.lower():
            results.append({
                "id": item_id,
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "time_required": item.time_required
            })
    return results

def _get_random_craft() -> Dict:
    """Get a random craft suggestion for inspiration."""
    item_id = random.choice(list(CRAFT_DATABASE.keys()))
    return _get_craft_details(item_id)

def _search_crafts_by_materials(materials: List[str]) -> List[Dict]:
    """Find crafts that can be made with available materials.
    
    Args:
        materials: List of materials you have available
    """
    results = []
    materials_lower = [m.lower() for m in materials]
    
    for item_id, item in CRAFT_DATABASE.items():
        # Check if any of the craft materials match the available materials
        item_materials_lower = [m.lower() for m in item.materials]
        if any(available in item_mat for available in materials_lower for item_mat in item_materials_lower):
            results.append({
                "id": item_id,
                "name": item.name,
                "description": item.description,
                "materials_needed": item.materials,
                "difficulty": item.difficulty,
                "time_required": item.time_required
            })
    
    return results

def _estimate_craft_time(item_ids: List[str]) -> Dict:
    """Estimate total time needed for multiple crafts.
    
    Args:
        item_ids: List of craft item IDs to estimate time for
    """
    total_time = 0
    valid_items = []
    invalid_items = []
    
    for item_id in item_ids:
        if item_id in CRAFT_DATABASE:
            item = CRAFT_DATABASE[item_id]
            valid_items.append({
                "id": item_id,
                "name": item.name,
                "time": item.time_required
            })
            # Simple time parsing (this is a basic implementation)
            time_str = item.time_required.lower()
            if "minute" in time_str:
                # Extract numbers from time string
                import re
                numbers = re.findall(r'\d+', time_str)
                if numbers:
                    total_time += int(numbers[0])  # Take first number as minutes
            elif "hour" in time_str:
                numbers = re.findall(r'\d+', time_str)
                if numbers:
                    total_time += int(numbers[0]) * 60  # Convert hours to minutes
        else:
            invalid_items.append(item_id)
    
    return {
        "valid_items": valid_items,
        "invalid_items": invalid_items,
        "estimated_total_minutes": total_time,
        "estimated_total_hours": round(total_time / 60, 2)
    }

# MCP tool wrappers
@mcp.tool()
def list_craft_items() -> List[Dict]:
    """List all available craft items with their basic information."""
    return _list_craft_items()

@mcp.tool()
def get_craft_details(item_id: str) -> Dict:
    """Get detailed information about a specific craft item.
    
    Args:
        item_id: The ID of the craft item to retrieve details for
    """
    return _get_craft_details(item_id)

@mcp.tool()
def search_crafts_by_category(category: str) -> List[Dict]:
    """Search for craft items by category.
    
    Args:
        category: The category to search for (e.g., 'paper_crafts', 'origami', 'jewelry')
    """
    return _search_crafts_by_category(category)

@mcp.tool()
def search_crafts_by_difficulty(difficulty: str) -> List[Dict]:
    """Search for craft items by difficulty level.
    
    Args:
        difficulty: The difficulty level ('easy', 'medium', 'hard')
    """
    return _search_crafts_by_difficulty(difficulty)

@mcp.tool()
def get_random_craft() -> Dict:
    """Get a random craft suggestion for inspiration."""
    return _get_random_craft()

@mcp.tool()
def search_crafts_by_materials(materials: List[str]) -> List[Dict]:
    """Find crafts that can be made with available materials.
    
    Args:
        materials: List of materials you have available
    """
    return _search_crafts_by_materials(materials)

@mcp.tool()
def estimate_craft_time(item_ids: List[str]) -> Dict:
    """Estimate total time needed for multiple crafts.
    
    Args:
        item_ids: List of craft item IDs to estimate time for
    """
    return _estimate_craft_time(item_ids)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()