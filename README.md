<p align="right">
  Language Switch / 语言选择：
  <a href="./README.zh-CN.md">🇨🇳 中文</a> | <a href="./README.md">🇬🇧 English</a>
</p>

**INTRODUCTION**
---
**Runner Pro** is a Python-based running analytics and AI agent application designed to transform personal exercise
records into meaningful, data-driven insights through exercise science, statistical analysis, interactive visualisation,
and intelligent assessment.

Built with **Streamlit**, Runner Pro integrates traditional data analytics with **specialised AI agents powered by
LangGraph and large language models (LLMs)**. The application provides dedicated analytical workflows for evaluating
training workloads, running efficiency, and post-exercise heart rate recovery.

Rather than relying exclusively on LLMs for numerical calculations, Runner Pro combines **deterministic data processing
and exercise metric calculations with agent-based interpretation and assessment**. This approach separates quantitative
analysis from AI-generated insights, supporting more transparent, structured, and evidence-informed assessments.

**FEATURES**
---

- **Data Management:** Load, organise, and explore exercise records through structured data management workflows.
- **Data Quality & Imputation:** Identify missing values and duplicate records, and apply configurable numerical and
  categorical imputation methods.
- **Acute:Chronic Workload Ratio (ACWR):** Examine short-term and long-term training workload relationships to identify
  workload variations.
- **Efficiency Factor (EF):** Evaluate running efficiency through the relationship between exercise speed and average
  heart rate.
- **Heart Rate Recovery (HRR):** Analyse post-exercise heart rate recovery using measurements collected immediately
  after exercise and during the following two minutes.
- **Interactive Data Visualisation:** Explore exercise metrics and longitudinal trends through interactive data tables
  and charts.
- **AI Agents:** Use specialised agents to interpret exercise metrics, identify relevant patterns, evaluate data
  limitations, and generate contextual assessments.
- **Agent-Based Workflows:** Orchestrate analytical and assessment operations using LangGraph, with structured data
  models and configurable LLM integrations.
- **AI-Assisted Training Recommendations:** Generate conditional training and recovery recommendations based on
  available exercise data.
- **Configurable Analysis:** Customise supported data processing methods, AI models, and assessment languages.

**AGENT ARCHITECTURE**
---
Runner Pro incorporates a modular AI agent architecture built with **LangGraph, LangChain, and Pydantic**.

Specialised analytical agents are designed to handle different aspects of running performance:

- **ACWR Agent:** Analyses acute and chronic training workload relationships and provides workload management
  assessments.
- **EF Agent:** Interprets running efficiency trends and evaluates variations in speed relative to heart rate.
- **HRR Agent:** Examines post-exercise heart rate recovery patterns, including first-minute and second-minute recovery
  characteristics.

The agent workflows combine quantitative exercise data with LLM-based interpretation, using structured input and output
schemas to maintain consistent assessment formats.

The architecture separates data preparation, numerical calculations, agent orchestration, and assessment generation,
allowing individual analytical components to be developed and maintained independently.

**TECHNOLOGY STACK**
---

- **Python:** Core application development and analytical logic.
- **Streamlit:** Interactive user interface and data visualisation.
- **Pandas:** Data manipulation, preprocessing, and numerical calculations.
- **SQLAlchemy & SQLite:** Database operations and structured data storage.
- **Pydantic:** Data validation and structured AI assessment outputs.
- **LangChain:** LLM integration and structured model interactions.
- **LangGraph:** Agent workflow orchestration and state management.
- **DeepSeek & OpenAI:** Supported LLM providers for AI-assisted assessments.

**Simple Demonstration**
---

1. Clone the repository to your local machine.
2. Install the required dependencies with the command `pip install -r requirements.txt`.
3. Run the application with the command `streamlit run main.py`.
4. You can also try the application by visiting the following
   link:  
   [![Static Badge](https://img.shields.io/badge/Open%20in%20Streamlit-Daochashao-red?style=for-the-badge&logo=streamlit&labelColor=white)](https://lg-run-pro.streamlit.app/)

**PRIVACY NOTICE**
---

This application is designed to process the data you provide to generate customized suggestions and results. Your
privacy is paramount.

**We do not collect, store, or transmit your personal information or data.** All processing occurs locally on your
device (in your browser or runtime environment), and **no data is ever sent to an external server or third party.**

- **Local Processing:** Your data never leaves your device. The entire analysis and generation process happens locally.
- **No Data Retention:** Since no data is transmitted, none is stored on any server. Closing the application typically
  clears any temporary local data.
- **Transparency:** The entire codebase is open source. You are encouraged to review the [code](./) to verify how your
  data is handled.

In summary, you maintain full control and ownership of your data at all times.

**LICENCE**
---
This project is open source and available under the **[BSD-3-Clause Licence](LICENCE)**.

In simple terms, this is a very permissive licence that allows you to freely use this code for almost any purpose,
including in proprietary projects, as long as you include the original copyright and licence notice.

Feel free to fork, modify, and build upon this work! We simply ask that you give credit where credit is due.

**ENVIRONMENT SETUP**
---
This project uses **Python 3.12** and [uv](https://docs.astral.sh/uv/) for fast dependency management and virtual
environment handling. The required Python version is automatically detected from the [.python-version](.python-version)
file.

1. **Installing uv**:  
   If you don't have `uv` installed, you can install it using the following command:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # This installation method works on macOS and Linux.
    ```
   Alternatively, you can install it by running the following PowerShell command:
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    # This installation method works on Windows.
    ```

   **💡 Recommended**: For the best experience, install `uv` as a standalone tool. Avoid installing it within `pip` or
   `conda` environments to prevent potential dependency conflicts.

2. **Adding Dependencies**:

- To add a main (production) dependency:
    ```bash
    uv add <package_name>
    # This automatically updates pyproject.toml and installs the package
    ```
- To add a development dependency:
    ```bash
    uv add <package_name> --group dev
    # Example: uv add ruff --group dev
    # This adds the package to the [project.optional-dependencies.dev] section automatically
    ```
- To add other types of optional dependencies (e.g., test, docs):
    ```bash
    uv add <package_name> --group test
    uv add <package_name> --group docs
    ```
- To import dependencies from a `requirements.txt` file:
    ```bash
    uv add -r requirements.txt
    # This reads packages from requirements.txt and adds them to pyproject.toml
    ```

3. Removing Dependencies

- To remove a main (production) dependency:
    ```bash
    uv remove <package_name>
    # This automatically updates pyproject.toml and removes the package
    ```
- To remove a development dependency:
    ```bash
    uv remove <package_name> --group dev
    # Example: uv remove ruff --group dev
    # This removes the package from the [project.optional-dependencies.dev] section
    ```
- To remove other types of optional dependencies:
    ```bash
    uv remove <package_name> --group test
    uv remove <package_name> --group docs
    ```

4. **Managing the Environment**

- After using add/remove commands, sync the environment:
    ```bash
    uv sync
    ```

**CHANGELOG**
---
This project uses [git-changelog](https://github.com/pawamoy/git-changelog) to automatically generate and maintain a
changelog based on [Conventional Commits](https://www.conventionalcommits.org/).

1. **Installation**
   ```bash
   pip install git-changelog
   # or use uv to add it as a development dependency
   uv add git-changelog --group dev
   ```
2. **Verify Installation**
   ```bash
   pip show git-changelog
   # or check the version specifically
   pip show git-changelog | grep Version
   ```
3. **Configuration**
   Ensure you have a properly configured `pyproject.toml` file at the project root. The configuration should specify
   Conventional Commits as the changelog style. Here is an example configuration:
   ```toml
   [tool.git-changelog]
   version = "0.1.0"
   style = "conventional-commits"
   output = "CHANGELOG.md"
   ```
4. **Generate Changelog**
   ```bash
   git-changelog --output CHANGELOG.md
   # Or use uv to run it if installed as a dev dependency
   uv run git-changelog --output CHANGELOG.md
   ```
   This command creates or updates the `CHANGELOG.md` file with all changes based on your git history.
5. **Push Changes**
   ```bash
   git push origin main
   ```
   Alternatively, use your IDE's Git interface (e.g., `Git → Push` in many editors).
6. **Note**:

- The changelog is automatically generated from your commit messages following the Conventional Commits specification.
- Run the generation command whenever you want to update the changelog, typically before a release or after significant
  changes.
