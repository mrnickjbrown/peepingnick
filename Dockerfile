# ---- Frontend build ----
FROM node:18 AS build-frontend
WORKDIR /frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# ---- Backend ----
FROM python:3.10-slim
WORKDIR /app

# Install backend dependencies
COPY backend/ ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend into /static
COPY --from=build-frontend /frontend/dist ./static

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
