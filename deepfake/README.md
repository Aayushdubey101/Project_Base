<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,20&height=200&section=header&text=Deepfake%20Detection&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=AI-Powered%20Image%20Authenticity%20Classifier&descAlignY=60&descSize=18" width="100%"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=7C3AED&center=true&vCenter=true&width=600&lines=ResNet-18+%7C+PyTorch+%7C+FastAPI+%7C+Streamlit;Real+vs+Deepfake+%E2%80%94+95%25%2B+Accuracy;Upload+%E2%86%92+Classify+%E2%86%92+Confidence+Score)](https://git.io/typing-svg)

<br/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.13-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.60-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Model](https://img.shields.io/badge/Model-ResNet--18-orange?style=flat-square&logo=pytorch)
![Accuracy](https://img.shields.io/badge/Accuracy-95.53%25-success?style=flat-square)

</div>

---

## 🧠 What It Does

> Upload any image → get an instant verdict: **Real** or **AI-Generated/Deepfake**

A production-style deepfake detection service built end-to-end:
- 🔬 **Fine-tuned ResNet-18** trained on Google Colab T4 with AMP
- ⚡ **FastAPI** REST backend — clean JSON responses with confidence scores
- 🖥️ **Streamlit** interactive UI — drag, drop, detect
- 📦 **`uv`-managed** environment with a locked dependency tree

---

## 🏗️ Architecture

```
╔══════════════════╗        POST /predict        ╔══════════════════════╗
║  Streamlit UI    ║ ──────────────────────────▶  ║   FastAPI Backend    ║
║  :8501           ║ ◀──────────────────────────  ║   :8000              ║
╚══════════════════╝    {label, confidence, ...}  ╚══════════╦═══════════╝
                                                             │
                                              ┌──────────────▼──────────────┐
                                              │       app/ (inference)       │
                                              │  preprocess → model → softmax│
                                              └──────────────┬──────────────┘
                                                             │
                                              ┌──────────────▼──────────────┐
                                              │  models/best_model.pth       │
                                              │  ResNet-18  •  2 classes     │
                                              └─────────────────────────────┘
```

---

## 📁 Folder Structure

```
deepfake/
├── 📂 app/
│   ├── model.py          # ModelLoader singleton (thread-safe)
│   ├── preprocess.py     # Resize → Tensor → ImageNet normalize
│   ├── predict.py        # predict_image() → {label, confidence, probs}
│   └── utils.py          # Upload helpers, extension validation
├── 📂 api/
│   └── main.py           # FastAPI: GET /, GET /health, POST /predict
├── 📂 streamlit/
│   └── app.py            # Upload UI + result display
├── 📂 models/            # best_model.pth + class_names.json (you provide)
├── 📂 tests/
│   └── test_api.py       # pytest: root, health, file-type rejection
├── 📂 uploads/           # Runtime image storage (gitignored)
├── pyproject.toml
├── uv.lock
├── run.py
└── README.md
```

---

## 🚀 Quick Start

### 1 — Install dependencies

```bash
# Requires uv + Python 3.11
uv sync
```

### 2 — Add your model files

```
models/
├── best_model.pth       # ResNet-18 fine-tuned checkpoint
└── class_names.json     # ["ai_images", "real"]
```

### 3 — Run the API

```bash
uv run run.py
# or
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4 — Run the UI (separate terminal)

```bash
uv run streamlit run streamlit/app.py
```

| Service | URL |
|---------|-----|
| FastAPI | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| Streamlit UI | http://localhost:8501 |

---

## 🔌 API Reference

### `POST /predict`

Upload an image file and receive a classification.

**Request** — `multipart/form-data`
```
file: <image file>   # .jpg .jpeg .png .bmp .webp
```

**Response**
```json
{
  "filename": "a3f9c2...jpg",
  "label": "ai_images",
  "confidence": 0.9871,
  "probabilities": {
    "ai_images": 0.9871,
    "real": 0.0129
  },
  "error": null
}
```

### `GET /health`
```json
{ "status": "ok" }
```

---

## 🧪 Testing

```bash
uv run pytest
```

Tests cover:
- `GET /` root response
- `GET /health` status
- `POST /predict` rejects unsupported file types

---

## 🔄 Swapping the Model

`ModelLoader` picks up any ResNet-18 checkpoint automatically:

1. Drop new files into `models/`:
   - `best_model.pth`
   - `class_names.json`
2. Restart the FastAPI process — model loads once at startup.

No code changes needed as long as the checkpoint follows the same architecture.

---

## 🛠️ Common `uv` Commands

```bash
uv add <package>          # add runtime dependency
uv add --dev <package>    # add dev dependency
uv remove <package>       # remove dependency
uv sync                   # install from lockfile
uv run pytest             # run tests
uv sync --no-dev          # production install (skip dev deps)
```

---

## 🚢 Deployment Notes

- **FastAPI**: Serve with `uvicorn --workers N` or gunicorn+uvicorn workers (no `--reload`)
- **Streamlit**: Separate process/service — set `API_URL` in `streamlit/app.py` to the deployed API host
- **Models**: Mount `models/` as a persistent volume so checkpoints survive redeploys
- **Uploads**: `uploads/` should be a writable, ideally ephemeral, volume
- **CORS**: Currently `allow_origins=["*"]` — restrict to your domain in production

---

## 🎓 Training Notebooks

Model trained in **Google Colab** on a **T4 GPU** with automatic mixed precision (AMP):

| Notebook | Description |
|----------|-------------|
| `resnet18_colab_t4_final.ipynb` | Full training run — includes "Version 2" fine-tuning cells |
| `resnet18-colab-t4_initial.ipynb` | Initial experiments |
| `95-53-resnet-18.ipynb` | Best checkpoint (95.53% validation accuracy) |

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,20&height=100&section=footer" width="100%"/>

**Built with ❤️ using PyTorch · FastAPI · Streamlit**

</div>

## Overview

- **app/** — model loading, preprocessing, and inference logic, shared by the API and any other client.
- **api/** — FastAPI app exposing `/`, `/health`, and `/predict`.
- **streamlit/** — Streamlit front end for uploading an image and viewing the prediction.
- **models/** — `best_model.pth` (fine-tuned ResNet-18 checkpoint) and `class_names.json` (`["ai_images", "real"]`), not committed.

Detects two classes: **deepfake/AI-generated** vs **real** images. Trained in `resnet18_colab_t4_final.ipynb` (Colab T4 + AMP); see the "Version 2" cells at the end of that notebook for fine-tuning on additional data.

## Folder structure

```
Deepfake/
├── models/               # best_model.pth, class_names.json (you provide)
├── app/
│   ├── __init__.py
│   ├── model.py          # ModelLoader singleton
│   ├── preprocess.py     # image loading + tensor transforms
│   ├── predict.py        # predict_image(image)
│   └── utils.py          # upload helpers
├── api/
│   ├── __init__.py
│   └── main.py           # FastAPI app
├── streamlit/
│   └── app.py            # Streamlit UI
├── tests/
│   └── test_api.py
├── uploads/               # runtime image uploads (gitignored)
├── assets/
├── pyproject.toml
├── uv.lock
├── run.py                 # FastAPI entrypoint
└── README.md
```

## Installation

Requires [uv](https://docs.astral.sh/uv/) and Python 3.11.

```bash
uv sync
```

This creates `.venv/` and installs everything from `uv.lock`.

## Common uv commands

```bash
uv add <package>          # add a runtime dependency
uv add --dev <package>    # add a dev dependency
uv remove <package>       # remove a dependency
uv sync                   # install/update the environment from the lockfile
uv run <command>          # run a command inside the project environment
uv run pytest             # run the test suite
```

## Running the FastAPI backend

```bash
uv run run.py
```

or directly with uvicorn:

```bash
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at `http://localhost:8000/docs`.

## Running the Streamlit app

In a separate terminal, with the API already running:

```bash
uv run streamlit run streamlit/app.py
```

Streamlit UI available at `http://localhost:8501`.

## Connecting a new trained model

`app/model.py` already instantiates a ResNet-18, replaces `fc` for `len(class_names)`, and loads `checkpoint["model_state_dict"]`. To swap in a new checkpoint:

1. Copy the new checkpoint and label file into `models/`:
   - `models/best_model.pth`
   - `models/class_names.json`
2. Restart the FastAPI process (`ModelLoader` loads once at startup).

No code changes needed as long as the checkpoint is a ResNet-18 fine-tuned the same way (see the notebook) and `class_names.json` keeps the same class order.

## Deployment notes

- Run `uv sync --no-dev` in production to skip dev-only dependencies.
- Serve FastAPI behind a process manager (e.g. `uvicorn` with `--workers`, or behind gunicorn/uvicorn workers) rather than `--reload`.
- Streamlit and FastAPI are separate processes; deploy them independently (e.g. FastAPI on one service/port, Streamlit on another) or put both behind a reverse proxy.
- Set `API_URL` in `streamlit/app.py` to the deployed FastAPI URL instead of `localhost` when they run on different hosts.
- Mount `models/` as a persistent volume so checkpoints survive container restarts/redeploys.
- `uploads/` is gitignored and should also be a writable, ideally ephemeral, volume in production.
