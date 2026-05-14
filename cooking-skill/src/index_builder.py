import json
import re
import sys
import requests
from typing import Dict, List
from src.nutrition_calculator import NutritionCalculator

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Anduin2017/HowToCook/master"
GITHUB_API_BASE = "https://api.github.com/repos/Anduin2017/HowToCook/contents"

CATEGORY_MAP = {
    "vegetable_dish": "素菜",
    "meat_dish": "荤菜",
    "aquatic": "水产",
    "breakfast": "早餐",
    "staple": "主食",
    "semi-finished": "半成品",
    "soup": "汤粥",
    "drink": "饮料",
    "condiment": "酱料",
    "dessert": "甜品",
}

DIFFICULTY_TIME_MAP = {
    1: (5, 15),
    2: (15, 25),
    3: (25, 40),
    4: (40, 60),
    5: (60, 120),
}


TIPS_CATEGORIES = [
    "tips/learn",
    "tips/advanced",
]

TIPS_ROOT_FILES = [
    "tips/厨房准备.md",
    "tips/如何选择现在吃什么.md",
    "tips/食材相克与禁忌.md",
]

TIPS_CATEGORY_MAP = {
    "tips/learn": "烹饪技法",
    "tips/advanced": "高级技巧",
}


class IndexBuilder:
    def __init__(self, nutrition_db_path: str, aliases_path: str):
        self.calc = NutritionCalculator(nutrition_db_path)
        with open(aliases_path, 'r', encoding='utf-8') as f:
            self.aliases = json.load(f)

    def build(self, output_path: str):
        recipes = []
        for category in CATEGORY_MAP.keys():
            category_recipes = self._fetch_category(category)
            recipes.extend(category_recipes)
            print(f"  已获取 {category}: {len(category_recipes)} 道")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        print(f"\n已构建 {len(recipes)} 道菜谱索引 -> {output_path}")

    def build_tutorials(self, output_path: str):
        tutorials = []
        for file_path in TIPS_ROOT_FILES:
            tutorial = self._fetch_tips_file(file_path)
            if tutorial:
                tutorials.append(tutorial)
                print(f"  已获取 {file_path}")

        for category in TIPS_CATEGORIES:
            category_tutorials = self._fetch_tips_category(category)
            tutorials.extend(category_tutorials)
            print(f"  已获取 {category}: {len(category_tutorials)} 篇")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tutorials, f, ensure_ascii=False, indent=2)
        print(f"\n已构建 {len(tutorials)} 篇教程索引 -> {output_path}")

    def _fetch_category(self, category: str) -> List[Dict]:
        url = f"{GITHUB_API_BASE}/dishes/{category}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            items = resp.json()
        except Exception as e:
            print(f"获取分类 {category} 失败: {e}")
            return []

        recipes = []
        for item in items:
            if item.get("type") != "dir":
                continue
            recipe = self._fetch_recipe(category, item["name"])
            if recipe:
                recipes.append(recipe)
        return recipes

    def _fetch_recipe(self, category: str, dir_name: str) -> Dict:
        file_url = f"{GITHUB_RAW_BASE}/dishes/{category}/{dir_name}/{dir_name}.md"
        try:
            resp = requests.get(file_url, timeout=10)
            resp.raise_for_status()
            content = resp.text
        except Exception:
            alt_url = f"{GITHUB_RAW_BASE}/dishes/{category}/{dir_name}.md"
            try:
                resp = requests.get(alt_url, timeout=10)
                resp.raise_for_status()
                content = resp.text
            except Exception as e:
                sys.stdout.flush()
                return None

        sys.stdout.write(".")
        sys.stdout.flush()
        return self._parse_recipe(content, category, dir_name)

    def _parse_recipe(self, content: str, category: str, dir_name: str) -> Dict:
        name = dir_name.replace(".md", "")
        difficulty = self._extract_difficulty(content)
        ingredients = self._extract_ingredients(content)
        steps = self._extract_steps(content)
        nutrition = self.calc.calculate(ingredients)
        spiciness = self.calc.infer_spiciness(ingredients)
        cooking_method = self._detect_cooking_method(content)
        is_low_fat = self.calc.is_low_fat(ingredients, cooking_method)

        time_range = DIFFICULTY_TIME_MAP.get(difficulty, (10, 30))

        tags = []
        if difficulty <= 2:
            tags.append("快手")
        if is_low_fat:
            tags.append("低脂")
        if spiciness == 0:
            tags.append("清淡")
        elif spiciness >= 4:
            tags.append("重辣")

        return {
            "name": name,
            "category": category,
            "category_cn": CATEGORY_MAP.get(category, category),
            "difficulty": difficulty,
            "spiciness": spiciness,
            "nutrition": nutrition,
            "ingredients": ingredients,
            "steps": steps,
            "cooking_method": cooking_method,
            "cooking_time_min": time_range[0],
            "cooking_time_max": time_range[1],
            "tags": tags,
            "source_file": f"dishes/{category}/{dir_name}/{dir_name}.md",
        }

    def _extract_difficulty(self, content: str) -> int:
        match = re.search(r'难度[：:]\s*★{1,5}', content)
        if match:
            return match.group().count('★')
        match = re.search(r'([1-5])\s*星', content)
        if match:
            return int(match.group(1))
        return 2

    def _extract_ingredients(self, content: str) -> List[str]:
        in_ingredients = False
        ingredients = []
        for line in content.split('\n'):
            if '原料' in line or '食材' in line or '材料' in line:
                in_ingredients = True
                continue
            if in_ingredients:
                if line.startswith('##') or line.startswith('#'):
                    break
                match = re.match(r'\s*[*\-]\s*(.+)', line)
                if match:
                    ingredients.append(match.group(1).strip())
        return ingredients

    def _extract_steps(self, content: str) -> List[str]:
        in_steps = False
        steps = []
        for line in content.split('\n'):
            if line.startswith('##') and '操作' in line:
                in_steps = True
                continue
            if in_steps:
                if line.startswith('##'):
                    break
                match = re.match(r'\s*[-\d]+\.\s*(.+)', line)
                if not match:
                    match = re.match(r'\s*[-]\s*(.+)', line)
                if match:
                    steps.append(match.group(1).strip())
        return steps

    def _detect_cooking_method(self, content: str) -> str:
        methods = ["清蒸", "水煮", "白灼", "凉拌", "蒸", "煮", "炖", "红烧", "炒", "煎", "炸", "烤", "焖"]
        for method in methods:
            if method in content:
                return method
        return ""

    def _fetch_tips_file(self, file_path: str) -> Dict:
        url = f"{GITHUB_RAW_BASE}/{file_path}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            content = resp.text
        except Exception as e:
            print(f"获取教程 {file_path} 失败: {e}")
            return None

        return self._parse_tutorial(content, file_path)

    def _fetch_tips_category(self, category: str) -> List[Dict]:
        url = f"{GITHUB_API_BASE}/{category}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            items = resp.json()
        except Exception as e:
            print(f"获取教程分类 {category} 失败: {e}")
            return []

        tutorials = []
        for item in items:
            if item.get("type") != "file" or not item["name"].endswith(".md"):
                continue
            tutorial = self._fetch_tips_file(f"{category}/{item['name']}")
            if tutorial:
                tutorials.append(tutorial)
        return tutorials

    def _parse_tutorial(self, content: str, file_path: str) -> Dict:
        name = file_path.split("/")[-1].replace(".md", "")
        category = "基础指南"
        for prefix, cat in TIPS_CATEGORY_MAP.items():
            if file_path.startswith(prefix):
                category = cat
                break

        keywords = []
        for kw in ["焯水", "蒸", "煮", "炒", "煎", "炸", "烤", "炖", "凉拌", "腌", "高压锅", "空气炸锅", "微波炉", "去腥", "油温", "糖色", "辅料", "厨房准备", "食材相克"]:
            if kw in content or kw in name:
                keywords.append(kw)

        return {
            "name": name,
            "category": category,
            "keywords": keywords,
            "content": content,
            "source_file": file_path,
        }
