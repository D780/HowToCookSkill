#!/usr/bin/env python3
"""
智能烹饪技能 - 核心功能示例演示
运行所有核心功能并输出结果到 examples/ 目录
"""
import json
import os
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from scripts.recommender import Recommender
from scripts.ingredient_matcher import IngredientMatcher
from scripts.nutrition_calculator import NutritionCalculator

OUTPUT_DIR = os.path.join(BASE_DIR, "examples")


def load_recipes():
    with open(os.path.join(BASE_DIR, "data", "recipes_index.json"), 'r', encoding='utf-8') as f:
        return json.load(f)


def load_tutorials():
    with open(os.path.join(BASE_DIR, "data", "tutorials_index.json"), 'r', encoding='utf-8') as f:
        return json.load(f)


def write_example(name: str, content: str):
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  -> 已输出: {name}")


def example_1_menu_card():
    """示例 1: 智能推荐菜单卡片"""
    recipes = load_recipes()
    rec = Recommender(recipes)

    result = rec.recommend(people=2, scene="workday")
    card = rec.generate_menu_card(result, people=2)

    title = "示例 1：智能推荐菜单卡片（2 人份 / 工作日）"
    content = f"{title}\n{'=' * 50}\n\n{card}"
    write_example("01_menu_card.txt", content)


def example_2_recipe_detail():
    """示例 2: 菜谱详情（含做法和分量估算）"""
    recipes = load_recipes()
    rec = Recommender(recipes)

    match = next((r for r in recipes if "西红柿炒鸡蛋" in r["name"]), None)
    if not match:
        match = next((r for r in recipes if "炒鸡蛋" in r["name"]), recipes[0])

    detail = rec.generate_recipe_detail(match, servings=2)

    title = "示例 2：菜谱详情（含做法和分量估算）"
    content = f"{title}\n{'=' * 50}\n\n{detail}"
    write_example("02_recipe_detail.txt", content)


def example_3_recipe_detail_with_amount():
    """示例 3: 菜谱详情（原始菜谱有分量的例子）"""
    recipes = load_recipes()
    rec = Recommender(recipes)

    match = next((r for r in recipes if "田螺酿" in r["name"]), None)
    if not match:
        match = next((r for r in recipes if "酿" in r["name"]), recipes[0])

    detail = rec.generate_recipe_detail(match, servings=4)

    title = "示例 3：菜谱详情（原始有分量，4 人份）"
    content = f"{title}\n{'=' * 50}\n\n{detail}"
    write_example("03_recipe_detail_amount.txt", content)


def example_4_shopping_list():
    """示例 4: 购物清单（按类别分行展示）"""
    recipes = load_recipes()
    rec = Recommender(recipes)

    result = rec.recommend(people=3, scene="weekend")
    shopping = rec.generate_shopping_list(result, have=["盐", "食用油"])

    title = "示例 4：购物清单（按类别分行展示）"
    content = f"{title}\n{'=' * 50}\n\n{shopping}"
    write_example("04_shopping_list.txt", content)


def example_5_ingredient_search():
    """示例 5: 食材反推"""
    recipes = load_recipes()
    matcher = IngredientMatcher(os.path.join(BASE_DIR, "data", "ingredient_aliases.json"))

    result = matcher.find_by_ingredients(["鸡蛋", "西红柿", "豆腐"], recipes, min_match=0.3)

    lines = [
        "示例 5：食材反推",
        "=" * 50,
        "",
        "家里食材：鸡蛋、西红柿、豆腐",
        "",
        f"可以做的菜（共找到 {len(result)} 道）:",
        "",
    ]
    for r in result[:8]:
        matched = ", ".join(r.get("matched_ingredients", []))
        n = r.get("nutrition", {})
        lines.append(f"  - {r['name']}")
        lines.append(f"    匹配度: {r.get('match_ratio', 0)*100:.0f}% | 匹配食材: {matched} | {n.get('calories', '?')}kcal")
        lines.append("")

    write_example("05_ingredient_search.txt", "\n".join(lines))


def example_6_nutrition_info():
    """示例 6: 营养信息查询"""
    recipes = load_recipes()

    lines = [
        "示例 6：营养信息查询",
        "=" * 50,
        "",
    ]

    for name in ["宫保鸡丁", "西红柿炒鸡蛋", "清蒸鱼", "蒜蓉虾"]:
        match = next((r for r in recipes if name in r["name"]), None)
        if match:
            n = match.get("nutrition", {})
            spiciness = match.get("spiciness", 0)
            chili = f"{'★' * spiciness}/5" if spiciness > 0 else "不辣"
            lines.append(f"【{match['name']}】")
            lines.append(f"  卡路里: {n.get('calories', '?')}kcal | 蛋白质: {n.get('protein', '?')}g | 碳水: {n.get('carbs', '?')}g | 脂肪: {n.get('fat', '?')}g")
            lines.append(f"  辣度: {chili} | 类型: {match.get('category_cn', '?')}")
            lines.append("")

    write_example("06_nutrition_info.txt", "\n".join(lines))


def example_7_tutorials():
    """示例 7: 烹饪教程"""
    tutorials = load_tutorials()

    lines = [
        "示例 7：烹饪教程",
        "=" * 50,
        "",
        "所有教程:",
        "",
    ]
    for t in tutorials:
        lines.append(f"  [{t['category']}] {t['name']}")
        if t.get('keywords'):
            lines.append(f"    关键词: {', '.join(t['keywords'][:5])}")
        lines.append("")

    # 展示一个教程内容
    if tutorials:
        t = tutorials[0]
        content = t.get("content", "")
        preview = content[:500]
        lines.append("-" * 50)
        lines.append(f"【{t['name']}】预览")
        lines.append("-" * 50)
        lines.append("")
        lines.append(preview)
        if len(content) > 500:
            lines.append("\n...（内容较长，已截断）")
        lines.append("")

    write_example("07_tutorials.txt", "\n".join(lines))


def example_8_daily_meals():
    """示例 8: 一日三餐推荐"""
    recipes = load_recipes()
    rec = Recommender(recipes)

    lunch = rec.recommend(people=2, scene="workday", prefer_categories=["meat_dish", "aquatic", "vegetable_dish"])
    dinner = rec.recommend(people=2, scene="workday", prefer_categories=["soup", "vegetable_dish"])
    dinner = [r for r in dinner if r["name"] not in set(r["name"] for r in lunch)]

    breakfast = [r for r in recipes if r.get("category") == "breakfast"]

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    season_cn = {"spring": "春", "summer": "夏", "autumn": "秋", "winter": "冬"}
    season = season_cn.get(rec._get_season(), "冬")

    lines = [
        f"示例 8：一日三餐推荐",
        "=" * 50,
        f"日期: {today} | 季节: {season}季 | 人数: 2 人",
        "",
    ]

    # 早餐
    lines.append("☀️ 早餐")
    lines.append("-" * 30)
    if breakfast:
        for r in breakfast[:2]:
            n = r.get("nutrition", {})
            lines.append(f"  - {r['name']}")
            lines.append(f"    卡路里: {n.get('calories', '?')}kcal | 预计时间: {r.get('cooking_time_min', '?')}-{r.get('cooking_time_max', '?')} 分钟")
    else:
        lines.append("  - 暂无早餐菜谱，建议：牛奶 + 鸡蛋 + 全麦面包")
    lines.append("")

    # 午餐
    lines.append("🌤️ 午餐（工作日快手菜）")
    lines.append("-" * 30)
    for i, r in enumerate(lunch[:3], 1):
        n = r.get("nutrition", {})
        lines.append(f"  {i}. {r['name']}")
        lines.append(f"     卡路里: {n.get('calories', '?')}kcal | {r.get('category_cn', '?')} | 难度: {'★' * r.get('difficulty', 1)}")
    lines.append("")

    # 晚餐
    lines.append("🌙 晚餐（清淡搭配）")
    lines.append("-" * 30)
    for i, r in enumerate(dinner[:3], 1):
        n = r.get("nutrition", {})
        lines.append(f"  {i}. {r['name']}")
        lines.append(f"     卡路里: {n.get('calories', '?')}kcal | {r.get('category_cn', '?')} | 难度: {'★' * r.get('difficulty', 1)}")
    lines.append("")

    # 购物清单
    all_recipes = (breakfast[:1] if breakfast else []) + lunch[:3] + dinner[:3]
    if all_recipes:
        shopping = rec.generate_shopping_list(all_recipes)
        lines.append(shopping)

    write_example("08_daily_meals.txt", "\n".join(lines))


def example_9_low_fat():
    """示例 9: 低脂餐推荐"""
    recipes = load_recipes()
    rec = Recommender(recipes)

    result = rec.recommend(people=2, diet_mode="low_fat", max_spiciness=0)
    card = rec.generate_menu_card(result, people=2)

    title = "示例 9：低脂餐推荐（不辣）"
    content = f"{title}\n{'=' * 50}\n\n{card}"
    write_example("09_low_fat.txt", content)


def example_10_search():
    """示例 10: 搜索菜谱"""
    recipes = load_recipes()

    lines = [
        "示例 10：搜索菜谱",
        "=" * 50,
        "",
    ]

    for keyword in ["鸡", "鱼", "豆腐"]:
        matches = [r for r in recipes if keyword in r["name"]]
        lines.append(f"搜索关键词: '{keyword}' (找到 {len(matches)} 道)")
        lines.append("-" * 30)
        for r in matches[:5]:
            n = r.get("nutrition", {})
            lines.append(f"  - {r['name']} | {r.get('category_cn')} | 难度:{r.get('difficulty')}星 | {n.get('calories', '?')}kcal")
        if len(matches) > 5:
            lines.append(f"  ... 还有 {len(matches) - 5} 道")
        lines.append("")

    write_example("10_search.txt", "\n".join(lines))


def main():
    print("智能烹饪技能 - 核心功能示例演示")
    print("=" * 50)
    print()

    examples = [
        ("智能推荐菜单卡片", example_1_menu_card),
        ("菜谱详情（分量估算）", example_2_recipe_detail),
        ("菜谱详情（原始有分量）", example_3_recipe_detail_with_amount),
        ("购物清单（分类展示）", example_4_shopping_list),
        ("食材反推", example_5_ingredient_search),
        ("营养信息查询", example_6_nutrition_info),
        ("烹饪教程", example_7_tutorials),
        ("一日三餐推荐", example_8_daily_meals),
        ("低脂餐推荐", example_9_low_fat),
        ("搜索菜谱", example_10_search),
    ]

    for name, func in examples:
        print(f"运行: {name}")
        try:
            func()
        except Exception as e:
            print(f"  -> 失败: {e}")
        print()

    print("=" * 50)
    print(f"所有示例已输出到: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
