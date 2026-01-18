# NewsApp - Docker Setup Guide

This document provides detailed instructions for running NewsApp in Docker with an isolated Python virtual environment.

## Quick Start

### Using docker-compose (Recommended)

# Run with default settings (uses RSS feeds - no API key needed!)
docker-compose up -it

# Or, run with optional News API key for additional sources
export NEWS_API_KEY="your_api_key_here"
docker-compose up -it
```

### Using Docker directly

```bash
# Build the image
docker build -t terminal-news-app:latest .

# Run with default settings (RSS feeds, no API key needed)
docker run -it terminal-news-app:latest

# Or run with optional API key
docker run -it \
  -v ~/.newsapp:/app/.newsapp \
  -v ./config:/app/config \
  -e NEWS_API_KEY="your_api_key_here" \
  terminal-news-app:latest
```

### Using Docker directly

```bash
# Build the image
docker build -t terminal-news-app:latest .

# Run with interactive terminal
docker run -it \
  -v ~/.newsapp:/app/.newsapp \
  -v ./config:/app/config \
  -e NEWS_API_KEY="your_api_key_here" \
  terminal-news-app:latest
```

## Docker Architecture

### Base Image
- **Image**: `python:3.11-slim-bullseye`
- **Size**: ~150MB (slim variant for reduced footprint)
- **OS**: Debian Bullseye

### Virtual Environment
- **Location**: `/app/venv` inside container
- **Created during build**: Ensures reproducible builds
- **Automatically activated**: Entry point activates venv before running app

### Multi-Stage Build
```
Stage 1 (Builder):
  - Install build tools
  - Create virtual environment
  - Install Python dependencies

Stage 2 (Runtime):
  - Copy venv from builder
  - Install runtime dependencies only
  - Copy application code
  - Smaller final image
```

## Volume Mounts

### Volumes Used

| Volume/Mount | Purpose | Permissions | Location |
|---|---|---|---|
| `newsapp-data` | Cache, logs, user config | Read/Write | `/app/.newsapp` |
| `newsapp-logs` | Application logs | Read/Write | `/app/logs` |
| `./config` | Configuration files | Read-only | `/app/config` |

### Persistent Storage

```bash
# Create local directories (optional, auto-created by Docker)
mkdir -p ~/.newsapp
mkdir -p ./config

# Run with mounted volumes
docker-compose up -d
```

Your configuration and cache will persist in:
- **Host**: `~/.newsapp/` → **Container**: `/app/.newsapp/`
- **Host**: `./config/` → **Container**: `/app/config/` (read-only)

## Environment Variables

### Required
- `NEWS_API_KEY` - Your News API key

### Optional
- `DEBUG` - Set to `true` for debug logging (default: `false`)
- `CONFIG_PATH` - Path to config file (default: `/app/config/config.yaml`)
- `PYTHONUNBUFFERED` - Already set to `1` in Dockerfile

### Setting Environment Variables

**Option 1: Command line**
```bash
docker run -it \
  -e NEWS_API_KEY="your_key" \
  -e DEBUG="true" \
  terminal-news-app:latest
```

**Option 2: .env file (with docker-compose)**
```bash
# Create .env file
cat > .env << EOF
NEWS_API_KEY=your_api_key_here
DEBUG=false
EOF

# Run
docker-compose up -d
```

**Option 3: Modify docker-compose.yml**
```yaml
environment:
  - NEWS_API_KEY=your_api_key_here
  - DEBUG=false
```

## Running the Application

### Interactive Mode
```bash
# Best for testing and interactive use
docker-compose run -it terminal-news-app
```

### Background Mode
```bash
# Run in background (not typical for terminal UI app)
docker-compose up -d

# View logs
docker-compose logs -f terminal-news-app
```

### Custom Commands
```bash
# Run with custom arguments
docker run -it terminal-news-app python -m src.main --help

# Run tests (if available)
docker run -it terminal-news-app pytest tests/
```

## Building the Image

### Build Options

**Standard build (Dockerfile only)**
```bash
docker build -t newsapp:latest .
docker build -t newsapp:0.1.0 .
```

**With build arguments**
```bash
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  -t newsapp:latest \
  .
```

**With docker-compose**
```bash
docker-compose build
docker-compose build --no-cache  # Rebuild without cache
```

### Build Output
- **Final image size**: ~400-500MB (with dependencies)
- **Build time**: ~2-3 minutes (first time), <30 seconds (cached)
- **Python version**: 3.11

## Managing Containers

### Container Operations

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs terminal-news-app
docker logs -f terminal-news-app  # Follow logs

# Execute command in running container
docker exec -it terminal-news-app bash

# Stop container
docker stop terminal-news-app

# Start stopped container
docker start terminal-news-app

# Restart container
docker restart terminal-news-app

# Remove container
docker rm terminal-news-app

# Remove image
docker rmi terminal-news-app:latest
```

### Cleaning Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

## Troubleshooting

### Issue: API Key not working
```bash
# Verify environment variable is set
docker exec terminal-news-app env | grep NEWS_API_KEY

# Check logs for API errors
docker-compose logs -f terminal-news-app
```

### Issue: Cache/config not persisting
```bash
# Verify volume mounts
docker inspect terminal-news-app | grep -A 10 Mounts

# Check volume existence
docker volume ls | grep newsapp

# Recreate volumes if needed
docker-compose down -v  # WARNING: Deletes data!
docker-compose up -d
```

### Issue: Container won't start
```bash
# Check container logs
docker-compose logs terminal-news-app

# Check Docker daemon
docker version

# Verify image was built
docker images | grep terminal-news-app
```

### Issue: Permission denied errors
```bash
# The container runs as non-root user (appuser:1000)
# Ensure volume directories are accessible

# Fix permissions on host
chmod -R 755 ~/.newsapp
chmod -R 755 ./config
```

### Issue: Out of memory
```bash
# Increase Docker memory limit
# In docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 1024M  # Increase from 512M
```

## Performance Tuning

### Resource Limits (docker-compose)
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

### Network Optimization
```bash
# Use host network (Linux only)
docker run --network host ...

# Custom DNS
docker run --dns 8.8.8.8 ...
```

### Caching Optimization
- The Dockerfile uses multi-stage build to reduce image size
- Dependencies are cached in venv and reused across container restarts
- Use `--no-cache` flag to rebuild without using cache

## Docker Registries

### Pushing to Docker Hub
```bash
# Tag image
docker tag terminal-news-app:latest username/terminal-news-app:latest
docker tag terminal-news-app:latest username/terminal-news-app:0.1.0

# Push to registry
docker push username/terminal-news-app:latest
docker push username/terminal-news-app:0.1.0
```

### Pulling from registry
```bash
# Run directly from registry
docker run -it username/terminal-news-app:latest
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Build and Push Docker Image

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: username/terminal-news-app:latest
```

## Development Workflow

### Development Container
```bash
# Mount source code for live editing
docker run -it \
  -v $(pwd)/src:/app/src \
  -v ~/.newsapp:/app/.newsapp \
  terminal-news-app:latest
```

### Entering Container Shell
```bash
# Open bash in running container
docker-compose exec terminal-news-app bash

# Run Python interactively
docker-compose exec terminal-news-app python
```

### Hot Reload (if applicable)
```bash
# Use volume mount to reflect source changes
docker-compose.override.yml:
volumes:
  - ./src:/app/src
```

## Best Practices

1. **Always use docker-compose** for consistency
2. **Set NEWS_API_KEY** before running
3. **Use read-only volumes** for configuration (`:ro` flag)
4. **Monitor resource usage**: `docker stats`
5. **Regular cleanup**: `docker system prune`
6. **Keep image size minimal**: Use slim base image
7. **Don't run as root**: Container uses `appuser`
8. **Use health checks**: Already configured in Dockerfile
9. **Log rotation**: Configured in docker-compose
10. **Version your images**: Tag with version numbers

## Further Reading

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
