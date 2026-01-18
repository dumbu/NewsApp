# Testing Guide for NewsApp

## Running Tests (Docker Only)

### Quick Start
```bash
# Run all tests
./newsapp test

# Run with coverage report
./newsapp test --coverage

# Run specific test file
./newsapp test tests/test_models.py

# Run specific test
./newsapp test tests/test_config.py::TestConfigManager::test_save_and_load_config

# Run tests matching a pattern
./newsapp test -k "test_article"
```

### Using docker-compose directly
```bash
# Run all tests
docker-compose -f docker-compose.test.yml run --rm test

# Run with coverage
docker-compose -f docker-compose.test.yml run --rm test pytest --cov=src --cov-report=html

# Run specific test file
docker-compose -f docker-compose.test.yml run --rm test pytest tests/test_models.py

# Shell access to test container
docker-compose -f docker-compose.test.yml run --rm test /bin/bash
```

## Test Structure

```
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Shared fixtures
├── test_models.py           # Data model tests
├── test_config.py           # Configuration tests
├── test_cache.py            # Cache functionality tests
├── test_api.py              # API/news fetching tests
└── test_ui_settings.py      # UI component tests
```

## Writing New Tests

1. Create test file in `tests/` directory with `test_` prefix
2. Use pytest conventions (test classes start with `Test`, test functions with `test_`)
3. Use fixtures from `conftest.py` or create new ones
4. Run tests in Docker: `./newsapp test tests/your_new_test.py`

### Example Test
```python
"""tests/test_example.py"""
import pytest

class TestExample:
    def test_something(self, sample_article):
        """Test description."""
        assert sample_article.id is not None
```

## Test Fixtures

Available fixtures from `conftest.py`:
- `temp_config_dir` - Temporary directory for config files
- `config_manager` - ConfigManager instance
- `sample_article` - Single Article instance
- `sample_articles` - List of Article instances

## Test Markers

```bash
# Run only async tests
./newsapp test -m asyncio

# Skip slow tests
./newsapp test -m "not slow"

# Run integration tests
./newsapp test -m integration
```

## Coverage Reports

After running `./newsapp test --coverage`, open the HTML report:
```bash
firefox htmlcov/index.html  # or your browser
```

## Important Rules

⚠️ **DO NOT run tests locally with python/pytest**
✅ **ALWAYS use `./newsapp test` or docker-compose**

This ensures:
- Consistent test environment
- Proper dependencies
- No local environment pollution
- Same conditions as CI/CD
