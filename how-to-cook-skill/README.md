# How to Cook Skill

智能烹饪技能，基于 [HowToCook](https://github.com/Anduin2017/HowToCook) 构建。

## 功能

- 智能推荐 - 按人数、场景、季节、饮食模式推荐搭配
- 营养查询 - 卡路里、蛋白质、碳水、脂肪信息
- 辣度标注 - 0-5 级辣度标识
- 购物清单 - 自动生成采购清单
- 食材反推 - 根据家中食材推荐可做的菜
- 烹饪教程 - 焯水、蒸、炒煎、油温判断等技法教学
- 自动同步 - 定期从 HowToCook 更新菜谱和教程

---

## 安装

### 方式一：独立使用

```bash
# 进入技能目录
cd how-to-cook-skill

# 安装依赖
pip install -r requirements.txt

# 首次使用，构建索引（从 GitHub 抓取菜谱和教程）
python chef_skill.py build
```

### 方式二：作为 AI Agent 技能安装

本技能符合 [superpowers](https://github.com/obra/superpowers) 规范，可通过以下方式安装：

```bash
# 克隆到 skills 目录
git clone <repo-url> skills/how-to-cook-skill
cd skills/how-to-cook-skill
pip install -r requirements.txt
python chef_skill.py build
```

AI Agent 会自动读取 `SKILL.md` 识别该技能，并在检测到烹饪相关意图时触发。

---

## 使用

### CLI 命令行模式

#### 推荐菜式

```bash
# 2 人份推荐
python chef_skill.py recommend --people 2

# 3 人份 + 购物清单（适合准备去买菜）
python chef_skill.py recommend --people 3 --shopping-list

# 低脂餐 + 不吃辣
python chef_skill.py recommend --diet low_fat --no-spicy

# 工作日快手菜
python chef_skill.py recommend --scene workday

# 根据家中食材推荐
python chef_skill.py recommend --ingredients 鸡蛋 豆腐 --people 2
```

#### 搜索菜谱

```bash
python chef_skill.py search 宫保
```

#### 菜谱详情（含做法）

```bash
python chef_skill.py detail 宫保鸡丁
python chef_skill.py detail 宫保鸡丁 --servings 4
```

#### 营养信息

```bash
python chef_skill.py nutrition 宫保鸡丁
```

#### 食材反推

```bash
python chef_skill.py ingredients 鸡蛋 西红柿 豆腐
```

#### 烹饪教程

```bash
# 列出所有教程
python chef_skill.py tutorial

# 查看具体教程
python chef_skill.py tutorial 焯水
python chef_skill.py tutorial 油温
python chef_skill.py tutorial 蒸
python chef_skill.py tutorial 炒
```

#### 同步更新

```bash
python chef_skill.py sync
```

### AI 对话模式

安装为 AI Agent 技能后，直接用自然语言对话：

| 你说 | AI 触发 |
|------|---------|
| "今天吃什么" | 推荐菜式，会主动询问用餐人数、偏好等 |
| "想吃点简单的" | 推荐快手菜 |
| "想吃低卡的" | 低脂模式推荐 |
| "宫保鸡丁怎么做" | 展示菜谱详情和做法步骤 |
| "宫保鸡丁多少卡路里" | 展示营养信息 |
| "家里有鸡蛋豆腐能做什么" | 食材反推 |
| "怎么焯水" | 展示焯水教程 |
| "炒和煎有什么区别" | 展示相关烹饪技法教程 |
| "推荐几个菜我要去买菜" | 推荐 + 购物清单 |

---

## 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `recommend` | 智能推荐 | `recommend --people 3 --shopping-list` |
| `search` | 搜索菜谱 | `search 宫保` |
| `detail` | 菜谱详情 | `detail 宫保鸡丁 --servings 4` |
| `nutrition` | 营养查询 | `nutrition 西红柿炒鸡蛋` |
| `ingredients` | 食材反推 | `ingredients 鸡蛋 西红柿` |
| `tutorial` | 烹饪教程 | `tutorial 焯水` |
| `build` | 构建索引 | `build` |
| `sync` | 同步更新 | `sync` |

### 推荐选项

| 选项 | 说明 |
|------|------|
| `--people N` | 用餐人数（影响搭配数量） |
| `--scene workday/weekend` | 场景（工作日推荐快手菜） |
| `--diet low_fat` | 低脂模式 |
| `--no-spicy` | 不吃辣 |
| `--low-cal` | 低卡路里 |
| `--ingredients A B` | 家中食材列表 |
| `--shopping-list` | 生成购物清单 |

---

## 目录结构

```
how-to-cook-skill/
├── SKILL.md              # AI Agent 技能描述文件
├── chef_skill.py         # CLI 入口脚本
├── requirements.txt      # Python 依赖
├── README.md             # 使用说明
├── scripts/              # 核心模块
│   ├── index_builder.py      # 索引构建（菜谱 + 教程抓取）
│   ├── recommender.py        # 推荐引擎
│   ├── nutrition_calculator.py  # 营养计算
│   ├── ingredient_matcher.py    # 食材匹配与反推
│   └── recipe_sync.py          # 同步服务
├── data/                 # 数据文件
│   ├── recipes_index.json    # 菜谱索引
│   ├── tutorials_index.json  # 教程索引
│   ├── nutrition_db.json     # 营养数据库
│   ├── ingredient_aliases.json  # 食材别名映射
│   └── user_preferences.json  # 用户偏好
└── tests/                # 测试用例
```

---

## 推荐策略

### 按人数搭配
- 1-2 人：2 道菜
- 3-4 人：4 道菜
- 5-6 人：6 道菜

### 季节性调整
自动根据当前月份调整推荐：
- 春：清淡、时令蔬菜
- 夏：凉拌、清蒸
- 秋：润燥、煲汤
- 冬：炖菜、红烧、热汤

### 低脂餐
过滤高脂肪食材（五花肉、油炸类），优先蒸/煮/凉拌做法。

### 菜品去重
避免推荐主要食材重复的菜式（如不会同时推荐两道都用大量鸡蛋的菜）。

---

## 烹饪教程体系

教程文档来自 HowToCook 仓库的 tips/ 目录，涵盖：

### 基础指南
- 厨房准备 - 厨房必备工具、调料等
- 如何选择现在吃什么 - 决策帮助

### 烹饪技法 (tips/learn/)
- 学习焯水、学习炒与煎、学习蒸、学习煮、学习凉拌、学习腌
- 高压力锅、空气炸锅、微波炉、去腥

### 高级技巧 (tips/advanced/)
- 辅料技巧、糖色的炒制、油温判断技巧、高级专业术语

---

## 定时同步

可通过 crontab 设置每周同步更新：

```
0 8 * * 1 cd /path/to/how-to-cook-skill && python chef_skill.py sync >> /dev/null 2>&1
```

---

## 营养数据来源

营养数据基于公开营养数据库整理，为估算值，仅供参考。辣度通过食材关键词推断（0-5 级）。

---

## 运行测试

```bash
python -m pytest tests/ -v
```
