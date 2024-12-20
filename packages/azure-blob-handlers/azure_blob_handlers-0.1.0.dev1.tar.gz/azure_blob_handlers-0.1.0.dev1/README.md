# Azure Blob Handlers

Azure Blob Handling libray for Python.


## Setup environment

### 1. Install dependencies

```
poetry install
```

### 2. Build with poetry

```
poetry build
```

### 3. Publish to PyPi

```
poetry publish
```


## Test azure-blob-hadlers package

### 1. Create azurite container

```
docker compose up -d
```

### 2. Create test container and upload test files

```
python -m tests.setup_azurite
```

## 3. Run tests

```
python -m pytest
```