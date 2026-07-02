# 知乎盐选故事创作工作区

知乎盐选短篇小说创作项目，包含知识库、故事稿件与 Cursor Agent Skills。

## 目录结构

- `knowledge-base/` — 盐选创作知识库（平台规则、结构模板、钩子、文风等）
- `stories/` — 按日期+标题归档的故事稿件
- `.cursor/skills/` — Cursor Agent Skills
  - `yanxuan-story-writer` — 盐选爆款短篇创作规范
  - `story-workspace` — 故事工作区管理与字数门禁

## 使用方式

在 Cursor 中打开本项目，Agent 会自动加载 `.cursor/skills/` 下的技能文件，配合 `knowledge-base/` 进行选题、大纲与逐章创作。
