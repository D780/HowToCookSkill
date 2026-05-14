#!/usr/bin/env python3
"""智能烹饪技能 - CLI 交互入口"""
import json
import os
import sys
import argparse
from scripts.recommender import Recommender
from scripts.ingredient_matcher import IngredientMatcher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "data", "recipes_index.json")
TUTORIALS_PATH = os.path.join(BASE_DIR, "data", "tutorials_index.json")
NUTRITION_PATH = os.path.join(BASE_DIR, "data", "nutrition_db.json")
ALIASES_PATH = os.path.join(BASE_DIR, "data", "ingredient_aliases.json")
PREFS_PATH = os.path.join(BASE_DIR, "data", "user_preferences.json")


def load_recipes():
    if not os.path.exists(INDEX_PATH):
        print("菜谱索引不存在，请先运行索引构建: python chef_skill.py build")
        sys.exit(1)
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_tutorials():
    if not os.path.exists(TUTORIALS_PATH):
        print("教程索引不存在，请先运行索引构建: python chef_skill.py build")
        sys.exit(1)
    with open(TUTORIALS_PATH, 'r', encoding='utf-8') as f:
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
        max_spiciness=0 if args.no_spicy else prefs.get("default_spiciness_max", 5),
        max_calories=350 if args.low_cal else prefs.get("default_calories_max", 1000),
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
        print(f"  - {r['name']} | {r.get('category_cn')} | 难度:{r.get('difficulty')}星 | 辣度:{r.get('spiciness')}/5 | {n.get('calories', '?')}kcal")

    if len(matches) > 10:
        print(f"  ... 还有 {len(matches) - 10} 道")


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
    spiciness = match.get("spiciness", 0)
    chili = f"{'辣度: ★' * spiciness}/5" if spiciness > 0 else "不辣"

    print(f"【{match['name']}】营养信息:")
    print(f"  卡路里: {n.get('calories', '?')}kcal")
    print(f"  蛋白质: {n.get('protein', '?')}g")
    print(f"  碳水: {n.get('carbs', '?')}g")
    print(f"  脂肪: {n.get('fat', '?')}g")
    print(f"  {chili}")


def cmd_ingredients(args):
    recipes = load_recipes()
    matcher = IngredientMatcher(ALIASES_PATH)
    result = matcher.find_by_ingredients(args.ingredients, recipes, min_match=float(args.min_match or 0.3))

    if not result:
        print(f"未找到能用 {', '.join(args.ingredients)} 做的菜")
        return

    print(f"可以做的菜（匹配度从高到低）:")
    for r in result[:10]:
        matched = ", ".join(r.get("matched_ingredients", []))
        n = r.get("nutrition", {})
        print(f"  - {r['name']} | 匹配度: {r.get('match_ratio', 0)*100:.0f}% | 匹配食材: {matched} | {n.get('calories', '?')}kcal")

    if len(result) > 10:
        print(f"  ... 还有 {len(result) - 10} 道")


def cmd_build(args):
    from scripts.index_builder import IndexBuilder
    builder = IndexBuilder(NUTRITION_PATH, ALIASES_PATH)
    builder.build(INDEX_PATH)
    builder.build_tutorials(TUTORIALS_PATH)


def cmd_sync(args):
    from scripts.recipe_sync import run_sync
    run_sync()


def cmd_tutorial(args):
    tutorials = load_tutorials()

    if not args.keyword:
        print("所有烹饪教程:")
        print("=" * 60)
        for t in tutorials:
            print(f"  [{t['category']}] {t['name']}")
            if t.get('keywords'):
                print(f"    关键词: {', '.join(t['keywords'][:5])}")
        print(f"\n共 {len(tutorials)} 篇教程")
        print("查看具体教程: python chef_skill.py tutorial <关键词>")
        return

    keyword = " ".join(args.keyword)
    matches = []
    for t in tutorials:
        if keyword.lower() in t["name"].lower():
            matches.append(t)
            continue
        for kw in t.get("keywords", []):
            if keyword.lower() in kw.lower():
                matches.append(t)
                break

    if not matches:
        print(f"未找到包含 '{keyword}' 的教程")
        print("可用教程:")
        for t in tutorials:
            print(f"  - {t['name']} ({t['category']})")
        return

    t = matches[0]
    content = t.get("content", "")
    lines = content.split("\n")

    print(f"【{t['name']}】")
    print("=" * 60)
    print(f"分类: {t['category']}")
    print(f"来源: {t['source_file']}")
    print(f"关键词: {', '.join(t.get('keywords', []))}")
    print("-" * 60)
    print("")

    in_content = False
    for line in lines:
        if line.startswith("#") and not in_content:
            in_content = True
            continue
        print(line)

    if len(matches) > 1:
        print("\n" + "-" * 60)
        print(f"找到 {len(matches)} 个相关教程，其他匹配:")
        for m in matches[1:]:
            print(f"  - {m['name']} ({m['category']})")


def main():
    parser = argparse.ArgumentParser(
        description="智能烹饪技能 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python chef_skill.py recommend --people 3 --shopping-list
  python chef_skill.py search 宫保
  python chef_skill.py detail 宫保鸡丁
  python chef_skill.py nutrition 西红柿炒鸡蛋
  python chef_skill.py ingredients 鸡蛋 西红柿 豆腐
  python chef_skill.py build
  python chef_skill.py sync
        """,
    )
    subparsers = parser.add_subparsers(dest="command")

    # recommend
    p_recommend = subparsers.add_parser("recommend", help="推荐菜式")
    p_recommend.add_argument("--people", type=int, help="用餐人数")
    p_recommend.add_argument("--scene", choices=["workday", "weekend"], help="场景")
    p_recommend.add_argument("--diet", choices=["low_fat"], help="饮食模式")
    p_recommend.add_argument("--no-spicy", action="store_true", help="不吃辣")
    p_recommend.add_argument("--low-cal", action="store_true", help="低卡路里")
    p_recommend.add_argument("--ingredients", nargs="+", help="家中食材")
    p_recommend.add_argument("--shopping-list", action="store_true", help="生成购物清单")

    # search
    p_search = subparsers.add_parser("search", help="搜索菜谱")
    p_search.add_argument("keyword", nargs="+", help="搜索关键词")

    # detail
    p_detail = subparsers.add_parser("detail", help="查看菜谱详情")
    p_detail.add_argument("name", nargs="+", help="菜名")
    p_detail.add_argument("--servings", type=int, default=2, help="份数")

    # nutrition
    p_nutrition = subparsers.add_parser("nutrition", help="查看营养信息")
    p_nutrition.add_argument("name", nargs="+", help="菜名")

    # ingredients
    p_ingredients = subparsers.add_parser("ingredients", help="根据食材反推菜谱")
    p_ingredients.add_argument("ingredients", nargs="+", help="食材列表")
    p_ingredients.add_argument("--min-match", type=float, default=0.3, help="最低匹配度")

    # build
    subparsers.add_parser("build", help="构建索引")

    # sync
    subparsers.add_parser("sync", help="同步更新")

    # tutorial
    p_tutorial = subparsers.add_parser("tutorial", help="查看烹饪教程")
    p_tutorial.add_argument("keyword", nargs="*", help="教程关键词")

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
        "tutorial": cmd_tutorial,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
