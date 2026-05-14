import json
import re
from typing import Dict, List, Tuple


class NutritionCalculator:
    SPICY_KEYWORDS = {
        5: ["变态辣", "魔鬼辣", "死神辣"],
        4: ["麻辣", "小米辣", "泡椒", "剁椒", "特辣"],
        3: ["干辣椒", "辣子", "辣椒酱", "辣油", "中辣"],
        2: ["青椒", "红椒", "辣椒", "小辣", "微辣"],
        1: ["可选辣", "胡椒粉", "胡椒"],
    }

    LOW_FAT_TAGS = ["清蒸", "水煮", "白灼", "凉拌", "蒸", "煮", "炖"]
    HIGH_FAT_INGREDIENTS = ["五花肉", "油炸", "黄油", "肥肉", "培根", "肥牛"]

    def __init__(self, nutrition_db_path: str):
        with open(nutrition_db_path, 'r', encoding='utf-8') as f:
            self.nutrition_db = json.load(f)

    def calculate(self, ingredients: List[str]) -> Dict:
        total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
        for item in ingredients:
            name, grams = self._parse_ingredient(item)
            nutrition = self._lookup_nutrition(name)
            factor = grams / 100.0
            for key in total:
                total[key] += nutrition.get(key, 0) * factor
        return {k: round(v, 1) for k, v in total.items()}

    def infer_spiciness(self, ingredients: List[str]) -> int:
        all_text = " ".join(ingredients)
        for level in [5, 4, 3, 2, 1]:
            for keyword in self.SPICY_KEYWORDS[level]:
                if keyword in all_text:
                    return level
        return 0

    def is_low_fat(self, ingredients: List[str], cooking_method: str = "") -> bool:
        all_text = " ".join(ingredients) + " " + cooking_method
        for ing in self.HIGH_FAT_INGREDIENTS:
            if ing in all_text:
                return False
        for method in self.LOW_FAT_TAGS:
            if method in all_text:
                return True
        return False

    def _parse_ingredient(self, ingredient: str) -> Tuple[str, float]:
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:g|克|ml|毫升)', ingredient)
        if match:
            grams = float(match.group(1))
            name = re.sub(r'\d+(?:\.\d+)?\s*(?:g|克|ml|毫升)', '', ingredient).strip()
        else:
            grams = 100.0
            name = ingredient.strip()
        return name, grams

    def _lookup_nutrition(self, name: str) -> Dict:
        if name in self.nutrition_db:
            return self.nutrition_db[name]
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
