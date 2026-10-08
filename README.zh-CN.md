<p align="center">
  <a href="README.md">English</a> · <strong>简体中文</strong> · <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <img src="assets/hero.png" alt="IPCC Plotting Style — 以可追溯的来源支撑气候科学绘图" width="100%">
</p>

<h1 align="center">IPCC Plotting Style</h1>
<p align="center"><strong>以来源可追溯的视觉语言，呈现气候研究。</strong></p>
<p align="center">
  <a href="https://github.com/GISWLH/IPCC/actions/workflows/checks.yml"><img src="https://github.com/GISWLH/IPCC/actions/workflows/checks.yml/badge.svg" alt="检索与示例验证状态"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-173c66" alt="检索需要 Python 3.10 或更新版本">
  <img src="https://img.shields.io/badge/Retrieval-offline-287d7d" alt="离线检索">
  <a href="https://github.com/GISWLH/IPCC/stargazers"><img src="https://img.shields.io/github/stars/GISWLH/IPCC?style=flat&color=d98725" alt="GitHub 星标数"></a>
</p>

<p align="center">
  <a href="#overview">项目概览</a> · <a href="#quick-start">快速开始</a> · <a href="#gallery">示例展示</a> · <a href="#method">方法说明</a> · <a href="CONTRIBUTING.md">参与贡献</a>
</p>

<a id="overview"></a>
## 项目概览

**IPCC Plotting Style 将 IPCC 第一工作组公开绘图代码中的视觉规范，转化为可复用的科学可视化工作流程。** 项目整合本地证据库、专题风格指南与可运行示例，帮助研究者有依据地选择配色、版式、情景表达与不确定性呈现方式。

项目适用于 Codex、Claude，也可直接通过命令行使用，重点支持降水、径流、干旱、区域水资源压力及集合比较等研究场景。检索结果保留来源信息；展示图均可用小规模合成数据重新生成。

| 证据基础 | 可核验的覆盖范围 |
|---|---:|
| 上游代码仓库 | **135** |
| 明确命名的图件目标¹ | **122** |
| 已索引的代码与 Notebook 记录 | **3,465** |
| 绘图类别 | **9** |

¹ 这 122 个目标依据 **121 个图件专题仓库的名称**推导而来：包含多幅图的编号被展开，同一图的不同面板被合并。其中，**65 个目标关联的仓库包含已打包代码**；其余 57 个目标在对应专题仓库中仅有引用或元数据证据。整章仓库还提供其他材料。这些数字不代表完整复现了相应图件，也不是已研读论文的数量。完整映射与统计边界见[语料审计及计数规则](docs/corpus-methodology.md)（英文）。

**本地运行，无需外部服务。** 检索仅使用 Python 标准库，不需要 API 密钥、向量嵌入服务或数据库。本项目由社区独立维护，与 IPCC 无隶属关系，亦未获其官方背书。

<a id="quick-start"></a>
## 快速开始

检索需要 Python **3.10+**；可选绘图示例已在 Python **3.12** 环境中验证。

```bash
git clone https://github.com/GISWLH/IPCC.git
cd IPCC

# 检索本地可用代码及其来源；无需安装依赖。
python scripts/search_ipcc_examples.py "scenario uncertainty" --family time_series --limit 3
python scripts/search_ipcc_examples.py "stippling" --family map --json
```

主命令为每个本地可用源文件返回匹配度最高的代码片段，并提供上游仓库、原始路径、提交标识和规范化本地路径。`--json` 输出 JSONL；`--all-types` 还会返回未打包输入数据、文档及输出图件的引用。

需要更细的筛选时：

```bash
python scripts/ipcc_rag_search.py "uncertainty" --repo Chapter-11 --source-only --unique-files
```

在助手中使用时，可通过其技能安装机制将本仓库注册为 `ipcc-plotting-style`，或直接让助手读取 [SKILL.md](SKILL.md)。复制技能时，请将 `scripts/` 和 `references/` 与该文件一并保留。

> “绘制降水变化地图，使用以零为中心的发散色标，并以点状标记表示低一致性区域。先检索 IPCC 源码示例，解释视觉设计选择，再注明原始代码来源。”

<a id="gallery"></a>
## 可复现示例

**以下数值均为合成数据。** 示例用于展示绘图规范，不代表 IPCC 的科学结论或预测。

### 01 · 情景轨迹与不确定性

中位数轨迹与 5–95% 集合区间同时呈现中心趋势和离散程度；统一的情景配色便于跨图比较。

![合成情景轨迹与不确定性区间](assets/demos/scenarios.png)

### 02 · 空间变化与一致性

Robinson 投影、以零为中心的发散色标和点状标记共同表达空间格局及其限定条件。一致性掩膜采用示意规则，不构成统计评估。

![合成降水变化地图及示意性低一致性标记](assets/demos/precipitation.png)

### 03 · 区域集合分布

分组箱线图比较四个区域与三种情景。箱体表示四分位距，须线采用 5–95% 分位范围，范围外的值不显示。

![不同情景下的合成区域径流分布](assets/demos/ensembles.png)

建议在虚拟环境中安装可选绘图依赖，然后生成全部示例：

```bash
python -m pip install -r requirements-demo.txt
python examples/generate.py
```

`results/demos/` 中包含 PNG/PDF 图件和记录实际合成数组、随机种子、依赖版本及风格参考来源的清单。添加 `--formats png pdf svg` 可导出 SVG。项目内置经过校验的小型 Natural Earth 陆地边界数据，绘图时无需联网下载。详见[示例指南](examples/README.md)（英文）。

<a id="method"></a>
## 从来源证据到可运行图件

| 阶段 | 技术方法 | 作用 |
|---|---|---|
| 源码打包 | 筛选脚本、仅保留代码的 Notebook 及 Python 导出文件 | 无需大型气候数据集即可检查绘图实现 |
| 结构化索引 | 带有仓库、路径、提交和类别标签的 JSONL 片段 | 保留可追溯的来源关联 |
| 类别路由 | 九类绘图任务与凝练的证据指南 | 将可视化需求对应到相关设计规范 |
| 本地检索 | 按文档长度归一化的词项评分、路径与类别加权、文件级去重 | 优先提供可在本地查阅的代码 |
| 适配与验证 | 源码阅读、合成数据绘图及来源清单 | 将设计规范转化为可运行、可审查的示例 |

当前实现采用**关键词检索**，不使用向量嵌入或模型微调。建议使用 `fill_between`、`boxplot`、`stippling`、`colorbar` 等具体英文绘图词项；README 的语言切换不会改变索引或检索分词规则。索引中的语言标签可能表示上游仓库的主要语言，而非单个文件的语言。原始索引生成脚本未随项目分发；[方法说明](docs/corpus-methodology.md)区分了可核验的实现细节与未记录的历史制作过程。

支持的类别：`map`、`time_series`、`distribution`、`uncertainty`、`multi_panel`、`color_style`、`raster_stripes`、`bar_hist_density` 和 `scatter`。

## 项目结构

| 位置 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) | 助手工作流程与输出要求 |
| [scripts/](scripts/) | 检索命令、可复用搜索函数与语料审计 |
| [examples/](examples/) · [assets/](assets/) · [results/](results/) | 示例代码、精选预览与本地生成结果 |
| [references/evidence/](references/evidence/) | 按绘图类别组织的风格指南 |
| [references/rag/](references/rag/) | 13,219 条索引记录及分类表 |
| [references/source-code/](references/source-code/) | 1,141 个归档源文件及独立的打包清单 |
| [tests/](tests/) · [docs/](docs/) | 行为验证、方法、来源与项目指南 |

## 开发与验证

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-demo.txt
python -m unittest discover -s tests -v
python scripts/audit_corpus.py --check
python examples/generate.py
```

检索及语料审计测试无需第三方依赖。缺少绘图库时，示例测试会明确标记为跳过；CI 会安装这些依赖并执行完整测试。修改源码或更新预览前，请阅读[贡献指南](CONTRIBUTING.md)（英文），并同步维护三种语言 README 中的覆盖范围与命令。

## 引用与适用范围

借鉴绘图规范时，请注明上游仓库、文件路径、提交标识和原作者。风格参考不能替代科学数据引用，也不能为不确定性计算提供科学依据。项目不包含大型气候数据，归档脚本也可能依赖其原始运行环境。

源代码档案保留各上游项目的不同使用条款；本项目尚未声明统一的项目级许可证。再分发前请查阅[来源与许可说明](docs/provenance.md)（英文）。Natural Earth 地理数据属于公共领域，其准确来源记录在[数据说明](examples/data/README.md)中。

如果本项目对你的研究有帮助，欢迎在 GitHub 点亮 Star，让更多研究者发现它。可复现的示例、清晰的问题反馈与严谨的来源标注，都是有价值的贡献。
