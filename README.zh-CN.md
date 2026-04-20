<div align="center">

# Research Innovation Explorer

**一个宿主中立、搜索优先的研究创新点探索技能，用于文献驱动的 idea 发现、理论包装与高质量 Markdown 报告生成。**

[English README](./README.md)

[![GitHub stars](https://img.shields.io/github/stars/foryourhealth111-pixel/research-innovation-explorer?style=flat-square)](https://github.com/foryourhealth111-pixel/research-innovation-explorer)
[![GitHub repo size](https://img.shields.io/github/repo-size/foryourhealth111-pixel/research-innovation-explorer?style=flat-square)](https://github.com/foryourhealth111-pixel/research-innovation-explorer)
![宿主中立](https://img.shields.io/badge/宿主中立-host--neutral-111827?style=flat-square)
![搜索优先](https://img.shields.io/badge/搜索优先-search--first-0f766e?style=flat-square)
![报告输出](https://img.shields.io/badge/报告输出-Markdown%20%2B%20可视化-7c3aed?style=flat-square)

</div>

## 这个仓库解决什么问题

很多“找创新点”的流程会卡在三件事上：

- 只靠印象找论文，没有系统检索
- 能拼组合，但讲不清为什么这个组合成立
- 做完分析后没有形成可读、可分享、可追溯的报告

`research-innovation-explorer` 的设计目标，就是把这三件事接起来：

1. 先做系统搜索，再做判断。
2. 把论文拆成可复用能力，而不是只看标题。
3. 生成并筛选组合候选。
4. 对最强候选做诚实的理论表达。
5. 最终输出一份优雅的 Markdown 报告，包含参考文献、分析依据和可视化摘要。

## 核心方法学

这个技能围绕一条非常明确的研究生产链条展开：

1. 先收集大约 40 篇最新的、顶会的、Oral 级别的、开源的、业界认可的优质论文。
2. 以这些论文为基础，建立一个方向敏感的 `40 x 40` 组合矩阵。
3. 去掉自己和自己的对角线组合，保留剩余的 `40 x 39 = 1560` 种 `A + B` 可能。
4. 对这 1560 个候选做快速逻辑验证、轻量实验验证，以及有针对性的搜索补充。
5. 基于搜索到的信息和验证结果，把空间收缩到大约 15 个真正靠谱、能跑通、值得继续推进的 Idea。

这不是工作流边缘上的一个小技巧，而是整个技能的操作核心。重点不是等待“灵光一现”，而是先做足搜索，再强制组合，再快速验证，最后只保留那些经得起信息和证据筛选的少数候选。

| 阶段 | 要做什么 | 产出什么 |
| --- | --- | --- |
| 论文池 | 收集约 40 篇有代码、有影响力的近期强论文 | 一份可复用的能力清单 |
| 组合阶段 | 穷举 `40 x 40` 空间并移除自组合 | 1560 个方向敏感的 `A + B` 候选 |
| 快速验证 | 搜索相关工作、检查代码、做快速逻辑判断或最小实验 | 一批更现实的可行选项 |
| 最终筛选 | 只保留兼具新颖性、逻辑一致性和可实现性的组合 | 大约 15 个可推进的 Idea |

## 你会得到什么

| 层级 | 作用 |
| --- | --- |
| `SKILL.md` | 定义完整流程、判断规则与交付要求 |
| `scripts/build_search_queries.py` | 生成主题扫描、新颖性检查、失败分析等查询包 |
| `scripts/build_idea_matrix.py` | 从论文池生成组合候选矩阵并评分 |
| `scripts/build_markdown_report.py` | 生成带 Mermaid 图、证据表和参考文献的 Markdown 报告草稿 |
| `references/` | 放置搜索手册、理论表达规则、报告规范和边界约束 |
| `assets/templates/` | 提供搜索日志、论文池、idea brief、实验计划和报告模板 |

## 工作流

```mermaid
flowchart LR
    A[搜索阶段] --> B[论文池]
    B --> C[能力拆解]
    C --> D[组合矩阵]
    D --> E[候选筛选]
    E --> F[理论表达]
    F --> G[实验设计]
    G --> H[Markdown 报告]
```

## 设计原则

### 1. 搜索优先

只要当前环境具备搜索能力，就不应该仅凭记忆去做“最新文献”判断。

### 2. 理论表达要诚实

这个技能支持统一框架、极端特例、控制变量等写法，但前提是这些表达真的能被定义、解释和验证。

### 3. 报告要带证据

最终输出的 Markdown 文档不只是“结论合集”，而是必须包含：

- 参考文献
- 分析依据
- 候选比较
- 可视化摘要

### 4. 宿主中立

这里沉淀的是工作流本身，而不是某一个 agent 平台的专属写法。无论是支持 Skills 的宿主，还是手工执行，都可以复用。

## 快速开始

### 1. 先生成查询包

```bash
python scripts/build_search_queries.py \
  --topic "long-context reasoning" \
  --keywords "memory routing, verifier head, benchmark"
```

### 2. 准备论文池

从这些模板开始：

- `assets/templates/search-log.csv`
- `assets/templates/paper-pool.csv`

### 3. 生成组合矩阵

```bash
python scripts/build_idea_matrix.py \
  assets/templates/paper-pool.csv \
  --output work/idea-matrix.csv
```

### 4. 生成 Markdown 报告

```bash
python scripts/build_markdown_report.py \
  --topic "Long-Context Reasoning" \
  --paper-pool assets/templates/paper-pool.csv \
  --idea-matrix work/idea-matrix.csv \
  --search-log assets/templates/search-log.csv \
  --output work/report.md
```

## 输出风格

报告层默认采用 GitHub 友好的视觉结构：

- Mermaid 流程图，用来解释流程与逻辑
- LaTeX 矩阵热力图，用来概览候选筛选结果
- Mermaid 饼图，用来快速展示分布
- Markdown 证据表，用来承载“分析依据”
- 简洁段落，用来承载 summary 和 detailed analysis

这样既适合工作中快速阅读，也适合作为可分享的研究 memo。

## 使用示例

### 综述文献矩阵

下面这个示例直接使用 README 原生的 LaTeX 热力矩阵来表达筛选结果。它展示的是一个 `40 x 40` 方向敏感综述矩阵的局部放大图：对角线位置表示自组合，已被屏蔽；颜色越深表示 `A + B` 组合潜力越强；金色描边表示那些经过搜索和快速验证之后进入 shortlist 的候选。

```math
\begin{array}{c|cccccccc}
 & P01 & P02 & P03 & P04 & P05 & P06 & P07 & P08 \\
\hline
P01 & \bbox[#D7D3CC,4px]{\phantom{0.00}} & \bbox[#EAF5F2,4px]{0.41} & \bbox[#BEE4DC,4px]{0.58} & \bbox[#EAF5F2,4px]{0.37} & \bbox[#0F766E,4px]{\color{white}{0.86}} & \bbox[#BEE4DC,4px]{0.61} & \bbox[#EAF5F2,4px]{0.44} & \bbox[#72C6B5,4px]{0.72} \\
P02 & \bbox[#BEE4DC,4px]{0.63} & \bbox[#D7D3CC,4px]{\phantom{0.00}} & \bbox[#EAF5F2,4px]{0.48} & \bbox[#72C6B5,4px]{0.74} & \bbox[#0F766E,4px,border:2px solid #C0841A]{\color{white}{0.92}} & \bbox[#EAF5F2,4px]{0.39} & \bbox[#BEE4DC,4px]{0.64} & \bbox[#0F766E,4px]{\color{white}{0.84}} \\
P03 & \bbox[#EAF5F2,4px]{0.36} & \bbox[#BEE4DC,4px]{0.59} & \bbox[#D7D3CC,4px]{\phantom{0.00}} & \bbox[#BEE4DC,4px]{0.62} & \bbox[#EAF5F2,4px]{0.40} & \bbox[#72C6B5,4px]{0.73} & \bbox[#0F766E,4px]{\color{white}{0.83}} & \bbox[#EAF5F2,4px]{0.45} \\
P04 & \bbox[#BEE4DC,4px]{0.55} & \bbox[#EAF5F2,4px]{0.43} & \bbox[#72C6B5,4px]{0.71} & \bbox[#D7D3CC,4px]{\phantom{0.00}} & \bbox[#0F766E,4px]{\color{white}{0.87}} & \bbox[#EAF5F2,4px]{0.38} & \bbox[#BEE4DC,4px]{0.57} & \bbox[#72C6B5,4px]{0.76} \\
P05 & \bbox[#0F766E,4px,border:2px solid #C0841A]{\color{white}{0.89}} & \bbox[#BEE4DC,4px]{0.60} & \bbox[#EAF5F2,4px]{0.42} & \bbox[#72C6B5,4px]{0.70} & \bbox[#D7D3CC,4px]{\phantom{0.00}} & \bbox[#0F766E,4px]{\color{white}{0.85}} & \bbox[#BEE4DC,4px]{0.56} & \bbox[#EAF5F2,4px]{0.34} \\
P06 & \bbox[#EAF5F2,4px]{0.47} & \bbox[#0F766E,4px]{\color{white}{0.82}} & \bbox[#BEE4DC,4px]{0.65} & \bbox[#EAF5F2,4px]{0.46} & \bbox[#72C6B5,4px]{0.75} & \bbox[#D7D3CC,4px]{\phantom{0.00}} & \bbox[#0F766E,4px]{\color{white}{0.81}} & \bbox[#BEE4DC,4px]{0.54} \\
P07 & \bbox[#BEE4DC,4px]{0.52} & \bbox[#EAF5F2,4px]{0.41} & \bbox[#0F766E,4px]{\color{white}{0.84}} & \bbox[#BEE4DC,4px]{0.58} & \bbox[#EAF5F2,4px]{0.49} & \bbox[#72C6B5,4px]{0.72} & \bbox[#D7D3CC,4px]{\phantom{0.00}} & \bbox[#0F766E,4px,border:2px solid #C0841A]{\color{white}{0.87}} \\
P08 & \bbox[#72C6B5,4px]{0.71} & \bbox[#BEE4DC,4px]{0.53} & \bbox[#EAF5F2,4px]{0.44} & \bbox[#0F766E,4px]{\color{white}{0.83}} & \bbox[#BEE4DC,4px]{0.60} & \bbox[#EAF5F2,4px]{0.43} & \bbox[#72C6B5,4px]{0.74} & \bbox[#D7D3CC,4px]{\phantom{0.00}}
\end{array}
```

图例说明：
- 灰色对角线：自组合，直接移除
- 绿色从浅到深：组合潜力从弱到强
- 金色描边：经过搜索支撑和快速验证后进入 shortlist 的候选

如果你希望最终 Markdown 报告不只是“列一个候选清单”，而是能让读者一眼看懂筛选逻辑，就应该把这种 LaTeX 原生矩阵图和证据表一起放进去。

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── templates/
├── references/
└── scripts/
```

## 适用场景

- 挖掘增量但可辩护的研究创新点
- 在真正动手实现之前，先把文献图谱拉清楚
- 检查某个 A+B 组合是否已经在论文或代码里出现过
- 输出一份高质量、带引用、带可视化的研究分析文档
- 训练文献检索、方法抽象、实验设计和研究写作能力

## 文档入口

- 主流程：[`SKILL.md`](./SKILL.md)
- 搜索手册：[`references/search-playbook.md`](./references/search-playbook.md)
- 理论表达：[`references/framing-and-theory.md`](./references/framing-and-theory.md)
- 报告规范：[`references/reporting-and-visualization.md`](./references/reporting-and-visualization.md)
- 报告模板：[`assets/templates/analysis-report-template.md`](./assets/templates/analysis-report-template.md)

## 说明

- 如果宿主不能渲染 Mermaid，就保留 Markdown 表格，并把 Mermaid 替换成静态图片或纯文本摘要。
- 如果当前环境没有搜索能力，可以手工执行这套流程，但应明确降低对“当前文献结论”的置信度。

## 社区

如果你希望参与更广泛的工具、工作流和 AI 原生构建讨论，可以访问 [linux.do](https://linux.do/)。
