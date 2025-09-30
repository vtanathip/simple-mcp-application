"""
Test suite for the craft tool FastMCP application.
"""

import pytest
import json
from typing import Dict, List, Any
from craft_tool import (
    mcp,
    CRAFT_DATABASE,
    CRAFT_INSTRUCTIONS,
    CRAFT_TIPS,
    list_craft_items,
    get_craft_details,
    search_crafts_by_category,
    search_crafts_by_difficulty,
    get_random_craft,
    search_crafts_by_materials,
    estimate_craft_time,
    # Import the underlying functions for testing
    _list_craft_items,
    _get_craft_details,
    _search_crafts_by_category,
    _search_crafts_by_difficulty,
    _get_random_craft,
    _search_crafts_by_materials,
    _estimate_craft_time
)


class TestCraftToolBasics:
    """Test basic functionality of craft tool functions."""
    
    def test_list_craft_items(self):
        """Test that list_craft_items returns all available crafts."""
        result = _list_craft_items()
        
        assert isinstance(result, list)
        assert len(result) == len(CRAFT_DATABASE)
        
        # Check structure of returned items
        for item in result:
            assert "id" in item
            assert "name" in item
            assert "description" in item
            assert "difficulty" in item
            assert "time_required" in item
            assert "category" in item
        
        # Check that all database items are included
        item_ids = {item["id"] for item in result}
        expected_ids = set(CRAFT_DATABASE.keys())
        assert item_ids == expected_ids

    def test_get_craft_details_valid_item(self):
        """Test getting details for a valid craft item."""
        item_id = "paper_airplane"
        result = _get_craft_details(item_id)
        
        assert isinstance(result, dict)
        assert "item" in result
        assert "instructions" in result
        assert "tips" in result
        
        # Check item details structure
        item = result["item"]
        assert item["name"] == "Paper Airplane"
        assert item["difficulty"] == "easy"
        assert item["category"] == "paper_crafts"
        
        # Check instructions and tips are lists
        assert isinstance(result["instructions"], list)
        assert isinstance(result["tips"], list)
        assert len(result["instructions"]) > 0
        assert len(result["tips"]) > 0

    def test_get_craft_details_invalid_item(self):
        """Test getting details for an invalid craft item."""
        result = _get_craft_details("nonexistent_craft")
        
        assert isinstance(result, dict)
        assert "error" in result
        assert "not found" in result["error"]

    def test__search_crafts_by_category(self):
        """Test searching crafts by category."""
        # Test valid category
        result = _search_crafts_by_category("paper_crafts")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == "paper_airplane"
        
        # Test case insensitive search
        result_case_insensitive = _search_crafts_by_category("PAPER_CRAFTS")
        assert result == result_case_insensitive
        
        # Test non-existent category
        result_empty = _search_crafts_by_category("nonexistent")
        assert isinstance(result_empty, list)
        assert len(result_empty) == 0

    def test__search_crafts_by_difficulty(self):
        """Test searching crafts by difficulty level."""
        # Test easy difficulty
        result = _search_crafts_by_difficulty("easy")
        assert isinstance(result, list)
        assert len(result) == 2  # paper_airplane and painted_rock
        
        easy_ids = {item["id"] for item in result}
        assert "paper_airplane" in easy_ids
        assert "painted_rock" in easy_ids
        
        # Test medium difficulty
        result_medium = _search_crafts_by_difficulty("medium")
        assert len(result_medium) == 2  # origami_crane and friendship_bracelet
        
        # Test hard difficulty
        result_hard = _search_crafts_by_difficulty("hard")
        assert len(result_hard) == 1  # macrame_plant_hanger
        
        # Test invalid difficulty
        result_invalid = _search_crafts_by_difficulty("impossible")
        assert isinstance(result_invalid, dict)
        assert "error" in result_invalid

    def test_get_random_craft(self):
        """Test getting a random craft suggestion."""
        result = _get_random_craft()
        
        assert isinstance(result, dict)
        assert "item" in result
        assert "instructions" in result
        assert "tips" in result
        
        # Verify it's a valid craft from our database
        item_name = result["item"]["name"]
        valid_names = {item.name for item in CRAFT_DATABASE.values()}
        assert item_name in valid_names

    def test__search_crafts_by_materials(self):
        """Test searching crafts by available materials."""
        # Test with paper
        result = _search_crafts_by_materials(["paper"])
        assert isinstance(result, list)
        assert len(result) >= 2  # Should find paper airplane and origami crane
        
        found_names = {item["name"] for item in result}
        assert "Paper Airplane" in found_names
        assert "Origami Crane" in found_names
        
        # Test with thread
        result_thread = _search_crafts_by_materials(["thread"])
        thread_names = {item["name"] for item in result_thread}
        assert "Friendship Bracelet" in thread_names
        
        # Test with no matching materials
        result_empty = _search_crafts_by_materials(["unicorn_horn"])
        assert isinstance(result_empty, list)
        assert len(result_empty) == 0

    def test__estimate_craft_time(self):
        """Test time estimation for multiple crafts."""
        # Test with valid items
        result = _estimate_craft_time(["paper_airplane", "origami_crane"])
        
        assert isinstance(result, dict)
        assert "valid_items" in result
        assert "invalid_items" in result
        assert "estimated_total_minutes" in result
        assert "estimated_total_hours" in result
        
        assert len(result["valid_items"]) == 2
        assert len(result["invalid_items"]) == 0
        assert result["estimated_total_minutes"] > 0
        assert result["estimated_total_hours"] > 0
        
        # Test with invalid items
        result_invalid = _estimate_craft_time(["nonexistent_craft"])
        assert len(result_invalid["valid_items"]) == 0
        assert len(result_invalid["invalid_items"]) == 1
        assert result_invalid["estimated_total_minutes"] == 0

    def test_estimate_craft_time_mixed(self):
        """Test time estimation with mix of valid and invalid items."""
        result = _estimate_craft_time(["paper_airplane", "nonexistent", "origami_crane"])
        
        assert len(result["valid_items"]) == 2
        assert len(result["invalid_items"]) == 1
        assert "nonexistent" in result["invalid_items"]


class TestCraftToolDataIntegrity:
    """Test data integrity and consistency."""
    
    def test_database_consistency(self):
        """Test that all database entries have consistent structure."""
        for item_id, item in CRAFT_DATABASE.items():
            assert hasattr(item, 'name')
            assert hasattr(item, 'description')
            assert hasattr(item, 'materials')
            assert hasattr(item, 'difficulty')
            assert hasattr(item, 'time_required')
            assert hasattr(item, 'category')
            
            assert isinstance(item.materials, list)
            assert len(item.materials) > 0
            assert item.difficulty in ['easy', 'medium', 'hard']

    def test_instructions_coverage(self):
        """Test that all craft items have instructions."""
        for item_id in CRAFT_DATABASE.keys():
            assert item_id in CRAFT_INSTRUCTIONS
            instructions = CRAFT_INSTRUCTIONS[item_id]
            assert isinstance(instructions, list)
            assert len(instructions) > 0

    def test_tips_coverage(self):
        """Test that all craft items have tips."""
        for item_id in CRAFT_DATABASE.keys():
            assert item_id in CRAFT_TIPS
            tips = CRAFT_TIPS[item_id]
            assert isinstance(tips, list)
            assert len(tips) > 0


class TestCraftToolEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_materials_search(self):
        """Test searching with empty materials list."""
        result = _search_crafts_by_materials([])
        assert isinstance(result, list)
        assert len(result) == 0

    def test_case_insensitive_searches(self):
        """Test that searches are case insensitive where appropriate."""
        # Category search
        result1 = _search_crafts_by_category("origami")
        result2 = _search_crafts_by_category("ORIGAMI")
        result3 = _search_crafts_by_category("Origami")
        assert result1 == result2 == result3
        
        # Difficulty search
        result4 = _search_crafts_by_difficulty("easy")
        result5 = _search_crafts_by_difficulty("EASY")
        result6 = _search_crafts_by_difficulty("Easy")
        assert result4 == result5 == result6

    def test_multiple_runs_consistency(self):
        """Test that multiple calls return consistent results (except random)."""
        # Test list_craft_items consistency
        result1 = _list_craft_items()
        result2 = _list_craft_items()
        assert result1 == result2
        
        # Test get_craft_details consistency
        details1 = _get_craft_details("paper_airplane")
        details2 = _get_craft_details("paper_airplane")
        assert details1 == details2


class TestFastMCPIntegration:
    """Test FastMCP integration and server setup."""
    
    def test_mcp_server_exists(self):
        """Test that the MCP server is properly initialized."""
        assert mcp is not None
        assert hasattr(mcp, 'run')

    def test_tool_registration(self):
        """Test that tools are properly registered with MCP."""
        # Test the underlying functions are callable
        tools = [
            _list_craft_items,
            _get_craft_details,
            _search_crafts_by_category,
            _search_crafts_by_difficulty,
            _get_random_craft,
            _search_crafts_by_materials,
            _estimate_craft_time
        ]
        
        for tool in tools:
            assert callable(tool)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])