# easyocr-api
2022 Codeep Learning Project API Server Repo

### Installation
```bash
pip install easyocr
pip install fastapi uvicorn
pip install python-multipart
```

### GPU Setting
- Visit [PyTorch Website](https://pytorch.org/get-started/locally/) and Download appropriate version depending on your system(ex. CUDA Version).

### Usage
```bash
uvicorn main:app --reload --host=0.0.0.0 --port=8000
```
- Choose your Host(IP) and Port Number.
