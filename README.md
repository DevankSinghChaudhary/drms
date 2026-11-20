# Disaster Resource Management System


## Prerequisites

- Git
- Python >=3.14
- uv (Setup below)

> [!NOTE]
> To install git on windows or any OS refer [here](https://git-scm.com/install/windows)

## SETUP

1. Clone the repository
```bash
git clone https://github.com/DevankSinghChaudhary/drms.git
cd drms
```

2. Install uv

Windows (PowerShell)
```bash
pip install uv
```

3. Install project dependencies
```bash
uv sync
```

4. Run the project
```bash
uv run main.py
```

## Project Structure
```bash
drms/
├── pyproject.toml
├── uv.lock
├── README.md
└── src/
    └── ip_project/
        └── ...
```
