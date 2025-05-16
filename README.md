# Ethereum Validator Data Aggregation

This project processes and aggregates data about Ethereum validators from a given input file. The primary goal is to compute specific metrics both on a per-block basis and as a total aggregation across all blocks. The solution is orchestrated in Python using the Polars library for efficient data manipulation.

---

## 🚀 Quick Start (VS Code Dev Container)

This project is configured to run inside a VS Code Dev Container, providing a consistent and isolated development environment with all necessary dependencies pre-installed.

### Requirements

- Visual Studio Code with the "Dev Containers" extension (ms-vscode-remote.remote-containers) installed.
- Docker Desktop (for macOS or Windows) or Docker Engine (for Linux) installed and running.
- Git, for cloning the repository.

### Setup & Running

1. **Clone the Repository**:

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2. **Initialize Git LFS (if not already done post-clone for `input_data`)**:
    The input data file (`input_data/validators_data.json.gz`) is expected to be managed by Git LFS. If you have cloned the repository and the LFS file is just a pointer, run:

    ```bash
    git lfs pull
    ```

3. **Open in Dev Container**:
    - Open the cloned repository folder in Visual Studio Code.
    - VS Code should automatically detect the `.devcontainer/devcontainer.json` configuration and prompt you to "Reopen in Container". Click it.
    - Alternatively, press **F1** (or **Ctrl+Shift+P** / **Cmd+Shift+P**) to open the command palette, type `Dev Containers: Reopen in Container`, and select it.
4. **Run the Pipeline**:
    Once the Dev Container is built and started, VS Code will connect to it. An integrated terminal will be available.
    Use the `Makefile` to run the main data processing pipeline:

    ```bash
    make run
    ```

5. **Verify Output**:
    To verify the correctness of the generated output files against the expected structure and values:

    ```bash
    make validate
    ```

    This command runs `scripts/validate_output.py`.

The Dev Container environment ensures that you have all the necessary Python packages and tools installed without needing to manage them on your local machine.

---

## ⚙️ CI (Continuous Integration)

- **Workflow File**: `.github/workflows/ci.yml`
- **Purpose**: The CI pipeline automates testing and validation for every push or pull request to the `main` branch.
- **Key Steps**:
    1. **Checkout Code**: Fetches the latest version of your repository.
    2. **Set up Python**: Initializes the Python environment.
    3. **Install Dependencies**: Installs project dependencies (e.g., from `requirements.txt`).
    4. **Run Linters/Formatters (Optional but Recommended)**: Checks for code style and formatting (e.g., using Black, Flake8, Ruff). *(Note: Add these if they are part of your CI)*
    5. **Run Tests**: Executes unit tests using `pytest` (e.g., `make test` or `pytest tests/`).
- **Outcome**: Ensures code quality, correctness of aggregations (on sample data), and that tests pass before changes are merged.

---

## 🗂️ Key Files & Project Structure

```
.
├── .devcontainer/                # VS Code Dev Container configuration
│   ├── git-aliases.conf          # Defines container settings, extensions, etc.
│   └── devcontainer.json         # Defines container settings, extensions, etc.
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI workflow
├── input_data/
│   └── validators_data.json.gz   # Input validator data (managed by Git LFS)
├── output/                       # Directory where output JSON files are saved 
├── scripts/
│   └── validate_output.py        # Script for detailed validation of output files against verify.py
├── src/
│   ├── aggregator.py             # Core logic for data aggregation using Polars
│   ├── main.py                   # Main script to orchestrate the pipeline
│   └── ...                       # Other utility/config Python modules
├── tests/
│   └── test_aggregator.py        # Unit tests for the aggregation logic
├── .gitignore
├── Makefile                      # Common commands for building, running, testing
├── README.md                     # This file
├── requirements.txt              # Python project dependencies
└── verify.py                     # Script to verify the structure and values of output files
```

---

## 📝 Assignment Requirements Summary

The core task is to process an input file containing Ethereum validator data and provide the following aggregations:

**Per Block:**

- Total balance for all validators
- Total effective balance for all validators
- Number of slashed validators
- Number of validators per status

**Total Aggregation (for all blocks combined):**

- Total balance for all validators
- Total effective balance for all validators
- Number of slashed validators
- Number of validators per status

The solution uses Python and the Polars library. The output structure is implicitly defined by `verify.py`.

---
