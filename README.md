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
Edit `config/config.ini` with your target URL, browser, and timeouts:
```
[app]
base_url = https://example.com
browser = chrome
timeout = 15
```

## Running the tests

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

## Viewing reports (Allure)

1. Run tests with the Allure formatter (writes raw results):
```
   python -m behave -f allure -o reports/allure
```
   > `allure` here is a short alias registered in `behave.ini` under
   > `[behave.formatters]`. It maps to
   > `allure_behave.formatter:AllureFormatter`, so you don't have to type
   > the full path each time.
2. Open the report (requires the Allure CLI installed):
```
   allure serve reports/allure
```

> The Allure **CLI** is separate from the `allure-behave` pip package.
> Install it via Scoop (Windows), Homebrew (macOS), or download from
> the Allure releases page.

## Project Structure

```
features/         Gherkin .feature files, step definitions, and hooks
pages/            Page Object Model classes (locators + actions)
utils/            Driver factory, config reader, data reader
test_data/        External test data (JSON/CSV/Excel)
config/           config.ini (URLs, browser, timeouts)
reports/          Allure results output
requirements.txt  Python dependencies
behave.ini        Behave runner configuration
```

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
