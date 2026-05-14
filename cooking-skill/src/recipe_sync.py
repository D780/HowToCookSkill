import json
import os
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
            result["message"] = f"新增 {len(added)} 道菜谱: {', '.join(list(added)[:5])}{'...' if len(added) > 5 else ''}"
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
