# CI/CD & Cloud Observability Demo

Project demo gồm React frontend và FastAPI backend, dùng để minh họa một ứng dụng sẵn sàng đưa vào CI/CD pipeline và có các tín hiệu observability cơ bản: health check, version, JSON log và Prometheus metrics.

## Kiến trúc

```text
Browser → React/Vite (port 3000 hoặc 5173)
              ↓ /api (Nginx/Vite proxy)
          FastAPI (port 8080) → JSON logs (stdout)
              ↓
          /metrics (Prometheus format)
```

- `frontend/`: dashboard React, build bằng Vite, production serve bằng Nginx.
- `backend/`: REST API FastAPI, observability middleware và pytest.
- `docker-compose.yml`: build và chạy cả hai service.

## Chạy backend local

Yêu cầu Python 3.10 trở lên.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Có thể cấu hình bằng `PORT` (mặc định `8080`), `APP_VERSION` (mặc định `v1.0.0`) và `SERVICE_NAME` (mặc định `backend`). Khi chạy Uvicorn trực tiếp, truyền `$PORT` vào tham số `--port` nếu muốn đổi cổng.

Chạy test (không cần external service):

```bash
cd backend
pytest
```

## Chạy frontend local

Yêu cầu Node.js LTS. Vite proxy request `/api` tới `http://localhost:8080` khi phát triển local.

```bash
cd frontend
npm install
npm run dev
```

Mở `http://localhost:5173`. Có thể đổi backend URL phía browser bằng biến build-time `VITE_API_BASE_URL`, nhưng production nên giữ rỗng để dùng proxy same-origin.

Khi deploy Kubernetes, frontend Nginx proxy `/api` tới `http://backend:8080` theo mặc định. Service backend cần có tên `backend` và port `8080`. Nếu tên hoặc port khác, đặt biến runtime `BACKEND_URL` trong frontend Deployment, ví dụ `http://backend-service:8080`. Không đặt tên Kubernetes Service vào `VITE_API_BASE_URL`, vì biến đó chạy trong browser và cluster DNS không khả dụng ở đó.

## Chạy bằng Docker Compose

Từ thư mục gốc project:

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8080
- Swagger UI: http://localhost:8080/docs

Dừng stack bằng `docker compose down`.

## Backend API

| Method | Endpoint | Mục đích |
| --- | --- | --- |
| GET | `/api/health` | Trạng thái, service và version |
| GET | `/api/version` | Version đang triển khai |
| GET | `/api/message` | Message demo |
| GET | `/api/items` | Danh sách chủ đề DevOps |
| GET | `/api/error` | Luôn trả HTTP 500 để demo lỗi |
| GET | `/metrics` | Prometheus metrics |

## Prometheus metrics

Mở http://localhost:8080/metrics hoặc chạy:

```bash
curl http://localhost:8080/metrics
```

Các metric chính gồm `http_requests_total`, `http_request_duration_seconds`, `http_errors_total` và `app_info`. Request scrape `/metrics` không được tính vào HTTP metrics để tránh self-noise.

## Kịch bản demo

1. Chạy ứng dụng bằng Docker Compose và mở http://localhost:3000.
2. Bấm các nút để kiểm tra health, version, message và items.
3. Bấm **Trigger Error** để tạo response HTTP 500.
4. Xem JSON request log bằng `docker compose logs backend`.
5. Mở http://localhost:8080/metrics, tìm status `500` trong `http_requests_total` và `http_errors_total`.

## Minh họa CI/CD và Observability

Mỗi service có Dockerfile độc lập, dependency và test tách rõ nên CI có thể chạy test/build theo service, tạo immutable image rồi triển khai cùng `APP_VERSION` của release. API `/api/health` phục vụ health probe; `/api/version` và `app_info` giúp xác định build đang chạy.

Middleware tạo request ID, ghi structured JSON log và đo request count, latency, error rate. Ba tín hiệu này hỗ trợ dashboard, alert và điều tra sự cố sau deploy; header `x-request-id` giúp liên kết request từ frontend hoặc gateway với backend log.
