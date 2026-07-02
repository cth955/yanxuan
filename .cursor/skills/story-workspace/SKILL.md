---
name: story-workspace
description: >-
  在本项目（zhihuyanxuan）中管理盐选故事创作的工作区：在 stories/ 下按日期+标题建文件夹、逐章写入文件、强制字数达标。
  仅在用户已明确确认开始创作之后使用（如「确认开始创作」「开始写」「开写」「按大纲写第1章」）。
  不要在选题碰撞、方案 Pitch、或未获用户确认时启用。
disable-model-invocation: true
---

# 故事工作区管理

本 Skill **仅适用于本项目**，负责把创作成果落到 `stories/` 目录，并强制执行字数门禁。

写作风格与情节规范仍遵循 `yanxuan-story-writer` 与 `knowledge-base/`；本 Skill 只管**何时建目录、写什么文件、字数怎么验**。

---

## 启用条件（必须全部满足）

1. 当前工作区是 `zhihuyanxuan` 项目（存在 `stories/` 与 `knowledge-base/`）
2. 用户**已明确确认**进入创作阶段，例如：
   - 「确认开始创作」「开始写」「开写」「写大纲」「写第 X 章」
   - 用户选定方案后说「就这个，开始」
3. **未确认前禁止**：不得提前建文件夹、不得写 chapter 文件

若用户仍在讨论选题或方案 → 只输出对话内容，**不**启用本 Skill。

---

## Step 1：创建工作目录

用户确认开始创作后，**第一件事**是建目录：

```
stories/YYYY-MM-DD-[故事标题]/
```

### 命名规则

| 部分 | 格式 | 示例 |
|------|------|------|
| 日期 | 当天日期 `YYYY-MM-DD` | `2026-06-24` |
| 标题 | 用户确认的故事名，去掉非法字符 | `深渊回响` |
| 完整路径 | 日期与标题用 `-` 连接 | `stories/2026-06-24-深渊回响/` |

- 标题中的 `/ \ : * ? " < > |` 替换为 `-`
- 空格保留或改为 `-`，同一故事内保持一致
- 若目录已存在（同日同题），继续写入该目录，不重复创建

### 初始文件

建目录后立即创建：

| 文件 | 时机 | 说明 |
|------|------|------|
| `outline.md` | 写大纲阶段 | 章节规划、目标字数、付费墙/A级反转标注 |
| `synopsis.md` | 有大纲后 | 300-500 字投稿梗概（可后补） |
| `checklist.md` | 开写前 | 从 `knowledge-base/10-workflow-and-checklist.md` 复制终检表头 |

---

## Step 2：逐章写入文件

### 文件命名（默认：一章一文件）

```
chapter-01.md
chapter-02.md
...
chapter-12.md
```

- 文件名用两位数字：`chapter-03.md` 而非 `chapter-3.md`
- 每章文件开头写标题行：`# 第 X 章：[章节名]`
- **禁止**只在聊天里输出正文而不写文件；每章完成后必须 `Write` 到对应路径

### 分批交付

用户要求「先写 1-4 章」时，仍按单章文件写入（`chapter-01.md` … `chapter-04.md`），不要合并成 `chapter-01-04.md`，除非用户明确要求合并格式。

---

## Step 3：字数标准（硬性门禁）

标准来源：`knowledge-base/02-structure-templates.md` 与 `knowledge-base/10-workflow-and-checklist.md`。

### 全篇

| 指标 | 要求 |
|------|------|
| 章节数 | 8-15 章 |
| 单章字数 | 800-2500 字；常规目标 **1200-1500 字** |
| 全文合计 | **≥ 12000 字**（大纲规划建议 ≥ 13000 留 buffer） |
| 单章下限 | 低于目标字数 **80%** → 必须回炉扩充 |

### 每章写完后的必做流程

1. 将正文写入 `chapter-XX.md`
2. 运行字数校验（见下方命令）
3. 未达标 → **在同一轮内扩充后覆盖写入**，不得交付未达标章节
4. 在 `checklist.md` 或 `outline.md` 更新该章「目标 / 实际 / 达标」记录

### 字数不够时的扩充（合规）

✅ 增加对话、1-2 个感官细节、简短内心活动、与主线相关的小场景  
❌ 灌水重复、无意义景物铺垫

---

## Step 4：字数校验命令

每章写入后执行：

```bash
python .cursor/skills/story-workspace/scripts/count-chars.py stories/YYYY-MM-DD-[标题]/chapter-XX.md --target 1500
```

批量检查整个故事目录：

```bash
python .cursor/skills/story-workspace/scripts/count-chars.py stories/YYYY-MM-DD-[标题]/ --min-total 12000
```

- `--target N`：单章目标字数（默认 1500）
- `--min-total N`：全文最低字数（默认 12000）
- 脚本统计**正文汉字**（去掉 Markdown 标记后），与盐选「字数」口径一致
- 退出码非 0 表示未达标 → 继续扩充，直到通过

---

## Step 5：合并与终稿（全文完成后）

全部章节达标后：

1. 合并为 `full-text.md`（按章节顺序拼接，保留各章标题）
2. 再次运行 `--min-total 12000` 核验
3. 完善 `synopsis.md` 与 `checklist.md`
4. 告知用户目录路径与各章字数摘要

---

## 目录结构速查

```
stories/
  YYYY-MM-DD-[故事标题]/
    outline.md
    chapter-01.md
    chapter-02.md
    ...
    full-text.md      # 全部章节达标后合并
    synopsis.md
    checklist.md
```

---

## 与创作流程的衔接

| 阶段 | 是否启用本 Skill | 动作 |
|------|------------------|------|
| 选题 / 3 方案 Pitch | ❌ | 仅对话，不建目录 |
| 用户确认方案 | ✅ | 建目录 + 写 `outline.md` |
| 逐章写作 | ✅ | 写 `chapter-XX.md` + 字数校验 |
| 润色 / 拆文 / 讨论 | ❌ 除非用户说开写 | 不新建 chapter |

---

## 回复用户时的习惯

- 每章交付：说明文件路径 + 实际字数 + 是否达标
- 未达标：明确差多少字，扩充后再报告
- 不要问「要不要保存到文件」——**默认必须保存**
