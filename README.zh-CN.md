<p align="right">
  Language Switch / 语言选择：
  <a href="./README.zh-CN.md">🇨🇳 中文</a> | <a href="./README.md">🇬🇧 English</a>
</p>

**项目介绍**
---
**Runner Pro** 是一款基于 Python 开发的跑步数据分析与人工智能智能体应用，旨在结合运动科学、统计分析、交互式数据可视化及智能评估技术，将个人运动记录转化为具有实际参考价值的数据分析结果。

Runner Pro 使用 **Streamlit** 构建交互式应用界面，并集成基于 **LangGraph 和大语言模型（LLMs）** 的人工智能 **智能体（AI
Agents）**，为训练负荷、跑步效率和运动后心率恢复等指标提供专门的数据分析与智能评估工作流。

与完全依赖大语言模型进行数值计算的方式不同，Runner Pro 将**确定性的数据处理和运动指标计算与智能体驱动的分析解读相结合**
，实现定量分析与 AI 评估的职责分离，从而提高分析流程的透明度、结构化程度及结果的可解释性。

**核心功能**
---

- **数据管理（Data Management）：** 加载、组织和查看运动记录，提供结构化的数据管理流程。
- **数据质量与插补（Data Quality & Imputation）：** 识别缺失值和重复记录，支持多种可配置的数值型与类别型数据插补方法。
- **急性与慢性训练负荷比（ACWR）：** 分析短期与长期训练负荷之间的关系，识别训练负荷的变化情况。
- **运动效率因子（EF）：** 通过运动速度与平均心率之间的关系，分析跑步效率及其变化趋势。
- **心率恢复（HRR）：** 基于运动结束时及随后两分钟内的心率记录，分析运动后的心率恢复情况。
- **交互式数据可视化（Interactive Data Visualisation）：** 通过交互式数据表格和图表展示运动指标及其长期变化趋势。
- **人工智能智能体（AI Agents）：** 使用专门的分析智能体解读运动指标、识别相关变化模式、评估数据局限性，并生成结构化分析结果。
- **智能体工作流（Agent-Based Workflows）：** 使用 LangGraph 编排分析与评估流程，结合结构化数据模型和可配置的大语言模型。
- **AI 辅助训练建议（AI-Assisted Training Recommendations）：** 根据现有运动数据生成具有条件性和参考价值的训练及恢复建议。
- **可配置分析（Configurable Analysis）：** 支持调整数据处理方法、AI 模型及评估语言。

**智能体架构**
---
Runner Pro 使用 **LangGraph、LangChain 和 Pydantic** 构建模块化的人工智能智能体架构。

针对不同的跑步训练指标，项目设计了专门的分析智能体：

- **ACWR Agent（训练负荷分析智能体）：** 分析急性与慢性训练负荷之间的关系，并生成训练负荷管理评估。
- **EF Agent（运动效率分析智能体）：** 解读跑步效率的变化趋势，分析运动速度与心率之间的关系。
- **HRR Agent（心率恢复分析智能体）：** 分析运动后的心率恢复模式，包括第一分钟与第二分钟的心率恢复特征。

智能体工作流将运动数据的定量分析与大语言模型的解释能力相结合，并通过结构化输入与输出模型保持评估结果的一致性。

整体架构将数据准备、数值计算、智能体工作流编排和评估结果生成相互分离，使不同分析模块能够独立开发、维护和扩展。

**技术栈**
---

- **Python：** 应用开发、业务逻辑与数据分析。
- **Streamlit：** 交互式用户界面与数据可视化。
- **Pandas：** 数据处理、预处理及数值计算。
- **SQLAlchemy & SQLite：** 数据库操作与结构化数据存储。
- **Pydantic：** 数据验证与 AI 评估结果的结构化输出。
- **LangChain：** 大语言模型集成与结构化模型调用。
- **LangGraph：** 智能体工作流编排与状态管理。
- **DeepSeek & OpenAI：** AI 辅助评估所支持的大语言模型服务提供商。

**简单演示**
---

1. 将本仓库克隆到本地计算机。
2. 使用以下命令安装所需依赖项：`pip install -r requirements.txt`
3. 使用以下命令运行应用程序：`streamlit run main.py`
4. 你也可以通过点击以下链接在线体验该应用：  
   [![Static Badge](https://img.shields.io/badge/Open%20in%20Streamlit-Daochashao-red?style=for-the-badge&logo=streamlit&labelColor=white)](https://lg-run-pro.streamlit.app/)

**隐私声明**
---
本应用程序旨在处理您提供的数据以生成定制化的建议和结果。您的隐私至关重要。

**我们不会收集、存储或传输您的个人信息或数据。** 所有处理都在您的设备本地进行（在浏览器或运行时环境中），*
*数据永远不会发送到任何外部服务器或第三方。**

- **本地处理：** 您的数据永远不会离开您的设备。整个分析和生成过程都在本地进行。
- **无数据保留：** 由于没有数据传输，因此不会在任何服务器上存储数据。关闭应用程序通常会清除任何临时本地数据。
- **透明度：** 整个代码库都是开源的。我们鼓励您随时审查[代码](./)以验证您的数据处理方式。

总之，您始终完全控制和拥有自己的数据。

**许可声明**
---
本项目是开源的，可在 [BSD-3-Clause 许可证](LICENCE) 下使用。

简单来说，这是一个非常宽松的许可证，允许您几乎出于任何目的自由使用此代码，包括在专有项目中，只要您包含原始的版权和许可证声明。

欢迎随意分叉、修改并在此作品基础上进行构建！我们只要求您在适当的地方给予认可。

**环境设置**
---
本项目使用 **Python 3.12** 和 [uv](https://docs.astral.sh/uv/) 进行快速的依赖管理和虚拟环境处理。所需的 Python
版本会自动从 [.python-version](.python-version) 文件中检测到。

1. **安装 uv**：  
   如果您还没有安装 `uv`，可以使用以下命令安装：
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # 此安装方法适用于 macOS 和 Linux。
    ```
   或者，您可以运行以下 PowerShell 命令来安装：
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    # 此安装方法适用于 Windows。
    ```

   **💡 推荐**：为了获得最佳体验，请将 `uv` 作为独立工具安装。避免在 `pip` 或 `conda` 环境中安装，以防止潜在的依赖冲突。

2. **添加依赖**：

- 添加主要（生产）依赖：
    ```bash
    uv add <package_name>
    # 这会自动更新 pyproject.toml 并安装包
    ```
- 添加开发依赖：
    ```bash
    uv add <package_name> --group dev
    # 示例：uv add ruff --group dev
    # 这会自动将包添加到 [project.optional-dependencies.dev] 部分
    ```
- 添加其他类型的可选依赖（例如测试、文档）：
    ```bash
    uv add <package_name> --group test
    uv add <package_name> --group docs
    ```
- 从 `requirements.txt` 文件导入依赖：
    ```bash
    uv add -r requirements.txt
    # 这会从 requirements.txt 读取包并将其添加到 pyproject.toml
    ```

3. **移除依赖**

- 移除主要（生产）依赖：
    ```bash
    uv remove <package_name>
    # 这会自动更新 pyproject.toml 并移除包
    ```
- 移除开发依赖：
    ```bash
    uv remove <package_name> --group dev
    # 示例：uv remove ruff --group dev
    # 这会从 [project.optional-dependencies.dev] 部分移除包
    ```
- 移除其他类型的可选依赖：
    ```bash
    uv remove <package_name> --group test
    uv remove <package_name> --group docs
    ```

4. **管理环境**

- 使用添加/移除命令后，同步环境：
    ```bash
    uv sync
    ```

**更新日志**
---
本项目使用 [git-changelog](https://github.com/pawamoy/git-changelog)
基于 [Conventional Commits](https://www.conventionalcommits.org/) 自动生成和维护更新日志。

1. **安装**
   ```bash
   pip install git-changelog
   # 或使用 uv 将其添加为开发依赖
   uv add git-changelog --group dev
   ```
2. **验证安装**
   ```bash
   pip show git-changelog
   # 或专门检查版本
   pip show git-changelog | grep Version
   ```
3. **配置**
   确保您在项目根目录有一个正确配置的 `pyproject.toml` 文件。配置应将 Conventional Commits 指定为更新日志样式。以下是示例配置：
   ```toml
   [tool.git-changelog]
   version = "0.1.0"
   style = "conventional-commits"
   output = "CHANGELOG.md"
   ```
4. **生成更新日志**
   ```bash
   git-changelog --output CHANGELOG.md
   # 或者使用 uv 运行
   uv run git-changelog --output CHANGELOG.md
   ```
   此命令会根据您的 git 历史记录创建或更新 `CHANGELOG.md` 文件。
5. **推送更改**
   ```bash
   git push origin main
   ```
   或者，使用您 IDE 的 Git 界面（例如，在许多编辑器中的 `Git → Push`）。
6. **注意**：

- 更新日志是根据您的提交消息遵循 Conventional Commits 规范自动生成的。
- 每当您想要更新更新日志时（通常在发布之前或进行重大更改之后），运行生成命令。
