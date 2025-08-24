# 🐳 Toy Robot

## Run tests with pytest
```bash
 pip install --no-cache-dir pytest
 pytest
```

## Run tests with docker
From the project root:
```bash
docker build -t toyrobot .
docker run --rm toyrobot
```

## Run sample file
```bash
PYTHONPATH=src python -m toy_robot.robot cmd.txt
```
