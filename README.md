# Doc2MD

[![Docker Pulls](https://img.shields.io/docker/pulls/felipefontoura/doc2md)](https://hub.docker.com/r/felipefontoura/doc2md)
[![Docker Image Size](https://img.shields.io/docker/image-size/felipefontoura/doc2md)](https://hub.docker.com/r/felipefontoura/doc2md)

Convert documents to Markdown format through a simple API service.

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
docker run -d -p 5000:5000 felipefontoura/doc2md
```

### API Usage

Convert a document to Markdown:

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.xlsx" \
  http://localhost:5000/convert
```

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Development](#development)

## ✨ Features

- Convert Excel files to Markdown
- Simple REST API interface
- Docker support
- Easy deployment with Docker Stack
- Multipart file upload support

## 🛠️ Installation

### Using Docker Hub

1. Pull the image:

```bash
docker pull felipefontoura/doc2md
```

2. Run the container:

```bash
docker run -d -p 5000:5000 felipefontoura/doc2md
```

## 💻 Usage

### API Endpoints

#### Convert Document

```bash
curl -X POST \
  -F "file=@file.xlsx" \
  http://localhost:5000/convert
```

## 📦 Deployment

### Docker Stack Deployment

Deploy using Docker Stack:

```bash
docker stack deploy --prune --resolve-image always -c stack.yml doc2md
```

Example `doc2md.yml`:

```yaml
version: '3.7'
services:
  doc2md:
    image: felipefontoura/doc2md:latest
    ports:
      - "5000:5000"
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
```

## 🔧 Development

1. Clone the repository
2. Build the Docker image locally
3. Run tests
4. Submit pull requests

## 📝 License

[MIT License](LICENSE)

---
Made with ❤️ by Felipe Fontoura
