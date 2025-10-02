"""
A simple craft tool for LLM using FastMCP library.

This module provides craft-related tools and utilities for language model interactions.
"""

from fastmcp import FastMCP
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import random
import logging
import sys
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('craft_tool_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Log server startup
logger.info("Starting Craft Tool Server initialization...")

try:
    # Initialize FastMCP server
    mcp = FastMCP("Craft Tool Server")
    logger.info("FastMCP server initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize FastMCP server: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)


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
    try:
        logger.debug("Listing all craft items")
        result = [
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
        logger.info(f"Successfully listed {len(result)} craft items")
        return result
    except Exception as e:
        logger.error(f"Error listing craft items: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Failed to list craft items: {str(e)}"}


def _get_craft_details(item_id: str) -> Dict:
    """Get detailed information about a specific craft item.

    Args:
        item_id: The ID of the craft item to retrieve details for
    """
    try:
        logger.debug(f"Getting craft details for item_id: {item_id}")

        if not item_id:
            logger.warning("Empty item_id provided to get_craft_details")
            return {"error": "Item ID cannot be empty"}

        if item_id not in CRAFT_DATABASE:
            logger.warning(
                f"Craft item '{item_id}' not found in database. Available items: {list(CRAFT_DATABASE.keys())}")
            return {"error": f"Craft item '{item_id}' not found"}

        item = CRAFT_DATABASE[item_id]
        result = {
            "item": item.model_dump(),
            "instructions": CRAFT_INSTRUCTIONS.get(item_id, []),
            "tips": CRAFT_TIPS.get(item_id, [])
        }
        logger.info(f"Successfully retrieved craft details for '{item_id}'")
        return result
    except Exception as e:
        logger.error(f"Error getting craft details for '{item_id}': {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Failed to get craft details: {str(e)}"}


def _search_crafts_by_category(category: str) -> List[Dict]:
    """Search for craft items by category.

    Args:
        category: The category to search for (e.g., 'paper_crafts', 'origami', 'jewelry')
    """
    try:
        logger.debug(f"Searching crafts by category: {category}")

        if not category:
            logger.warning(
                "Empty category provided to search_crafts_by_category")
            return {"error": "Category cannot be empty"}

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

        logger.info(f"Found {len(results)} crafts in category '{category}'")
        if len(results) == 0:
            available_categories = list(
                set(item.category for item in CRAFT_DATABASE.values()))
            logger.info(f"Available categories: {available_categories}")

        return results
    except Exception as e:
        logger.error(f"Error searching crafts by category '{category}': {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Failed to search by category: {str(e)}"}


def _search_crafts_by_difficulty(difficulty: str) -> List[Dict]:
    """Search for craft items by difficulty level.

    Args:
        difficulty: The difficulty level ('easy', 'medium', 'hard')
    """
    try:
        logger.debug(f"Searching crafts by difficulty: {difficulty}")

        if not difficulty:
            logger.warning(
                "Empty difficulty provided to search_crafts_by_difficulty")
            return {"error": "Difficulty cannot be empty"}

        if difficulty.lower() not in ['easy', 'medium', 'hard']:
            logger.warning(
                f"Invalid difficulty level '{difficulty}'. Valid levels: easy, medium, hard")
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

        logger.info(
            f"Found {len(results)} crafts with difficulty '{difficulty}'")
        return results
    except Exception as e:
        logger.error(
            f"Error searching crafts by difficulty '{difficulty}': {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Failed to search by difficulty: {str(e)}"}


def _get_random_craft() -> Dict:
    """Get a random craft suggestion for inspiration."""
    try:
        logger.debug("Getting random craft suggestion")

        if not CRAFT_DATABASE:
            logger.error("CRAFT_DATABASE is empty, cannot get random craft")
            return {"error": "No crafts available in database"}

        item_id = random.choice(list(CRAFT_DATABASE.keys()))
        logger.info(f"Selected random craft: {item_id}")
        return _get_craft_details(item_id)
    except Exception as e:
        logger.error(f"Error getting random craft: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Failed to get random craft: {str(e)}"}


def _search_crafts_by_materials(materials: List[str]) -> List[Dict]:
    """Find crafts that can be made with available materials.

    Args:
        materials: List of materials you have available
    """
    try:
        logger.debug(f"Searching crafts by materials: {materials}")

        if not materials or len(materials) == 0:
            logger.warning(
                "Empty materials list provided to search_crafts_by_materials")
            return []

        results = []
        materials_lower = [m.lower().strip() for m in materials if m.strip()]

        if not materials_lower:
            logger.warning("No valid materials found after processing")
            return []

        for item_id, item in CRAFT_DATABASE.items():
            # Check if any of the craft materials match the available materials
            item_materials_lower = [m.lower().strip() for m in item.materials]
            if any(available in item_mat for available in materials_lower for item_mat in item_materials_lower):
                results.append({
                    "id": item_id,
                    "name": item.name,
                    "description": item.description,
                    "materials_needed": item.materials,
                    "difficulty": item.difficulty,
                    "time_required": item.time_required
                })

        logger.info(
            f"Found {len(results)} crafts matching available materials")
        return results
    except Exception as e:
        logger.error(f"Error searching crafts by materials {materials}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []


def _estimate_craft_time(item_ids: List[str]) -> Dict:
    """Estimate total time needed for multiple crafts.

    Args:
        item_ids: List of craft item IDs to estimate time for
    """
    try:
        logger.debug(f"Estimating craft time for items: {item_ids}")

        if not item_ids or len(item_ids) == 0:
            logger.warning(
                "Empty item_ids list provided to estimate_craft_time")
            return {"error": "Item IDs list cannot be empty"}

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
                try:
                    if "minute" in time_str:
                        # Extract numbers from time string
                        import re
                        numbers = re.findall(r'\d+', time_str)
                        if numbers:
                            # Take first number as minutes
                            total_time += int(numbers[0])
                    elif "hour" in time_str:
                        numbers = re.findall(r'\d+', time_str)
                        if numbers:
                            # Convert hours to minutes
                            total_time += int(numbers[0]) * 60
                except Exception as parse_error:
                    logger.warning(
                        f"Failed to parse time for {item_id}: {parse_error}")
            else:
                invalid_items.append(item_id)
                logger.warning(
                    f"Invalid item_id '{item_id}' in time estimation")

        result = {
            "valid_items": valid_items,
            "invalid_items": invalid_items,
            "estimated_total_minutes": total_time,
            "estimated_total_hours": round(total_time / 60, 2)
        }

        logger.info(
            f"Time estimation complete: {len(valid_items)} valid, {len(invalid_items)} invalid items")
        return result
    except Exception as e:
        logger.error(f"Error estimating craft time for {item_ids}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Failed to estimate craft time: {str(e)}"}

# MCP tool wrappers


@mcp.tool()
def list_craft_items() -> List[Dict]:
    """List all available craft items with their basic information."""
    logger.info("MCP tool called: list_craft_items")
    return _list_craft_items()


@mcp.tool()
def get_craft_details(item_id: str) -> Dict:
    """Get detailed information about a specific craft item.

    Args:
        item_id: The ID of the craft item to retrieve details for
    """
    logger.info(f"MCP tool called: get_craft_details with item_id='{item_id}'")
    return _get_craft_details(item_id)


@mcp.tool()
def search_crafts_by_category(category: str) -> List[Dict]:
    """Search for craft items by category.

    Args:
        category: The category to search for (e.g., 'paper_crafts', 'origami', 'jewelry')
    """
    logger.info(
        f"MCP tool called: search_crafts_by_category with category='{category}'")
    return _search_crafts_by_category(category)


@mcp.tool()
def search_crafts_by_difficulty(difficulty: str) -> List[Dict]:
    """Search for craft items by difficulty level.

    Args:
        difficulty: The difficulty level ('easy', 'medium', 'hard')
    """
    logger.info(
        f"MCP tool called: search_crafts_by_difficulty with difficulty='{difficulty}'")
    return _search_crafts_by_difficulty(difficulty)


@mcp.tool()
def get_random_craft() -> Dict:
    """Get a random craft suggestion for inspiration."""
    logger.info("MCP tool called: get_random_craft")
    return _get_random_craft()


@mcp.tool()
def search_crafts_by_materials(materials: List[str]) -> List[Dict]:
    """Find crafts that can be made with available materials.

    Args:
        materials: List of materials you have available
    """
    logger.info(
        f"MCP tool called: search_crafts_by_materials with materials={materials}")
    return _search_crafts_by_materials(materials)


@mcp.tool()
def estimate_craft_time(item_ids: List[str]) -> Dict:
    """Estimate total time needed for multiple crafts.

    Args:
        item_ids: List of craft item IDs to estimate time for
    """
    logger.info(
        f"MCP tool called: estimate_craft_time with item_ids={item_ids}")
    return _estimate_craft_time(item_ids)


if __name__ == "__main__":
    try:
        logger.info("Starting MCP server...")
        logger.info(f"Server start time: {datetime.now()}")
        logger.info("MCP tools registered successfully")

        # Log available craft data for debugging
        logger.info(f"Craft database loaded with {len(CRAFT_DATABASE)} items")
        logger.info(
            f"Available craft categories: {list(set(item.category for item in CRAFT_DATABASE.values()))}")

        # Run the MCP server
        logger.info("Running MCP server with stdio transport...")
        # Using stdio for simplicity in this example
        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Fatal error starting MCP server: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        logger.error(
            "ROOT CAUSE: Server failed to start - check FastMCP installation and transport configuration")
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")
