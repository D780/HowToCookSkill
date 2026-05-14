import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.nutrition_calculator import NutritionCalculator


def test_calculate_nutrition():
    calc = NutritionCalculator('data/nutrition_db.json')
    result = calc.calculate(["西红柿 180g", "鸡蛋 90g", "食用油 20g"])
    assert result["calories"] > 0
    assert result["protein"] > 0
    assert result["carbs"] >= 0
    assert result["fat"] >= 0


def test_spiciness_none():
    calc = NutritionCalculator('data/nutrition_db.json')
    assert calc.infer_spiciness(["西红柿", "鸡蛋", "豆腐"]) == 0


def test_spiciness_low():
    calc = NutritionCalculator('data/nutrition_db.json')
    assert calc.infer_spiciness(["青椒", "肉丝"]) == 2


def test_spiciness_medium():
    calc = NutritionCalculator('data/nutrition_db.json')
    assert calc.infer_spiciness(["干辣椒", "鸡丁"]) == 3


def test_spiciness_high():
    calc = NutritionCalculator('data/nutrition_db.json')
    assert calc.infer_spiciness(["小米辣", "牛肉"]) >= 4


def test_missing_ingredient():
    calc = NutritionCalculator('data/nutrition_db.json')
    result = calc.calculate(["未知食材 100g"])
    assert result["calories"] == 0


def test_low_fat_true():
    calc = NutritionCalculator('data/nutrition_db.json')
    assert calc.is_low_fat(["鱼", "豆腐"], "清蒸") is True


def test_low_fat_false():
    calc = NutritionCalculator('data/nutrition_db.json')
    assert calc.is_low_fat(["五花肉", "辣椒"], "炸") is False
