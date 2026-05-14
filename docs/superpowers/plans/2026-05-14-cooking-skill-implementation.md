# 智能烹饪技能实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 HowToCook 构建智能菜谱推荐技能，支持语义化询问、营养估算、食材反推、定时同步

**架构:** Python 3 模块化设计，数据层（JSON）+ 业务层（索引构建/营养计算/推荐引擎）+ 交互层（CLI 入口）

**技术栈:** Python 3, requests, json

---

## 文件结构总览

```
cooking-skill/
├── data/
│   ├── recipes_index.json         # 菜谱索引（自动生成）
│   ├── nutrition_db.json          # 食材营养数据库（手动维护）
│   ├── ingredient_aliases.json    # 食材别名映射（手动维护）
│   └── user_preferences.json      # 用户口味偏好（运行时生成）
├── src/
│   ├── __init__.py
│   ├── index_builder.py           # 菜谱索引构建器
│   ├── recipe_sync.py             # 菜谱同步服务
│   ├── nutrition_calculator.py    # 营养估算工具
│   ├── ingredient_matcher.py      # 食材匹配引擎
│   └── recommender.py             # 推荐引擎
├── chef_skill.py                  # 技能交互入口
├── tests/
│   ├── test_nutrition.py
│   ├── test_matcher.py
│   └── test_recommender.py
├── README.md
└── requirements.txt
```

---

### Task 1: 项目基础结构 + 营养数据库

**目标:** 创建项目目录、依赖文件、营养数据库、食材别名文件

**Files:**
- Create: `/workspace/cooking-skill/requirements.txt`
- Create: `/workspace/cooking-skill/data/nutrition_db.json`
- Create: `/workspace/cooking-skill/data/ingredient_aliases.json`
- Create: `/workspace/cooking-skill/data/user_preferences.json`
- Create: `/workspace/cooking-skill/src/__init__.py`

- [ ] **Step 1: 创建 requirements.txt**

```
requests>=2.28.0
```

- [ ] **Step 2: 创建 nutrition_db.json**

```json
{
  "西红柿": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2},
  "番茄": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2},
  "鸡蛋": {"calories": 144, "protein": 13.3, "carbs": 2.8, "fat": 8.8, "fiber": 0},
  "食用油": {"calories": 899, "protein": 0, "carbs": 0, "fat": 100, "fiber": 0},
  "盐": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0},
  "糖": {"calories": 392, "protein": 0, "carbs": 99.8, "fat": 0, "fiber": 0},
  "盐": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0},
  "生抽": {"calories": 60, "protein": 5.6, "carbs": 4.5, "fat": 0.5, "fiber": 0},
  "老抽": {"calories": 85, "protein": 4.2, "carbs": 15, "fat": 0.2, "fiber": 0},
  "醋": {"calories": 31, "protein": 0.1, "carbs": 5.7, "fat": 0.1, "fiber": 0},
  "料酒": {"calories": 112, "protein": 0, "carbs": 1.6, "fat": 0, "fiber": 0},
  "淀粉": {"calories": 344, "protein": 0.5, "carbs": 84, "fat": 0.1, "fiber": 0.1},
  "葱": {"calories": 32, "protein": 1.4, "carbs": 7.3, "fat": 0.2, "fiber": 2.1},
  "姜": {"calories": 41, "protein": 1.8, "carbs": 8.9, "fat": 0.6, "fiber": 2.0},
  "蒜": {"calories": 128, "protein": 5.7, "carbs": 28, "fat": 0.4, "fiber": 1.2},
  "鸡胸肉": {"calories": 133, "protein": 24.6, "carbs": 0, "fat": 2.0, "fiber": 0},
  "猪肉": {"calories": 250, "protein": 17, "carbs": 0, "fat": 20, "fiber": 0},
  "五花肉": {"calories": 395, "protein": 14, "carbs": 0, "fat": 37, "fiber": 0},
  "牛肉": {"calories": 175, "protein": 20.2, "carbs": 0, "fat": 9.5, "fiber": 0},
  "羊肉": {"calories": 203, "protein": 19.2, "carbs": 0, "fat": 13.5, "fiber": 0},
  "土豆": {"calories": 76, "protein": 2.0, "carbs": 17.2, "fat": 0.2, "fiber": 0.7},
  "马铃薯": {"calories": 76, "protein": 2.0, "carbs": 17.2, "fat": 0.2, "fiber": 0.7},
  "花菜": {"calories": 24, "protein": 2.1, "carbs": 4.2, "fat": 0.3, "fiber": 2.0},
  "西兰花": {"calories": 34, "protein": 2.8, "carbs": 4.4, "fat": 0.4, "fiber": 2.7},
  "豆腐": {"calories": 81, "protein": 8.1, "carbs": 2.0, "fat": 3.7, "fiber": 0.1},
  "黄瓜": {"calories": 15, "protein": 0.8, "carbs": 2.9, "fat": 0.2, "fiber": 0.5},
  "茄子": {"calories": 23, "protein": 1.1, "carbs": 4.9, "fat": 0.2, "fiber": 2.5},
  "青椒": {"calories": 20, "protein": 0.9, "carbs": 4.0, "fat": 0.2, "fiber": 1.5},
  "红椒": {"calories": 26, "protein": 1.0, "carbs": 5.0, "fat": 0.3, "fiber": 1.8},
  "干辣椒": {"calories": 282, "protein": 13.0, "carbs": 45, "fat": 8.0, "fiber": 26},
  "小米辣": {"calories": 31, "protein": 1.2, "carbs": 5.8, "fat": 0.4, "fiber": 1.5},
  "米饭": {"calories": 116, "protein": 2.6, "carbs": 25.9, "fat": 0.3, "fiber": 0.3},
  "面条": {"calories": 110, "protein": 3.6, "carbs": 23, "fat": 0.2, "fiber": 0.5},
  "虾": {"calories": 85, "protein": 18.0, "carbs": 0.2, "fat": 1.0, "fiber": 0},
  "鱼": {"calories": 110, "protein": 18.0, "carbs": 0, "fat": 3.5, "fiber": 0},
  "紫菜": {"calories": 262, "protein": 26.7, "carbs": 38.1, "fat": 4.0, "fiber": 24},
  "花生": {"calories": 567, "protein": 25.8, "carbs": 16.1, "fat": 44.3, "fiber": 8.5},
  "白菜": {"calories": 17, "protein": 1.5, "carbs": 3.2, "fat": 0.1, "fiber": 0.9},
  "芹菜": {"calories": 14, "protein": 1.0, "carbs": 2.5, "fat": 0.2, "fiber": 1.6},
  "香菜": {"calories": 32, "protein": 2.1, "carbs": 5.0, "fat": 0.4, "fiber": 2.8},
  "胡萝卜": {"calories": 41, "protein": 1.2, "carbs": 9.6, "fat": 0.2, "fiber": 2.8},
  "洋葱": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1, "fiber": 0.8},
  "玉米": {"calories": 86, "protein": 3.3, "carbs": 19.0, "fat": 1.2, "fiber": 2.9},
  "南瓜": {"calories": 23, "protein": 1.0, "carbs": 5.3, "fat": 0.1, "fiber": 0.8},
  "冬瓜": {"calories": 11, "protein": 0.4, "carbs": 2.6, "fat": 0.1, "fiber": 0.7},
  "韭菜": {"calories": 26, "protein": 2.4, "carbs": 3.5, "fat": 0.5, "fiber": 1.4},
  "蘑菇": {"calories": 22, "protein": 3.1, "carbs": 2.5, "fat": 0.3, "fiber": 1.8},
  "金针菇": {"calories": 32, "protein": 2.7, "carbs": 4.8, "fat": 0.4, "fiber": 2.7},
  "香菇": {"calories": 26, "protein": 2.2, "carbs": 3.4, "fat": 0.3, "fiber": 2.5},
  "木耳": {"calories": 27, "protein": 1.5, "carbs": 5.9, "fat": 0.1, "fiber": 2.5},
  "红豆": {"calories": 324, "protein": 20.2, "carbs": 63.4, "fat": 0.6, "fiber": 12.0},
  "绿豆": {"calories": 329, "protein": 21.6, "carbs": 62.0, "fat": 1.2, "fiber": 10.0},
  "黄豆": {"calories": 359, "protein": 35.0, "carbs": 19.6, "fat": 16.0, "fiber": 15.0},
  "鸡翅": {"calories": 194, "protein": 18.0, "carbs": 0, "fat": 12.0, "fiber": 0},
  "鸡腿": {"calories": 181, "protein": 17.6, "carbs": 0, "fat": 11.5, "fiber": 0},
  "排骨": {"calories": 280, "protein": 16.0, "carbs": 0, "fat": 23.0, "fiber": 0},
  "猪蹄": {"calories": 257, "protein": 22.0, "carbs": 0, "fat": 18.0, "fiber": 0},
  "牛奶": {"calories": 54, "protein": 3.0, "carbs": 5.0, "fat": 3.2, "fiber": 0},
  "酸奶": {"calories": 72, "protein": 3.5, "carbs": 9.0, "fat": 2.5, "fiber": 0},
  "黄油": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81.0, "fiber": 0},
  "芝士": {"calories": 350, "protein": 25.0, "carbs": 1.3, "fat": 28.0, "fiber": 0},
  "面粉": {"calories": 364, "protein": 10.3, "carbs": 76.0, "fat": 1.1, "fiber": 2.7},
  "燕麦": {"calories": 389, "protein": 16.9, "carbs": 66.3, "fat": 6.9, "fiber": 10.6},
  "大米": {"calories": 346, "protein": 7.5, "carbs": 77.2, "fat": 0.8, "fiber": 0.7},
  "枸杞": {"calories": 349, "protein": 14.3, "carbs": 64.1, "fat": 4.6, "fiber": 13.0},
  "红枣": {"calories": 264, "protein": 3.2, "carbs": 67.8, "fat": 0.4, "fiber": 9.5},
  "银耳": {"calories": 200, "protein": 10.0, "carbs": 64.0, "fat": 1.4, "fiber": 30.0},
  "莲子": {"calories": 344, "protein": 17.2, "carbs": 73.0, "fat": 2.0, "fiber": 11.0}
}
```

- [ ] **Step 3: 创建 ingredient_aliases.json**

```json
{
  "西红柿": ["番茄", "西红柿"],
  "土豆": ["马铃薯", "土豆"],
  "卷心菜": ["包菜", "圆白菜", "卷心菜"],
  "青椒": ["柿子椒", "青椒", "甜椒"],
  "花菜": ["菜花", "花菜"],
  "胡萝卜": ["红萝卜", "胡萝卜"],
  "木耳": ["黑木耳", "木耳"],
  "香菇": ["冬菇", "香菇"],
  "紫菜": ["海苔", "紫菜"],
  "虾": ["虾仁", "虾", "大虾"],
  "鱼": ["鱼肉", "鱼"],
  "猪肉": ["猪肉", "瘦肉", "里脊"],
  "牛肉": ["牛肉", "牛柳"],
  "鸡肉": ["鸡肉", "鸡胸肉", "鸡腿"],
  "羊肉": ["羊肉", "羊排"],
  "鸡蛋": ["鸡蛋", "蛋"],
  "大米": ["大米", "米"],
  "面粉": ["面粉", "中筋面粉"]
}
```

- [ ] **Step 4: 创建 user_preferences.json（空模板）**

```json
{
  "disliked_ingredients": [],
  "disliked_taste": [],
  "favorite_categories": [],
  "favorite_recipes": [],
  "default_spiciness_max": 5,
  "default_calories_max": 1000,
  "diet_mode": null,
  "disliked_recipes": []
}
```

- [ ] **Step 5: 创建 src/__init__.py**

```python
# cooking-skill source package
```

- [ ] **Step 6: 验证文件结构**

```bash
ls -R /workspace/cooking-skill/
```

确认目录结构和文件都存在。

---

### Task 2: 营养计算器 - nutrition_calculator.py

**目标:** 实现营养估算功能，根据食材列表计算卡路里、蛋白质、碳水、脂肪，以及辣度推断

**Files:**
- Create: `/workspace/cooking-skill/src/nutrition_calculator.py`
- Test: `/workspace/cooking-skill/tests/test_nutrition.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_nutrition.py
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.nutrition_calculator import NutritionCalculator

def load_json(name):
    with open(f'data/{name}', 'r', encoding='utf-8') as f:
        return json.load(f)

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
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd /workspace/cooking-skill && python -m pytest tests/test_nutrition.py -v
```

- [ ] **Step 3: 实现 NutritionCalculator**

```python
# src/nutrition_calculator.py
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
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd /workspace/cooking-skill && python -m pytest tests/test_nutrition.py -v
```

---

### Task 3: 索引构建器 - index_builder.py

**目标:** 从 HowToCook GitHub 仓库抓取菜谱，解析元数据，计算营养数据，输出索引文件

**Files:**
- Create: `/workspace/cooking-skill/src/index_builder.py`
- Create: `/workspace/cooking-skill/chef_skill.py`（创建基础入口）

- [ ] **Step 1: 实现索引构建器**

```python
# src/index_builder.py
import json
import os
import re
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
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        print(f"已构建 {len(recipes)} 道菜谱索引 -> {output_path}")

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
                print(f"获取菜谱失败 {dir_name}: {e}")
                return None

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
```

---

### Task 4: 食材匹配引擎 - ingredient_matcher.py

**目标:** 实现食材别名匹配和反推菜谱功能

**Files:**
- Create: `/workspace/cooking-skill/src/ingredient_matcher.py`
- Test: `/workspace/cooking-skill/tests/test_matcher.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_matcher.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.ingredient_matcher import IngredientMatcher

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
```

- [ ] **Step 2: 实现 IngredientMatcher**

```python
# src/ingredient_matcher.py
import json
from typing import Dict, List, Set

class IngredientMatcher:
    def __init__(self, aliases_path: str):
        with open(aliases_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.aliases = data
        self.name_to_canonical = {}
        for canonical, variants in data.items():
            for variant in variants:
                self.name_to_canonical[variant] = canonical

    def resolve_name(self, name: str) -> str:
        return self.name_to_canonical.get(name, name)

    def normalize_ingredients(self, ingredients: List[str]) -> List[str]:
        normalized = []
        for item in ingredients:
            clean = item.strip()
            resolved = self.resolve_name(clean)
            if resolved not in normalized:
                normalized.append(resolved)
        return normalized

    def find_by_ingredients(self, user_ingredients: List[str], recipes: List[Dict], min_match: float = 0.3) -> List[Dict]:
        user_set = set(self.normalize_ingredients(user_ingredients))
        scored = []
        for recipe in recipes:
            recipe_ingredients = set(self.normalize_ingredients(recipe.get("ingredients", [])))
            if not recipe_ingredients:
                continue
            match_count = len(user_set & recipe_ingredients)
            match_ratio = match_count / len(recipe_ingredients)
            if match_ratio >= min_match:
                scored.append({
                    **recipe,
                    "match_ratio": round(match_ratio, 2),
                    "matched_ingredients": list(user_set & recipe_ingredients),
                })
        scored.sort(key=lambda x: x["match_ratio"], reverse=True)
        return scored

    def get_shopping_list(self, recipes: List[Dict], have_ingredients: List[str] = None) -> List[str]:
        have = set(self.normalize_ingredients(have_ingredients or []))
        needed = {}
        for recipe in recipes:
            for ing in recipe.get("ingredients", []):
                resolved = self.resolve_name(ing.strip())
                if resolved not in have and resolved not in needed:
                    needed[resolved] = ing
        return list(needed.values())
```

- [ ] **Step 3: 运行测试**

```bash
cd /workspace/cooking-skill && python -m pytest tests/test_matcher.py -v
```

---

### Task 5: 推荐引擎 - recommender.py

**目标:** 实现按人数、场景、季节、饮食模式的智能推荐

**Files:**
- Create: `/workspace/cooking-skill/src/recommender.py`
- Test: `/workspace/cooking-skill/tests/test_recommender.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_recommender.py
import sys
import os
import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.recommender import Recommender

def get_sample_recipes():
    return [
        {"name": "宫保鸡丁", "category": "meat_dish", "category_cn": "荤菜", "difficulty": 2, "spiciness": 3, "nutrition": {"calories": 380, "protein": 28, "carbs": 15, "fat": 22}, "ingredients": ["鸡胸肉", "花生", "干辣椒"], "cooking_time_min": 20, "tags": ["麻辣"], "steps": ["切丁", "炒制"]},
        {"name": "清炒花菜", "category": "vegetable_dish", "category_cn": "素菜", "difficulty": 1, "spiciness": 0, "nutrition": {"calories": 85, "protein": 3, "carbs": 12, "fat": 4}, "ingredients": ["花菜"], "cooking_time_min": 8, "tags": ["清淡", "快手"], "steps": ["切块", "翻炒"]},
        {"name": "紫菜蛋花汤", "category": "soup", "category_cn": "汤粥", "difficulty": 1, "spiciness": 0, "nutrition": {"calories": 60, "protein": 5, "carbs": 6, "fat": 2}, "ingredients": ["紫菜", "鸡蛋"], "cooking_time_min": 10, "tags": ["清淡", "快手"], "steps": ["烧水", "打蛋"]},
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
```

- [ ] **Step 2: 实现 Recommender**

```python
# src/recommender.py
import random
import datetime
from typing import Dict, List, Optional

class Recommender:
    CATEGORY_PRIORITY = {
        "meat_dish": "荤菜",
        "aquatic": "水产",
        "vegetable_dish": "素菜",
        "soup": "汤粥",
        "staple": "主食",
        "dessert": "甜品",
        "drink": "饮料",
        "breakfast": "早餐",
    }

    SEASON_METHODS = {
        "spring": {"prefer": ["清淡", "凉拌", "蒸"], "avoid": []},
        "summer": {"prefer": ["凉拌", "清蒸", "清淡", "快手"], "avoid": ["炖"]},
        "autumn": {"prefer": ["汤粥", "炖", "蒸"], "avoid": []},
        "winter": {"prefer": ["炖", "红烧", "汤粥", "焖"], "avoid": ["凉拌"]},
    }

    def __init__(self, recipes: List[Dict]):
        self.recipes = recipes

    def recommend(
        self,
        people: int = 2,
        scene: str = "workday",
        diet_mode: str = None,
        max_spiciness: int = 5,
        max_calories: int = 1000,
        exclude_categories: List[str] = None,
        prefer_categories: List[str] = None,
        have_ingredients: List[str] = None,
        disliked_ingredients: List[str] = None,
        avoid_recipe_names: List[str] = None,
    ) -> List[Dict]:
        candidates = list(self.recipes)

        if have_ingredients:
            from src.ingredient_matcher import IngredientMatcher
            try:
                matcher = IngredientMatcher("data/ingredient_aliases.json")
                candidates = matcher.find_by_ingredients(have_ingredients, candidates, min_match=0.3)
            except Exception:
                pass

        if diet_mode == "low_fat":
            candidates = [r for r in candidates if r.get("nutrition", {}).get("fat", 100) < 20]
            max_calories = min(max_calories, 400)

        if max_spiciness < 5:
            candidates = [r for r in candidates if r.get("spiciness", 0) <= max_spiciness]

        if max_calories < 1000:
            candidates = [r for r in candidates if r.get("nutrition", {}).get("calories", 0) <= max_calories]

        if scene == "workday":
            candidates = [r for r in candidates if r.get("difficulty", 5) <= 2]

        if disliked_ingredients:
            from src.ingredient_matcher import IngredientMatcher
            try:
                matcher = IngredientMatcher("data/ingredient_aliases.json")
                disliked_resolved = set(matcher.resolve_name(i) for i in disliked_ingredients)
            except Exception:
                disliked_resolved = set(disliked_ingredients)
            candidates = [r for r in candidates if not any(
                matcher.resolve_name(i) in disliked_resolved 
                for i in r.get("ingredients", [])
            ) if 'matcher' in dir()]
            candidates = self._filter_disliked(candidates, disliked_ingredients)

        if avoid_recipe_names:
            candidates = [r for r in candidates if r["name"] not in avoid_recipe_names]

        if prefer_categories:
            prefer_set = set(prefer_categories)
            candidates = [r for r in candidates if r.get("category") in prefer_set] + \
                        [r for r in candidates if r.get("category") not in prefer_set]

        season = self._get_season()
        season_prefs = self.SEASON_METHODS.get(season, {})
        preferred_tags = season_prefs.get("prefer", [])
        if preferred_tags:
            preferred = [r for r in candidates if any(t in r.get("tags", []) for t in preferred_tags)]
            others = [r for r in candidates if not any(t in r.get("tags", []) for t in preferred_tags)]
            candidates = preferred + others

        candidates = self._remove_duplicate_main_ingredient(candidates)

        count = self._get_dish_count(people)
        if len(candidates) > count:
            selected = self._select_balanced(candidates, count)
        else:
            selected = candidates

        return selected[:count]

    def generate_menu_card(self, recipes: List[Dict], people: int = 2) -> str:
        lines = []
        lines.append(f"🍽️ 今日推荐（{people} 人份）")
        lines.append("=" * 40)
        lines.append("")

        for i, recipe in enumerate(recipes, 1):
            n = recipe.get("nutrition", {})
            stars = "⭐" * recipe.get("difficulty", 1)
            chili = "🌶️" * recipe.get("spiciness", 0) if recipe.get("spiciness", 0) > 0 else "🍃"
            
            lines.append(f"{i}. {recipe['name']} {stars} {chili}")
            lines.append(f"   卡路里: {n.get('calories', '?')}kcal | 蛋白质: {n.get('protein', '?')}g | 碳水: {n.get('carbs', '?')}g | 脂肪: {n.get('fat', '?')}g")
            lines.append(f"   难度: {recipe.get('difficulty', '?')} 星 | 预计时间: {recipe.get('cooking_time_min', '?')}-{recipe.get('cooking_time_max', '?')} 分钟")
            lines.append(f"   类型: {recipe.get('category_cn', '?')} | 口味: {'/'.join(recipe.get('tags', ['普通']))}")
            lines.append("")

        return "\n".join(lines)

    def generate_recipe_detail(self, recipe: Dict, servings: int = 2) -> str:
        lines = []
        n = recipe.get("nutrition", {})
        stars = "⭐" * recipe.get("difficulty", 1)
        chili = "🌶️" * recipe.get("spiciness", 0) if recipe.get("spiciness", 0) > 0 else "🍃 不辣"
        
        lines.append(f"📖 {recipe['name']}")
        lines.append("=" * 40)
        lines.append(f"难度: {stars} | 辣度: {chili} | 卡路里: {n.get('calories', '?')}kcal/份")
        lines.append("")
        lines.append(f"食材（{servings} 人份）：")
        for ing in recipe.get("ingredients", []):
            lines.append(f"  • {ing}")
        lines.append("")
        lines.append("步骤：")
        for i, step in enumerate(recipe.get("steps", []), 1):
            lines.append(f"  {i}. {step}")
        lines.append("")
        lines.append("=" * 40)
        return "\n".join(lines)

    def generate_shopping_list(self, recipes: List[Dict], have: List[str] = None) -> str:
        from src.ingredient_matcher import IngredientMatcher
        try:
            matcher = IngredientMatcher("data/ingredient_aliases.json")
            needed = matcher.get_shopping_list(recipes, have)
        except Exception:
            needed = []
            for r in recipes:
                for ing in r.get("ingredients", []):
                    if ing not in needed:
                        needed.append(ing)

        recipe_names = " + ".join(r["name"] for r in recipes)
        lines = [
            f"📋 购物清单（{recipe_names}）",
            "=" * 40,
        ]
        if needed:
            lines.append("需要购置：")
            for item in needed:
                lines.append(f"  • {item}")
        else:
            lines.append("食材齐全，无需购买！")
        return "\n".join(lines)

    def _get_season(self) -> str:
        month = datetime.datetime.now().month
        if 3 <= month <= 5:
            return "spring"
        elif 6 <= month <= 8:
            return "summer"
        elif 9 <= month <= 11:
            return "autumn"
        return "winter"

    def _get_dish_count(self, people: int) -> int:
        if people <= 2:
            return 2
        elif people <= 4:
            return 4
        elif people <= 6:
            return 6
        return 4

    def _select_balanced(self, candidates: List[Dict], count: int) -> List[Dict]:
        selected = []
        used_categories = set()
        used_main_ingredients = set()

        meat_cats = {"meat_dish", "aquatic"}
        for cat in meat_cats:
            cat_candidates = [r for r in candidates if r.get("category") == cat and r.get("category") not in used_categories]
            if cat_candidates:
                chosen = random.choice(cat_candidates)
                selected.append(chosen)
                used_categories.add(chosen.get("category"))
                used_main_ingredients.update(self._get_main_ingredient(chosen))

        for cat in ["vegetable_dish", "soup", "staple", "dessert", "drink"]:
            if len(selected) >= count:
                break
            cat_candidates = [r for r in candidates if r.get("category") == cat]
            filtered = [r for r in cat_candidates if not self._conflicts(r, used_main_ingredients)]
            if filtered:
                chosen = random.choice(filtered)
                selected.append(chosen)
                used_main_ingredients.update(self._get_main_ingredient(chosen))
            elif cat_candidates:
                chosen = random.choice(cat_candidates)
                selected.append(chosen)

        remaining = [r for r in candidates if r not in selected]
        while len(selected) < count and remaining:
            chosen = random.choice(remaining)
            selected.append(chosen)
            remaining.remove(chosen)

        return selected

    def _remove_duplicate_main_ingredient(self, candidates: List[Dict]) -> List[Dict]:
        result = []
        used = set()
        for r in candidates:
            main = self._get_main_ingredient(r)
            if not main.intersection(used):
                result.append(r)
                used.update(main)
            else:
                result.append(r)
        return result

    def _get_main_ingredient(self, recipe: Dict) -> set:
        ingredients = recipe.get("ingredients", [])
        main = set()
        for ing in ingredients:
            for keyword in ["肉", "鸡", "鱼", "虾", "牛", "羊", "猪", "排", "蛋"]:
                if keyword in ing and len(ing) <= 6:
                    main.add(ing)
                    break
        return main

    def _conflicts(self, recipe: Dict, used_ingredients: set) -> bool:
        main = self._get_main_ingredient(recipe)
        return bool(main & used_ingredients)

    def _filter_disliked(self, candidates: List[Dict], disliked: List[str]) -> List[Dict]:
        from src.ingredient_matcher import IngredientMatcher
        try:
            matcher = IngredientMatcher("data/ingredient_aliases.json")
            disliked_resolved = set(matcher.resolve_name(i) for i in disliked)
        except Exception:
            disliked_resolved = set(disliked)
        
        result = []
        for r in candidates:
            has_disliked = False
            for ing in r.get("ingredients", []):
                try:
                    resolved = matcher.resolve_name(ing.strip())
                except Exception:
                    resolved = ing.strip()
                if resolved in disliked_resolved:
                    has_disliked = True
                    break
            if not has_disliked:
                result.append(r)
        return result
```

- [ ] **Step 3: 运行测试**

```bash
cd /workspace/cooking-skill && python -m pytest tests/test_recommender.py -v
```

---

### Task 6: 菜谱同步服务 - recipe_sync.py

**目标:** 实现增量同步，对比远程与本地差异，更新索引

**Files:**
- Create: `/workspace/cooking-skill/src/recipe_sync.py`

- [ ] **Step 1: 实现同步服务**

```python
# src/recipe_sync.py
import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List
from src.index_builder import IndexBuilder
from src.nutrition_calculator import NutritionCalculator

class RecipeSync:
    def __init__(self, nutrition_db_path: str, aliases_path: str, index_path: str):
        self.builder = IndexBuilder(nutrition_db_path, aliases_path)
        self.index_path = index_path
        self.calc = NutritionCalculator(nutrition_db_path)

    def sync(self) -> Dict:
        old_recipes = self._load_existing()
        old_names = {r["name"] for r in old_recipes}

        self.builder.build(self.index_path)
        new_recipes = self._load_existing()
        new_names = {r["name"] for r in new_recipes}

        added = new_names - old_names
        removed = old_names - new_names

        result = {
            "synced_at": datetime.now().isoformat(),
            "total_recipes": len(new_recipes),
            "added": list(added),
            "removed": list(removed),
        }

        if added:
            result["message"] = f"新增 {len(added)} 道菜谱: {', '.join(added[:5])}{'...' if len(added) > 5 else ''}"
        else:
            result["message"] = "菜谱无更新"

        return result

    def _load_existing(self) -> List[Dict]:
        if not os.path.exists(self.index_path):
            return []
        with open(self.index_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def run_sync():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sync = RecipeSync(
        nutrition_db_path=os.path.join(base_dir, "data", "nutrition_db.json"),
        aliases_path=os.path.join(base_dir, "data", "ingredient_aliases.json"),
        index_path=os.path.join(base_dir, "data", "recipes_index.json"),
    )
    result = sync.sync()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

if __name__ == "__main__":
    run_sync()
```

---

### Task 7: 技能交互入口 - chef_skill.py

**目标:** 实现 CLI 交互入口，支持语义化命令

**Files:**
- Modify: `/workspace/cooking-skill/chef_skill.py`

- [ ] **Step 1: 实现 CLI 入口**

```python
#!/usr/bin/env python3
"""智能烹饪技能 - CLI 交互入口"""
import json
import os
import sys
import argparse
from src.recommender import Recommender
from src.ingredient_matcher import IngredientMatcher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "data", "recipes_index.json")
NUTRITION_PATH = os.path.join(BASE_DIR, "data", "nutrition_db.json")
ALIASES_PATH = os.path.join(BASE_DIR, "data", "ingredient_aliases.json")
PREFS_PATH = os.path.join(BASE_DIR, "data", "user_preferences.json")

def load_recipes():
    if not os.path.exists(INDEX_PATH):
        print("❌ 菜谱索引不存在，请先运行索引构建: python chef_skill.py build")
        sys.exit(1)
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_preferences():
    if not os.path.exists(PREFS_PATH):
        return {}
    with open(PREFS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def cmd_recommend(args):
    recipes = load_recipes()
    prefs = load_preferences()
    rec = Recommender(recipes)

    result = rec.recommend(
        people=args.people or 2,
        scene=args.scene or "workday",
        diet_mode=args.diet or prefs.get("diet_mode"),
        max_spiciness=args.no_spicy and 0 or prefs.get("default_spiciness_max", 5),
        max_calories=args.low_cal and 350 or prefs.get("default_calories_max", 1000),
        have_ingredients=args.ingredients,
        disliked_ingredients=prefs.get("disliked_ingredients", []),
        avoid_recipe_names=prefs.get("disliked_recipes", []),
    )

    print(rec.generate_menu_card(result, args.people or 2))

    if args.shopping_list:
        print("")
        print(rec.generate_shopping_list(result, args.ingredients))

def cmd_search(args):
    recipes = load_recipes()
    keyword = " ".join(args.keyword)
    matches = [r for r in recipes if keyword.lower() in r["name"].lower()]
    
    if not matches:
        print(f"未找到包含 '{keyword}' 的菜谱")
        return

    print(f"找到 {len(matches)} 道菜谱:")
    for r in matches[:10]:
        n = r.get("nutrition", {})
        print(f"  • {r['name']} | {r.get('category_cn')} | ⭐{r.get('difficulty')} | 🌶️{r.get('spiciness')} | {n.get('calories', '?')}kcal")

def cmd_detail(args):
    recipes = load_recipes()
    name = " ".join(args.name)
    match = next((r for r in recipes if name.lower() in r["name"].lower()), None)
    
    if not match:
        print(f"未找到 '{name}' 的菜谱")
        return

    rec = Recommender(recipes)
    print(rec.generate_recipe_detail(match, args.servings or 2))

def cmd_nutrition(args):
    recipes = load_recipes()
    name = " ".join(args.name)
    match = next((r for r in recipes if name.lower() in r["name"].lower()), None)
    
    if not match:
        print(f"未找到 '{name}' 的营养信息")
        return

    n = match.get("nutrition", {})
    print(f"📊 {match['name']} 营养信息:")
    print(f"   卡路里: {n.get('calories', '?')}kcal")
    print(f"   蛋白质: {n.get('protein', '?')}g")
    print(f"   碳水: {n.get('carbs', '?')}g")
    print(f"   脂肪: {n.get('fat', '?')}g")
    print(f"   辣度: {'🌶️' * match.get('spiciness', 0)} ({match.get('spiciness', 0)}/5)")

def cmd_ingredients(args):
    recipes = load_recipes()
    matcher = IngredientMatcher(ALIASES_PATH)
    result = matcher.find_by_ingredients(args.ingredients, recipes, min_match=float(args.min_match or 0.3))
    
    if not result:
        print(f"未找到能用 {', '.join(args.ingredients)} 做的菜")
        return

    print(f"🍳 可以做的菜（匹配度从高到低）:")
    for r in result[:10]:
        matched = ", ".join(r.get("matched_ingredients", []))
        print(f"  • {r['name']} | 匹配度: {r.get('match_ratio', 0)*100:.0f}% | 匹配食材: {matched}")

def cmd_build(args):
    from src.index_builder import IndexBuilder
    builder = IndexBuilder(NUTRITION_PATH, ALIASES_PATH)
    builder.build(INDEX_PATH)

def cmd_sync(args):
    from src.recipe_sync import run_sync
    run_sync()

def main():
    parser = argparse.ArgumentParser(description="🍳 智能烹饪技能 CLI")
    subparsers = parser.add_subparsers(dest="command")

    p_recommend = subparsers.add_parser("recommend", help="推荐菜式")
    p_recommend.add_argument("--people", type=int, help="用餐人数")
    p_recommend.add_argument("--scene", choices=["workday", "weekend"], help="场景")
    p_recommend.add_argument("--diet", choices=["low_fat"], help="饮食模式")
    p_recommend.add_argument("--no-spicy", action="store_true", help="不吃辣")
    p_recommend.add_argument("--low-cal", action="store_true", help="低卡路里")
    p_recommend.add_argument("--ingredients", nargs="+", help="家中食材")
    p_recommend.add_argument("--shopping-list", action="store_true", help="生成购物清单")

    p_search = subparsers.add_parser("search", help="搜索菜谱")
    p_search.add_argument("keyword", nargs="+", help="搜索关键词")

    p_detail = subparsers.add_parser("detail", help="查看菜谱详情")
    p_detail.add_argument("name", nargs="+", help="菜名")
    p_detail.add_argument("--servings", type=int, default=2, help="份数")

    p_nutrition = subparsers.add_parser("nutrition", help="查看营养信息")
    p_nutrition.add_argument("name", nargs="+", help="菜名")

    p_ingredients = subparsers.add_parser("ingredients", help="根据食材反推菜谱")
    p_ingredients.add_argument("ingredients", nargs="+", help="食材列表")
    p_ingredients.add_argument("--min-match", type=float, default=0.3, help="最低匹配度")

    subparsers.add_parser("build", help="构建菜谱索引")
    subparsers.add_parser("sync", help="同步菜谱更新")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    commands = {
        "recommend": cmd_recommend,
        "search": cmd_search,
        "detail": cmd_detail,
        "nutrition": cmd_nutrition,
        "ingredients": cmd_ingredients,
        "build": cmd_build,
        "sync": cmd_sync,
    }
    
    commands[args.command](args)

if __name__ == "__main__":
    main()
```

---

### Task 8: 构建索引 + 首次运行测试

**目标:** 构建菜谱索引，验证完整流程

**Files:**
- No file changes, execution only

- [ ] **Step 1: 安装依赖**

```bash
cd /workspace/cooking-skill && pip install -r requirements.txt
```

- [ ] **Step 2: 构建索引**

```bash
cd /workspace/cooking-skill && python chef_skill.py build
```

预期输出：`已构建 XXX 道菜谱索引 -> /workspace/cooking-skill/data/recipes_index.json`

- [ ] **Step 3: 测试推荐**

```bash
cd /workspace/cooking-skill && python chef_skill.py recommend --people 3 --shopping-list
```

- [ ] **Step 4: 测试搜索**

```bash
cd /workspace/cooking-skill && python chef_skill.py search 宫保
```

- [ ] **Step 5: 测试详情**

```bash
cd /workspace/cooking-skill && python chef_skill.py detail 宫保鸡丁 --servings 4
```

- [ ] **Step 6: 测试营养查询**

```bash
cd /workspace/cooking-skill && python chef_skill.py nutrition 宫保鸡丁
```

- [ ] **Step 7: 测试食材反推**

```bash
cd /workspace/cooking-skill && python chef_skill.py ingredients 鸡蛋 西红柿
```

- [ ] **Step 8: 运行全部测试**

```bash
cd /workspace/cooking-skill && python -m pytest tests/ -v
```

---

### Task 9: README 文档

**目标:** 编写使用说明

**Files:**
- Create: `/workspace/cooking-skill/README.md`

- [ ] **Step 1: 创建 README**

```markdown
# 🍳 智能烹饪技能

基于 [HowToCook](https://github.com/Anduin2017/HowToCook) 构建的智能菜谱推荐系统。

## 功能

- 🎯 **智能推荐** - 按人数、场景、季节、饮食模式推荐搭配
- 📊 **营养查询** - 卡路里、蛋白质、碳水、脂肪信息
- 🌶️ **辣度标注** - 0-5 级辣度标识
- 🛒 **购物清单** - 自动生成采购清单
- 🥕 **食材反推** - 根据家中食材推荐可做的菜
- 🔄 **自动同步** - 定期从 HowToCook 更新菜谱

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 构建菜谱索引（首次使用）
python chef_skill.py build

# 推荐今天吃什么（2人份）
python chef_skill.py recommend --people 2

# 推荐 + 购物清单
python chef_skill.py recommend --people 3 --shopping-list

# 低脂餐推荐
python chef_skill.py recommend --diet low_fat --no-spicy

# 搜索菜谱
python chef_skill.py search 宫保

# 查看菜谱详情（含做法）
python chef_skill.py detail 宫保鸡丁

# 查看营养信息
python chef_skill.py nutrition 宫保鸡丁

# 根据食材反推
python chef_skill.py ingredients 鸡蛋 西红柿 豆腐

# 同步最新菜谱
python chef_skill.py sync
```

## 命令说明

| 命令 | 说明 | 示例 |
|------|------|------|
| `recommend` | 智能推荐 | `recommend --people 3 --shopping-list` |
| `search` | 搜索菜谱 | `search 宫保` |
| `detail` | 菜谱详情 | `detail 宫保鸡丁 --servings 4` |
| `nutrition` | 营养查询 | `nutrition 西红柿炒鸡蛋` |
| `ingredients` | 食材反推 | `ingredients 鸡蛋 西红柿` |
| `build` | 构建索引 | `build` |
| `sync` | 同步更新 | `sync` |

## 推荐选项

| 选项 | 说明 |
|------|------|
| `--people N` | 用餐人数（影响搭配数量） |
| `--scene workday/weekend` | 场景（工作日推荐快手菜） |
| `--diet low_fat` | 低脂模式 |
| `--no-spicy` | 不吃辣 |
| `--low-cal` | 低卡路里 |
| `--ingredients A B` | 家中食材列表 |
| `--shopping-list` | 生成购物清单 |

## 输出示例

### 推荐卡片
```
🍽️ 今日推荐（3 人份）
========================================

1. 宫保鸡丁 ⭐⭐ 🌶️🌶️🌶️
   卡路里: 380kcal | 蛋白质: 28g | 碳水: 15g | 脂肪: 22g
   难度: 2 星 | 预计时间: 15-25 分钟
   类型: 荤菜 | 口味: 麻辣

2. 清炒花菜 ⭐ 🍃
   卡路里: 85kcal | 蛋白质: 3g | 碳水: 12g | 脂肪: 4g
   难度: 1 星 | 预计时间: 5-15 分钟
   类型: 素菜 | 口味: 清淡/快手
```

### 菜谱详情
```
📖 宫保鸡丁
========================================
难度: ⭐⭐ | 辣度: 🌶️🌶️🌶️ | 卡路里: 380kcal/份

食材（2 人份）：
  • 鸡胸肉 200g
  • 花生 50g
  ...

步骤：
  1. 鸡胸肉切丁...
  2. ...
```

## 定时同步

可通过 crontab 设置每周同步：
```
0 8 * * 1 cd /path/to/cooking-skill && python chef_skill.py sync >> /dev/null 2>&1
```

## 营养数据来源

营养数据基于公开营养数据库整理，为估算值，仅供参考。
```

---

## 自审清单

### 1. 设计文档覆盖检查

| 设计需求 | 对应 Task | 状态 |
|---------|-----------|------|
| 数据索引构建 | Task 3, 8 | ✅ |
| 营养估算模型 | Task 1, 2 | ✅ |
| 辣度推断 | Task 2 | ✅ |
| 语义化推荐 | Task 5, 7 | ✅ |
| 食材反推 | Task 4, 7 | ✅ |
| 购物清单 | Task 4, 5, 7 | ✅ |
| 按人数搭配 | Task 5 | ✅ |
| 季节性推荐 | Task 5 | ✅ |
| 低脂餐支持 | Task 2, 5, 7 | ✅ |
| 菜品去重 | Task 5 | ✅ |
| 烹饪时间估算 | Task 3, 5 | ✅ |
| 定时同步 | Task 6 | ✅ |
| 用户偏好 | Task 1, 5, 7 | ✅ |
| 食材别名 | Task 1, 4 | ✅ |
| 输出格式友好 | Task 5, 7, 9 | ✅ |

### 2. 占位符扫描

- 无 TBD/TODO
- 所有测试包含完整代码
- 所有实现包含完整代码

### 3. 类型一致性

- 所有模块使用统一的 Dict/List 类型注解
- 菜谱索引字段在各模块间一致

### 4. 范围检查

- 聚焦于菜谱推荐技能，未超出设计范围
- 9 个 Task 均可独立验证
