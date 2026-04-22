# Python API Tests

A test automation framework built with **pytest**, **Playwright**, and **Allure**, covering API and UI layers.

## Stack

| Tool | Purpose |
|---|---|
| `pytest` | Test runner |
| `requests` | HTTP API client |
| `playwright` | Browser UI automation |
| `jsonschema` | API response schema validation |
| `allure-pytest` | Test reporting |
| `python-dotenv` | Environment variable management |

## Project Structure

```
python-api-tests/
├── pages/                  # Page Object Models (UI)
│   └── login_page.py
├── schemas/                # JSON schemas for API response validation
│   └── products.json
├── tests/
│   ├── test_products.py    # API tests — reqres.in products endpoint
│   └── ui/
│       └── test_login.py   # UI tests — saucedemo.com login
├── utils/
│   ├── api_client.py       # HTTP client wrapper (requests.Session)
│   └── schema_validator.py # JSON schema validation helper
├── conftest.py             # Shared pytest fixtures
├── config.py               # Environment variable loader
├── pytest.ini              # pytest configuration
├── Dockerfile              # Docker image for running tests in CI
└── requirements.txt        # Python dependencies
```

## Setup

**Prerequisites:** Python 3.12+

```bash
# clone the repo
git clone git@github.com:Djao-Da/cicd.git
cd cicd

# create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# install Playwright browsers
playwright install chromium

# configure environment variables
cp .env.example .env
# edit .env and add your REQRES_API_KEY (get one at https://reqres.in)
```

## Running Tests

```bash
# all tests
pytest -v

# only API tests
pytest tests/test_products.py -v

# only UI tests
pytest tests/ui/ -v

# smoke tests
pytest -m smoke -v

# regression tests
pytest -m regression -v

# UI tests with visible browser
pytest tests/ui/ -v --headed

# UI tests in slow motion (1s delay between actions)
pytest tests/ui/ -v --headed --slowmo 1000
```

## Allure Reports

```bash
# run tests and generate report data
pytest --alluredir=allure-results

# serve the report in browser
allure serve allure-results
```

## Running with Docker

```bash
# build image
docker build -t api-tests .

# run regression tests (pass API key as environment variable)
docker run --rm -e REQRES_API_KEY=your-key api-tests

# run with allure results saved to host machine
docker run --rm \
  -e REQRES_API_KEY=your-key \
  -v $(pwd)/allure-results:/app/allure-results \
  api-tests
```

## Environment Variables

| Variable | Description |
|---|---|
| `REQRES_API_KEY` | API key for reqres.in (get a free one at https://reqres.in) |

Copy `.env.example` to `.env` and fill in your values. The `.env` file is gitignored and never committed.
