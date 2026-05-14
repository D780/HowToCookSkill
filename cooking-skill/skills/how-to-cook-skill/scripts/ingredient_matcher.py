import json
from typing import Dict, List


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
            clean = self._clean_name(item)
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
                resolved = self.resolve_name(self._clean_name(ing))
                if resolved not in have and resolved not in needed:
                    needed[resolved] = ing
        return list(needed.values())

    def _clean_name(self, name: str) -> str:
        import re
        name = re.sub(r'\d+(?:\.\d+)?\s*(?:g|克|ml|毫升|个|只|根|颗|瓣|块|勺|片)', '', name)
        return name.strip()
