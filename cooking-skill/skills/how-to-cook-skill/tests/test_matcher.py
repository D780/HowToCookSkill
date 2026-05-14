import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.ingredient_matcher import IngredientMatcher


def test_alias_match():
    matcher = IngredientMatcher("data/ingredient_aliases.json")
    assert matcher.resolve_name("番茄") == "西红柿"
    assert matcher.resolve_name("马铃薯") == "土豆"
    assert matcher.resolve_name("未知食材") == "未知食材"


def test_find_recipes_by_ingredients():
    matcher = IngredientMatcher("data/ingredient_aliases.json")
    recipes = [
        {"name": "西红柿炒鸡蛋", "ingredients": ["西红柿", "鸡蛋"]},
        {"name": "土豆丝", "ingredients": ["土豆", "辣椒"]},
        {"name": "豆腐汤", "ingredients": ["豆腐", "葱"]},
    ]
    result = matcher.find_by_ingredients(["番茄", "蛋"], recipes)
    assert len(result) > 0
    assert result[0]["name"] == "西红柿炒鸡蛋"


def test_shopping_list():
    matcher = IngredientMatcher("data/ingredient_aliases.json")
    recipes = [
        {"name": "西红柿炒鸡蛋", "ingredients": ["西红柿", "鸡蛋", "盐"]},
    ]
    needed = matcher.get_shopping_list(recipes, have_ingredients=["盐"])
    assert "西红柿" in needed
    assert "鸡蛋" in needed
    assert "盐" not in needed


def test_normalize_ingredients():
    matcher = IngredientMatcher("data/ingredient_aliases.json")
    result = matcher.normalize_ingredients(["番茄", "马铃薯", "豆腐"])
    assert "西红柿" in result
    assert "土豆" in result
    assert "豆腐" in result
