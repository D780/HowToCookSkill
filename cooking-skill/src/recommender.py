import random
import datetime
from typing import Dict, List, Optional


class Recommender:
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
            candidates = self._filter_disliked(candidates, disliked_ingredients)

        if avoid_recipe_names:
            candidates = [r for r in candidates if r["name"] not in avoid_recipe_names]

        if prefer_categories:
            prefer_set = set(prefer_categories)
            preferred = [r for r in candidates if r.get("category") in prefer_set]
            others = [r for r in candidates if r.get("category") not in prefer_set]
            candidates = preferred + others

        season = self._get_season()
        season_prefs = self.SEASON_METHODS.get(season, {})
        preferred_tags = season_prefs.get("prefer", [])
        if preferred_tags:
            preferred = [r for r in candidates if any(t in r.get("tags", []) for t in preferred_tags)]
            others = [r for r in candidates if not any(t in r.get("tags", []) for t in preferred_tags)]
            candidates = preferred + others

        count = self._get_dish_count(people)
        if len(candidates) > count:
            selected = self._select_balanced(candidates, count)
        else:
            selected = candidates

        return selected[:count]

    def generate_menu_card(self, recipes: List[Dict], people: int = 2) -> str:
        lines = []
        lines.append(f"今日推荐（{people} 人份）")
        lines.append("=" * 40)
        lines.append("")

        for i, recipe in enumerate(recipes, 1):
            n = recipe.get("nutrition", {})
            stars = "★" * recipe.get("difficulty", 1)
            if recipe.get("spiciness", 0) > 0:
                chili = f"辣度: {'★' * recipe.get('spiciness', 0)}/5"
            else:
                chili = "不辣"

            tags_str = '/'.join(recipe.get('tags', ['普通']))
            time_range = f"{recipe.get('cooking_time_min', '?')}-{recipe.get('cooking_time_max', '?')} 分钟"

            lines.append(f"{i}. {recipe['name']}")
            lines.append(f"   卡路里: {n.get('calories', '?')}kcal | 蛋白质: {n.get('protein', '?')}g | 碳水: {n.get('carbs', '?')}g | 脂肪: {n.get('fat', '?')}g")
            lines.append(f"   难度: {stars} | 预计时间: {time_range}")
            lines.append(f"   类型: {recipe.get('category_cn', '?')} | {chili} | 口味: {tags_str}")
            lines.append("")

        return "\n".join(lines)

    def generate_recipe_detail(self, recipe: Dict, servings: int = 2) -> str:
        lines = []
        n = recipe.get("nutrition", {})
        stars = "★" * recipe.get("difficulty", 1)
        if recipe.get("spiciness", 0) > 0:
            chili = f"{'★' * recipe.get('spiciness', 0)}/5"
        else:
            chili = "不辣"

        lines.append(f"【{recipe['name']}】")
        lines.append("=" * 40)
        lines.append(f"难度: {stars} | 辣度: {chili} | 卡路里: {n.get('calories', '?')}kcal/份")
        lines.append(f"预计时间: {recipe.get('cooking_time_min', '?')}-{recipe.get('cooking_time_max', '?')} 分钟")
        lines.append(f"类型: {recipe.get('category_cn', '?')}")
        lines.append("")
        lines.append(f"食材（{servings} 人份）：")
        for ing in recipe.get("ingredients", []):
            lines.append(f"  - {ing}")
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
            f"购物清单（{recipe_names}）",
            "=" * 40,
        ]
        if needed:
            lines.append("需要购置：")
            for item in needed:
                lines.append(f"  - {item}")
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
            cat_candidates = [r for r in candidates if r.get("category") == cat]
            cat_candidates = [r for r in cat_candidates if not self._conflicts(r, used_main_ingredients)]
            if not cat_candidates:
                cat_candidates = [r for r in candidates if r.get("category") == cat]
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
            matcher = None

        result = []
        for r in candidates:
            has_disliked = False
            for ing in r.get("ingredients", []):
                if matcher:
                    try:
                        resolved = matcher.resolve_name(ing.strip())
                    except Exception:
                        resolved = ing.strip()
                else:
                    resolved = ing.strip()
                if resolved in disliked_resolved:
                    has_disliked = True
                    break
            if not has_disliked:
                result.append(r)
        return result
