# 🐳 Toy Robot

## 1. Install deps
```bash
 pip install --no-cache-dir pytest
```

## 2. Run tests with docker
From the project root:
```bash
docker build -t toyrobot .
docker run --rm toyrobot
```

## Run tests with pytest
```bash
pytest
```

## 3. Run sample file
```bash
PYTHONPATH=src python -m toy_robot.robot cmd.txt
```
