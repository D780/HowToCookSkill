import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.recommender import Recommender


def get_sample_recipes():
    return [
        {"name": "宫保鸡丁", "category": "meat_dish", "category_cn": "荤菜", "difficulty": 2, "spiciness": 3, "nutrition": {"calories": 380, "protein": 28, "carbs": 15, "fat": 22}, "ingredients": ["鸡胸肉", "花生", "干辣椒"], "cooking_time_min": 20, "cooking_time_max": 25, "tags": ["快手", "麻辣"], "steps": ["切丁", "炒制"]},
        {"name": "清炒花菜", "category": "vegetable_dish", "category_cn": "素菜", "difficulty": 1, "spiciness": 0, "nutrition": {"calories": 85, "protein": 3, "carbs": 12, "fat": 4}, "ingredients": ["花菜"], "cooking_time_min": 8, "cooking_time_max": 15, "tags": ["清淡", "快手"], "steps": ["切块", "翻炒"]},
        {"name": "紫菜蛋花汤", "category": "soup", "category_cn": "汤粥", "difficulty": 1, "spiciness": 0, "nutrition": {"calories": 60, "protein": 5, "carbs": 6, "fat": 2}, "ingredients": ["紫菜", "鸡蛋"], "cooking_time_min": 10, "cooking_time_max": 15, "tags": ["清淡", "快手"], "steps": ["烧水", "打蛋"]},
    ]


def test_recommend_by_people():
    rec = Recommender(get_sample_recipes())
    result = rec.recommend(people=2)
    assert len(result) >= 2


def test_recommend_low_fat():
    rec = Recommender(get_sample_recipes())
    result = rec.recommend(diet_mode="low_fat")
    assert len(result) > 0


def test_recommend_no_spicy():
    rec = Recommender(get_sample_recipes())
    result = rec.recommend(max_spiciness=0)
    for r in result:
        assert r["spiciness"] == 0


def test_menu_card_format():
    rec = Recommender(get_sample_recipes())
    result = rec.recommend(people=2)
    card = rec.generate_menu_card(result, people=2)
    assert "人份" in card
    assert "卡路里" in card


def test_recipe_detail_format():
    rec = Recommender(get_sample_recipes())
    recipe = get_sample_recipes()[0]
    detail = rec.generate_recipe_detail(recipe, servings=2)
    assert "宫保鸡丁" in detail
    assert "食材" in detail
    assert "步骤" in detail


def test_shopping_list():
    rec = Recommender(get_sample_recipes())
    recipes = rec.recommend(people=2)
    shopping = rec.generate_shopping_list(recipes, have=["盐"])
    assert "购物清单" in shopping


def test_workday_scene_filter():
    rec = Recommender(get_sample_recipes())
    result = rec.recommend(scene="workday")
    for r in result:
        assert r["difficulty"] <= 2
