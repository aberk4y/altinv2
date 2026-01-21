# Build Stage for Frontend
FROM node:18-alpine as build-frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Production Stage
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy Backend
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
# Copy Frontend Build from previous stage
COPY --from=build-frontend /app/frontend/build ./frontend/build

# Expose port (Koyeb uses 8000 by default but we can config)
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]
