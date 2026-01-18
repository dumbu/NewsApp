# NewsApp Tests

This directory contains the test suite for NewsApp. **All tests must be run inside Docker containers only.**

## Running Tests

### Run all tests
```bash
./newsapp test
```

### Run specific test file
```bash
docker-compose -f docker-compose.test.yml run --rm test pytest tests/test_models.py
```

### Run tests with coverage
```bash
docker-compose -f docker-compose.test.yml run --rm test pytest --cov=src --cov-report=html
```

### Run specific test
```bash
docker-compose -f docker-compose.test.yml run --rm test pytest tests/test_config.py::TestConfigManager::test_save_and_load_config
```

## Test Structure

- `conftest.py` - Shared pytest fixtures and configuration
- `test_models.py` - Tests for data models (Article, Category, etc.)
- `test_config.py` - Tests for configuration management
- `test_cache.py` - Tests for cache functionality
- `test_api.py` - Tests for API/news fetching
- `test_ui_settings.py` - Tests for UI components

## Test Coverage

Run tests with coverage report:
```bash
./newsapp test --coverage
```

## DO NOT run tests locally

All tests should only be executed within Docker containers to ensure:
- Consistent environment
- Proper dependencies
- No pollution of local environment
