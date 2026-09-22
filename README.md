# Selenium + Python BDD Automation Framework

UI test automation using Selenium WebDriver, Behave (BDD/Gherkin),
the Page Object Model, and Allure reporting.

## Tech Stack

- **Python** 3.9+
- **Selenium WebDriver** 4.x — browser automation
- **Behave** — BDD test runner (Gherkin feature files)
- **Allure** — test reporting
- **Page Object Model** — framework design pattern

## Prerequisites

Before you start, make sure you have:

1. **Python 3.9 or higher** installed
   - Check: `python --version`
2. **A browser** installed (Chrome recommended)
   - The matching driver is handled automatically by Selenium Manager
     (built into Selenium 4.6+), so no manual chromedriver download needed.
3. **Allure command-line tool** (only needed to view HTML reports)
   - Installed separately from pip — see "Viewing reports" below.
4. **Git** — to clone the repository.

## Setup

### 1. Clone the repository
```
git clone https://github.com/vishnumuruganantham/selenium-behave-python
cd selenium-behave-python
```

### 2. Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure the environment
Non-secret settings live in `config/config.ini`, split by environment:
```
[app]
timeout = 15

[prod]
base_url = https://www.saucedemo.com/

[qa]
base_url = https://www.int.saucedemo.com/
```

`browser` and `env` are set in `behave.ini` under `[behave.userdata]` (defaults:
`browser = firefox`, `env = prod`), and can be overridden per run without
editing any file:
```
python -m behave -D browser=chrome -D env=qa
```

## 4. Running the tests

Run everything:
```
python -m behave
```

Run only smoke tests (by tag):
```
python -m behave --tags=@smoke
```

Run regression but skip work-in-progress:
```
python -m behave --tags=@regression --tags=~@wip
```

Run a single feature file:
```
python -m behave features/login.feature
```

> **Why `python -m behave`?** Running Behave as a module through the Python
> interpreter avoids PATH issues — the bare `behave` command only works if
> the Python `Scripts` folder is on your system PATH. `python -m behave`
> works everywhere.

## 5. Viewing reports (Allure)

Every `python -m behave` run already writes Allure results automatically —
`behave.ini` runs both the `pretty` (console) and `allure` formatters by
default, and Allure's output goes to `reports/allure-results`. No extra
flags needed.

Open the report (requires the Allure CLI installed):
```
allure serve reports/allure-results
```

> `allure` in `behave.ini` is a short alias registered under
> `[behave.formatters]`, mapping to `allure_behave.formatter:AllureFormatter`.

> The Allure **CLI** is separate from the `allure-behave` pip package.
> Install it via Scoop (Windows), Homebrew (macOS), or download from
> the Allure releases page.

## Project Structure

```
features/         Gherkin .feature files, step definitions, and hooks
pages/            Page Object Model classes (locators + actions)
utils/            Driver factory, config reader, data reader
test_data/        External test data (JSON/CSV/Excel)
config/           config.ini (per-env base URLs, timeouts), config.yaml (YAML example)
reports/          Log file + Allure results output
requirements.txt  Python dependencies
behave.ini        Behave runner configuration (incl. browser/env defaults)
```

## Configuration & Test Data

This framework separates configuration and test data into four sources,
each with a clear purpose:

| Source | Holds | Committed to Git? | Read via |
|--------|-------|-------------------|----------|
| `config/config.ini` | Non-secret settings, per environment — base URL, timeout | Yes | `ConfigReader` (configparser) |
| `behave.ini` `[behave.userdata]` | Which browser and which env to run against | Yes | `context.config.userdata`, or `-D key=value` on the command line |
| `.env` | Secrets — passwords, API keys, tokens | No (git-ignored) | `python-dotenv` + `os.getenv` |
| `test_data/*.json` | Test input data — user profiles, datasets | Yes | `DataReader` (json) |

### 1. `config/config.ini` — environment settings

Non-sensitive settings, one section per environment. Safe to commit.

```
[app]
timeout = 15

[prod]
base_url = https://www.saucedemo.com/

[qa]
base_url = https://www.int.saucedemo.com/
```

Read in code:

```python
from utils.config_reader import ConfigReader

base_url = ConfigReader().get_base_url("prod")   # or "qa", etc.
timeout = ConfigReader().get("app", "timeout")
```

`env` itself comes from `behave.ini`'s `[behave.userdata]` (default `prod`),
resolved in `features/environment.py` and passed into `LoginPage(driver, env)`.
Override per run with `-D env=qa`, same mechanism as `-D browser=chrome`.

### 2. `.env` — secrets (never committed)

Sensitive values that must stay out of the repo. This file is git-ignored;
a `.env.example` template is committed so others know which keys to set.

```
TEST_USERNAME=your_username
TEST_PASSWORD=your_password
```

Read in code:

```python
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("TEST_USERNAME")
```

> Copy `.env.example` to `.env` and fill in real values before running
> tests that need credentials.

### 3. `test_data/*.json` — test input data

Test datasets kept outside the code, so cases can be added without
touching test logic.

```json
{
  "valid_user":   { "username": "vishnu", "password": "secret" },
  "invalid_user": { "username": "vishnu", "password": "wrong"  }
}
```

Read in code by key:

```python
from utils.data_reader import DataReader

user = DataReader.get_user("valid_user")
```

### Which goes where?

- **Changes per environment, not secret** (base URL, timeout) → `config.ini`
- **Which browser/env to run against** → `behave.ini` (`-D browser=...`,
  `-D env=...`)
- **Secret** (passwords, API keys) → `.env`
- **Test inputs** (users, datasets, expected values) → `test_data/*.json`

## Troubleshooting

- **`'behave' is not recognized`** — the Python Scripts folder isn't on
  your PATH. Use `python -m behave` instead (works regardless of PATH),
  or ensure dependencies are installed with `pip install -r requirements.txt`.
- **Browser doesn't open** — check `--headless` isn't set in the driver
  options if you want to watch it run.
- **`allure` command not found** — the Allure CLI isn't installed (it's
  separate from pip); see "Viewing reports."

## Core Selenium

Core Selenium interactions demonstrated against the [sample test website](https://the-internet.herokuapp.com/) to
practice basic Selenium actions with the driver.

**Implemented:**
1. Driver creation
2. Navigating to a URL — refresh, forward, and back
3. Waits: Implicit, Explicit, Fluent
4. Select (dropdowns)
5. Basic exception handling
6. Alerts
7. ActionChains
8. Frames
9. Window handles
10. Reading test data: JSON (`DataReader`), `.env` (`python-dotenv`),
    Excel (`openpyxl`), CSV (`csv`), and YAML (`PyYAML`)