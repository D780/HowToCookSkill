# 智能烹饪技能

基于 [HowToCook](https://github.com/Anduin2017/HowToCook) 构建的智能菜谱推荐系统。

## 功能

- 智能推荐 - 按人数、场景、季节、饮食模式推荐搭配
- 营养查询 - 卡路里、蛋白质、碳水、脂肪信息
- 辣度标注 - 0-5 级辣度标识
- 购物清单 - 自动生成采购清单
- 食材反推 - 根据家中食材推荐可做的菜
- 自动同步 - 定期从 HowToCook 更新菜谱

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 构建菜谱索引（首次使用）

```bash
python chef_skill.py build
```

### 推荐今天吃什么（2人份）

```bash
python chef_skill.py recommend --people 2
```

### 推荐 + 购物清单

```bash
python chef_skill.py recommend --people 3 --shopping-list
```

### 低脂餐推荐

```bash
python chef_skill.py recommend --diet low_fat --no-spicy
```

### 搜索菜谱

```bash
python chef_skill.py search 宫保
```

### 查看菜谱详情（含做法）

```bash
python chef_skill.py detail 宫保鸡丁
```

### 查看营养信息

```bash
python chef_skill.py nutrition 西红柿炒鸡蛋
```

### 根据食材反推

```bash
python chef_skill.py ingredients 鸡蛋 西红柿 豆腐
```

### 同步最新菜谱

```bash
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
今日推荐（3 人份）
========================================

1. 黔式腊肠娃娃菜
   卡路里: 0.0kcal | 蛋白质: 0.0g | 碳水: 0.0g | 脂肪: 0.0g
   难度: 1星 | 预计时间: 5-15 分钟
   类型: 荤菜 | 不辣 | 口味: 快手/清淡

2. 西葫芦炒鸡蛋
   卡路里: 1043.0kcal | 蛋白质: 13.3g | 碳水: 2.8g | 脂肪: 108.8g
   难度: 2星 | 预计时间: 15-25 分钟
   类型: 素菜 | 不辣 | 口味: 快手/清淡
```

### 菜谱详情

```
【西葫芦炒鸡蛋】
========================================
难度: 2星 | 辣度: 不辣 | 卡路里: 1043.0kcal/份
预计时间: 15-25 分钟
类型: 素菜

食材（2 人份）：
  - 西葫芦
  - 鸡蛋
  - 西红柿（可选）
  - 食用盐
  - 食用油

步骤：
  1. 西红柿洗净，切成小块，备用
  2. 西葫芦洗净，切成边长约为 4cm 的菱形，备用
  3. 打三个鸡蛋到碗里，打散搅匀，备用
  4. 热锅，锅内放入 5ml - 10ml 食用油
  ...
```

## 推荐策略

### 按人数搭配
- 1-2 人：2 道菜（荤 + 素）
- 3-4 人：4 道菜（荤 + 素 + 汤 + 主食）
- 5-6 人：6 道菜（多荤 + 多素 + 汤 + 甜品/饮料）

### 季节性推荐
- 春：清淡、时令蔬菜
- 夏：凉拌、清蒸、冷菜
- 秋：润燥、煲汤
- 冬：炖菜、红烧、热汤

### 菜品去重
推荐时自动避免主要食材重复，不会同时推荐两道都用大量相同主料的菜。

## 定时同步

可通过 crontab 设置每周同步：

```
0 8 * * 1 cd /path/to/cooking-skill && python chef_skill.py sync >> /dev/null 2>&1
```

## 营养数据来源

营养数据基于公开营养数据库整理，为估算值，仅供参考。

## 运行测试

```bash
python -m pytest tests/ -v
```
