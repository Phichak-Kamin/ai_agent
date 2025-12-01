# AI Agent

[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/Phichak-Kamin/ai_agent)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)]

Overview
--------
ai_agent is a starter project for building an "AI agent" — a programmable autonomous assistant that can process commands, orchestrate tasks, and integrate with external models or providers. This repository is configured to use an Ollama instance with the qwen2.5 model by default.

Status
------
alpha — actively developed and suitable for experimentation. Use in production only after additional hardening, testing, and security review.

Features
--------
- Starter architecture for an AI agent
- Built-in support for Ollama and qwen2.5 model
- Provider abstraction so additional providers can be added later
- Configuration and environment variable support
- Example run modes: local script and Docker
- Development and testing guidelines and recommended CI workflow

Prerequisites
-------------
- Python 3.9+
- pip
- Ollama running locally or accessible remotely (see Ollama docs)
- qwen2.5 model installed or available in your Ollama instance
- (Optional) API key if your Ollama server is protected
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

3. Ensure Ollama is running and that qwen2.5 is available
- If using a local Ollama server, the default URL is http://localhost:11434
- Install or pull the qwen2.5 model into your Ollama instance using Ollama instructions (see Ollama docs)

4. Configure environment variables:
- Create a `.env` file (recommended) or export variables in your shell.
- Example `.env`:
```
PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5
AGENT_CONFIG=./configs/default.yaml
PORT=8000
LOG_LEVEL=info
OLLAMA_API_KEY=           # optional, only if your Ollama server requires auth
```
- Ensure `.env` and other secret-containing files are listed in `.gitignore`.

Quick Start
-----------
Run the agent with the example configuration:
```bash
# Using config file
python run_agent.py --config configs/default.yaml

# Or using environment variables (example)
OLLAMA_URL=http://localhost:11434 OLLAMA_MODEL=qwen2.5 python run_agent.py
```

If your project uses a different entrypoint (e.g., `app.py` or `main.py`), run that instead.

Example Usage
-------------
Programmatic usage example that calls the configured Ollama instance directly (adjust imports / paths to match your repo layout):

```python
import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")

def generate(prompt, temperature=0.2, max_tokens=1024):
    url = f"{OLLAMA_URL}/api/generate?model={MODEL}"
    payload = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    headers = {}
    api_key = os.getenv("OLLAMA_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()  # adapt parsing based on how your Ollama instance returns results

if __name__ == "__main__":
    print(generate("Summarize the following text and suggest next steps: ..."))
```

Note: Confirm the exact request/response fields with your Ollama version and model. The example above is a general pattern and may require minor adjustments for your Ollama server.

Docker (Optional)
-----------------
Build and run a Docker image:
```bash
docker build -t ai_agent:latest .
# If connecting to a local Ollama instance from inside Docker on macOS/Windows:
docker run --env-file .env -p 8000:8000 ai_agent:latest

# If Docker must access host Ollama on Linux, consider --network="host"
# docker run --env-file .env --network="host" ai_agent:latest
```
If your Ollama server is on the host machine and you run the container with default bridge networking, set OLLAMA_URL to host.docker.internal (or the host IP) so the container can reach the Ollama server.

Project Structure
-----------------
Current repository layout (update as the project grows):
```
ai_agent/
├── ai_agent/
│   ├── __init__.py
│   ├── agent.py                # core Agent class & orchestration
│   ├── providers/              # provider integrations (ollama provider included)
│   ├── utils/                  # helpers, logging, retry logic
│   └── config/                 # config loader and validators
├── configs/
│   └── default.yaml
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── run_agent.py                # CLI entrypoint
└── README.md
```

Configuration
-------------
The config file controls provider selection, model settings, timeouts, and retries. The example below matches the default Ollama + qwen2.5 setup.

Example `configs/default.yaml`:
```yaml
provider: ollama
model: qwen2.5
ollama:
  url: http://localhost:11434
  api_key: ""          # optional; use environment variables for secrets
temperature: 0.2
max_tokens: 1024
timeout: 30
retries: 2
log_level: info
```

Environment variables can override the config where supported (e.g., AGENT_CONFIG, OLLAMA_URL, OLLAMA_MODEL, OLLAMA_API_KEY).

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
Add unit tests for core logic: provider integrations (including the Ollama provider), prompt handling, error and fallback behavior.
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
Recommended GitHub Actions CI:
- Linting with black/flake8
- Unit tests with pytest
- (Optional) Build and push Docker image on release

Example minimal `.github/workflows/ci.yml` is included in the repo templates section (if you choose to add it).

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
