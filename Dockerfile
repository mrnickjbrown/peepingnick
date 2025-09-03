# Stage 1: frontend build
FROM node:18 AS build-frontend
WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install && npm run build

# Stage 2: backend
FROM python:3.10-slim
WORKDIR /app
COPY backend/ ./backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build into backend
COPY --from=build-frontend /app/frontend/dist ./frontend/dist

EXPOSE 8080
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
