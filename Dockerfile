# Stage 1: Build frontend
FROM node:18 AS build-frontend
WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install && npm run build

# Stage 2: Backend with Python
FROM python:3.10-slim
WORKDIR /app

# Copy backend code
COPY backend/ ./
COPY --from=build-frontend /app/frontend/dist ./static

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
