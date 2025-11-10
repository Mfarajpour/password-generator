
# 🔐 Secure Password Generator

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitLab-orange)

A secure, production-ready password generator API built with Flask, featuring complete CI/CD pipeline and automated deployment.

---

## 🚀 Quick Start

```bash
# Using Docker Compose (Recommended)
docker-compose up -d

# Or using Docker
docker run -d -p 5000:5000 password-generator

# Or local development
pip install -r requirements.txt
python app.py
```

Visit: `http://localhost:5000`

---

## ✨ Features

### 🔒 Security First
- 🛡️ Uses `secrets` module for cryptographically strong random generation
- 👤 Non-root user in Docker containers
- ✅ Input validation and sanitization
- 🔐 Environment-based configuration

### 🚢 Production Ready
- 📦 Multi-stage Docker build (optimized image size)
- ⚡ Gunicorn WSGI server with worker management
- 💚 Health check endpoints
- 📊 Resource limits and monitoring
- 🔄 Graceful shutdown handling

### 🤖 Complete DevOps Pipeline
- ✅ **CI/CD**: Full GitLab pipeline (Test → Build → Deploy → Verify → Cleanup)
- 🧪 **Testing**: Separated unit and integration tests
- 📈 **Coverage**: Automated code coverage reporting
- 🔄 **Rollback**: One-click rollback capability
- 🧹 **Cleanup**: Automated old image cleanup
- 📦 **Versioning**: Git tag-based version tracking

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   GitLab    │─────▶│   CI/CD      │─────▶│ Docker Registry │
│ Repository  │      │  Pipeline    │      │  (Private)      │
└─────────────┘      └──────────────┘      └────────┬────────┘
                                                     │
                                                     ▼
                                          ┌──────────────────┐
                                          │ Production Server│
                                          │  ┌────────────┐  │
                                          │  │  Gunicorn  │  │
                                          │  │ 4 Workers  │  │
                                          │  │   Flask    │  │
                                          │  └────────────┘  │
                                          └──────────────────┘
```

### Tech Stack

**Backend:**
- Python 3.11 (Alpine Linux)
- Flask 3.0
- Gunicorn 21.2

**DevOps:**
- Docker (Multi-stage build)
- GitLab CI/CD
- Docker Registry
- pytest + coverage

---

## 📚 API Documentation

### Generate Password

```bash
POST /api/generate
Content-Type: application/json

{
  "length": 16,
  "uppercase": true,
  "lowercase": true,
  "digits": true,
  "symbols": true
}
```

**Response:**
```json
{
  "success": true,
  "password": "aB3$xY9#mK2@pL5!",
  "length": 16,
  "options": {
    "uppercase": true,
    "lowercase": true,
    "digits": true,
    "symbols": true
  }
}
```

### Health Check

```bash
GET /health

# Response
{
  "status": "healthy",
  "service": "password-generator",
  "version": "v1.0.0",
  "timestamp": "2025-11-10T10:30:45"
}
```

### Version Info

```bash
GET /version

# Response
{
  "version": "v1.0.0",
  "service": "password-generator",
  "environment": "production"
}
```

---

## 🔄 CI/CD Pipeline

### Pipeline Stages

1. **Test Stage**
   - Run unit tests
   - Calculate coverage
   - Trigger: Every commit

2. **Build Stage**
   - Build Docker image
   - Push to registry
   - Tag: `dev-{sha}` or `v{version}`

3. **Deploy Stage** (Manual)
   - Pull latest image
   - Zero-downtime deployment
   - Health verification

4. **Integration Test Stage**
   - End-to-end API testing
   - Deployed service verification
   - Auto-fail on errors

5. **Cleanup Stage** (Manual)
   - Remove old images
   - Disk space optimization

### Rollback

```bash
# In GitLab Pipeline:
# 1. Run Pipeline
# 2. Add variable: ROLLBACK_TO=v1.0.0
# 3. Execute rollback:production job
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests (requires running service)
pytest tests/integration/ -v

# With coverage
pytest --cov=app --cov-report=html
```

### Test Structure

```
tests/
├── unit/                 # Unit tests (no service required)
│   ├── test_api.py
│   └── test_password_generator.py
└── integration/          # Integration tests (requires service)
    └── test_integration.py
```

**Coverage:** 85%+ on core logic

---

## 🐳 Docker

### Multi-Stage Build

```dockerfile
# Stage 1: Builder (build dependencies)
FROM python:3.11-alpine AS builder
# Install and compile dependencies

# Stage 2: Runtime (minimal image)
FROM python:3.11-alpine
COPY --from=builder /install /usr/local
# Final image: ~80MB
```

### Docker Compose

```yaml
services:
  web:
    build: .
    ports:
      - "8080:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - APP_VERSION=v1.0.0
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | - | Flask secret key (required in prod) |
| `DEBUG` | `False` | Debug mode |
| `PORT` | `5000` | Application port |
| `APP_VERSION` | `unknown` | Application version |
| `GUNICORN_WORKERS` | `CPU*2+1` | Number of workers |
| `LOG_LEVEL` | `info` | Logging level |

### Setup

```bash
# Copy example env file
cp .env.example .env

# Edit configuration
nano .env

# Set SECRET_KEY (required)
SECRET_KEY=your-super-secret-production-key
```

---

## 📦 Deployment

### Production Deployment

```bash
# 1. Create and push tag
git tag v1.0.0
git push origin v1.0.0

# 2. In GitLab:
#    - Pipeline starts automatically
#    - Tests run
#    - Docker image builds
#    - Click "deploy:production" to deploy

# 3. Verify
curl http://your-server:5000/health
```

### Manual Deployment

```bash
# Pull image
docker pull registry.example.com/password-generator:v1.0.0

# Run container
docker run -d \
  --name password-generator \
  --restart unless-stopped \
  -p 5000:5000 \
  -e SECRET_KEY="your-secret" \
  -e APP_VERSION="v1.0.0" \
  registry.example.com/password-generator:v1.0.0
```

---

## 🎯 Performance

### Benchmarks

- **Throughput**: ~500 requests/sec
- **Latency**: ~20ms (average)
- **Memory**: ~50MB per worker
- **CPU**: ~5% idle, ~40% under load

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:5000/api/generate

# Results:
# Requests per second: 500
# Failed requests: 0
```

---

## 🛡️ Security

### Implemented

✅ Cryptographically secure random generation (`secrets`)  
✅ Non-root container user  
✅ Input validation (length: 4-128)  
✅ Environment-based secrets  
✅ No hardcoded credentials  

### Production Recommendations

⚠️ Change `SECRET_KEY` to strong random value  
⚠️ Use HTTPS/TLS in production  
⚠️ Implement rate limiting  
⚠️ Use secure Docker registry with TLS  
⚠️ Regular security updates  

**Note:** This project uses insecure Docker registry for educational purposes only.

---

## 🚧 Roadmap

- [ ] Rate limiting with Redis
- [ ] API authentication (JWT)
- [ ] Prometheus metrics
- [ ] Nginx reverse proxy
- [ ] Kubernetes deployment
- [ ] Swagger/OpenAPI docs
- [ ] Password strength indicator
- [ ] Multi-language support

---

## 💻 Local Development

```bash
# Clone repository
git clone <repository-url>
cd password-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run development server
export DEBUG=True
python app.py

# Run tests
pytest -v
```

---

## 📊 Project Stats

- **Lines of Code**: ~500
- **Test Coverage**: 85%+
- **Docker Image Size**: ~80MB
- **Build Time**: ~2 minutes
- **Deployment Time**: ~30 seconds

---

## 🤝 Contributing

This is an educational DevOps project. Suggestions and improvements are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 👤 Author

**Your Name**

- GitHub: [@mfarajpour](https://github.com/mfarajpour)
- LinkedIn: 
- Email:

---

## 🙏 Acknowledgments

- Flask & Gunicorn documentation
- Docker best practices guides
- GitLab CI/CD community
- DevOps learning resources

---

## 📞 Support

If you have issues:

1. Check existing Issues
2. Create new Issue
3. Submit Pull Request

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ for Learning DevOps

</div>


---

