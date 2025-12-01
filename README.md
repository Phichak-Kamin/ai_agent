# AI Agent

[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/Phichak-Kamin/ai_agent)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)]

Overview
--------
ai_agent is a starter project for building an "AI agent" — a programmable autonomous assistant that can process commands, orchestrate tasks, and integrate with external models or providers (e.g., OpenAI, local LLMs). This README is a practical, ready-to-use reference tailored to this repository.

Status
------
alpha — actively developed and suitable for experimentation. Use in production only after additional hardening, testing, and security review.

Features
--------
- Starter architecture for an AI agent
- Provider abstraction for connecting to external LLMs or APIs
- Configuration and environment variable support
- Example run modes: local script and Docker
- Development and testing guidelines and a recommended CI workflow

Prerequisites
-------------
- Python 3.9+
- pip
- (Optional) API key(s) for model providers (e.g., OPENAI_API_KEY)
- (Recommended) virtualenv, pyenv, or similar environment manager
- Docker (optional, for containerized runs)

Quick Installation
------------------
1. Clone the repository:
```bash
git clone https://github.com/Phichak-Kamin/ai_agent.git
cd ai_agent
```

2. Create and activate a virtual environment, then install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

3. Configure environment variables:
- Create a `.env` file (recommended) or export variables in your shell.
- Example `.env`:
```
OPENAI_API_KEY=sk-...
AGENT_CONFIG=./configs/default.yaml
PORT=8000
LOG_LEVEL=info
```
- Ensure `.env` and other secret-containing files are listed in `.gitignore`.

Quick Start
-----------
Run the agent with the example configuration:
```bash
python run_agent.py --config configs/default.yaml
```
Common CLI options (implemented in example runner):
- --config PATH        YAML config file (default: configs/default.yaml)
- --port PORT          HTTP server port (if applicable)
- --debug              Enable debug logging

If your project uses a different entrypoint (e.g., `app.py` or `main.py`), run that instead.

Example Usage
-------------
Programmatic usage example (adjust import paths and class names to match the repository):
```python
from ai_agent import Agent

agent = Agent(config_path="configs/default.yaml")
response = agent.run("Summarize the following content and suggest next steps.")
print(response)
```

Project Structure
-----------------
Current repository layout (update as the project grows):
```
ai_agent/
├── ai_agent/
│   ├── __init__.py
│   ├── agent.py                # core Agent class & orchestration
│   ├── providers/              # provider integrations (OpenAI, HF, local LLM)
│   ├── utils/                  # helpers, logging, retry logic
│   └── config/                 # config loader and validators
├── configs/
│   └── default.yaml
├── tests/
├── requirements.txt
├── requirements-dev.txt        # linting, testing tools
├── run_agent.py                # CLI entrypoint
└── README.md
```
If your layout differs, update this section accordingly.

Configuration
-------------
The config file controls provider selection, model settings, timeouts, and retries. The example below matches what the agent expects by default.

Example `configs/default.yaml`:
```yaml
provider: openai
model: gpt-4o
temperature: 0.2
max_tokens: 1024
timeout: 30
retries: 2
log_level: info
```

Environment variables can override the config where supported (e.g., AGENT_CONFIG, OPENAI_API_KEY, PORT, LOG_LEVEL).

Development
-----------
- Activate your virtual environment.
- Install development dependencies:
```bash
pip install -r requirements-dev.txt
```
- Lint / format:
```bash
black .
flake8
```
- Run unit tests:
```bash
pytest
```

Testing
-------
Add unit tests for core logic: provider integrations, prompt handling, error and fallback behavior.
Run tests with:
```bash
pytest tests/
```

Security
--------
- Never commit secret keys to the repository.
- Add `.env` and other secret files to `.gitignore`.
- Use a secret manager for production deployments (e.g., GitHub Secrets, AWS Secrets Manager, GCP Secret Manager).
- Validate and sanitize user-provided input before sending it to models or executing system operations.

CI/CD and Deployment
--------------------
Recommended GitHub Actions CI (example):
- Linting with black/flake8
- Unit tests with pytest
- (Optional) Build and push Docker image on release

Example minimal `.github/workflows/ci.yml`:
```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt || true
      - name: Lint
        run: black --check . && flake8
      - name: Test
        run: pytest -q
```

Contributing
------------
Thanks for considering contributing! Suggested workflow:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feat/your-feature
   ```
3. Implement your change and add tests.
4. Open a Pull Request with a clear description.

Consider adding `.github/ISSUE_TEMPLATE` and `.github/PULL_REQUEST_TEMPLATE` to make contributions easier.

License
-------
This project is licensed under the MIT License — see the LICENSE file for details.
