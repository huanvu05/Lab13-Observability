# 🚀 Day 13 Observability Lab – Phân chia công việc (Team 2 người)

> Mục tiêu: chia việc **KHÔNG đụng file nhau**, mỗi người chịu trách nhiệm 1 layer rõ ràng.
> Ưu tiên: pass lab + dễ demo + đủ evidence báo cáo.

---

# 👥 Tổng quan phân công

| Người       | Role                          | Focus                            |
| ----------- | ----------------------------- | -------------------------------- |
| 👤 Member A | Logging & Middleware Engineer | Log chuẩn + Correlation ID + PII |
| 👤 Member B | Tracing & Metrics Engineer    | Tracing + Dashboard + Incident   |

---

# 🔵 👤 MEMBER A — Logging & Middleware (KHÔNG đụng Agent)

## 🎯 Mục tiêu

Làm cho **log đạt chuẩn production**:

* Có correlation_id
* Có context (user/session/feature)
* Không leak PII
* Pass script `validate_logs.py`

---

## 📂 File cần làm (CHỈ các file này)

### 1. `app/middleware.py`

👉 Nhiệm vụ:

* Generate correlation_id
* Bind context
* Add response headers

### 2. `app/main.py`

👉 Nhiệm vụ:

* Enrich logs bằng context user

### 3. `app/logging_config.py`

👉 Nhiệm vụ:

* Bật PII scrub

---

## 🛠️ Chi tiết cần làm

### ✅ 1. Middleware (bắt buộc)

Thêm:

* `clear_contextvars()`
* generate `correlation_id`
* `bind_contextvars()`
* add headers:

  * `x-request-id`
  * `x-response-time-ms`

---

### ✅ 2. Log enrichment

Trong `main.py`:

```python
bind_contextvars(
    user_id_hash=hash_user_id(body.user_id),
    session_id=body.session_id,
    feature=body.feature,
    model=agent.model,
    env=os.getenv("APP_ENV", "dev"),
)
```

---

### ✅ 3. PII Scrubbing

Trong `logging_config.py`:

```python
scrub_event,
```

---

## 🧪 Cách test

Chạy:

```bash
uvicorn app.main:app --reload
python scripts/load_test.py
python scripts/validate_logs.py
```

---

## 🎯 Tiêu chí đạt 10 điểm

| Tiêu chí         | Yêu cầu                                 |
| ---------------- | --------------------------------------- |
| JSON log chuẩn   | Không lỗi schema                        |
| Correlation ID   | ≥ 2 unique IDs                          |
| Log enrichment   | Có đủ user_id_hash, session_id, feature |
| PII              | Không còn email / phone / credit card   |
| validate_logs.py | ≥ 90/100                                |

---

## 📊 Có cần logs cho báo cáo không?

👉 CÓ (RẤT QUAN TRỌNG)

Bạn phải chụp:

* Log có `correlation_id`
* Log đã bị `[REDACTED_EMAIL]`
* Log có đủ field context

---

---

# 🟢 👤 MEMBER B — Tracing + Metrics + Dashboard

## 🎯 Mục tiêu

Làm cho system:

* Có trace trên Langfuse
* Có metrics rõ ràng
* Có dashboard 6 panel
* Debug được incident

---

## 📂 File cần làm (KHÔNG đụng file của Member A)

### 1. `.env`

👉 Thêm Langfuse key

### 2. KHÔNG sửa code core (agent đã xong)

👉 Chỉ:

* chạy
* quan sát
* demo

---

## 🛠️ Chi tiết cần làm

---

### ✅ 1. Tracing (Langfuse)

* Thêm:

```env
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

* Gửi request:

```bash
python scripts/load_test.py
```

👉 Kiểm tra:

* có ≥ 10 traces
* có:

  * latency
  * tokens
  * metadata


---

### ✅ 2. Metrics API

Gọi:

```
GET /metrics
```

👉 Lấy:

* latency_p95
* cost
* tokens
* error

---

### ✅ 3. Dashboard (6 panels)

Theo `docs/dashboard-spec.md`:

BẮT BUỘC:

1. Latency (p50/p95/p99)
2. Traffic
3. Error rate
4. Cost
5. Tokens
6. Quality score

👉 Có thể dùng:

* Excel
* Grafana
* hoặc vẽ tay (nếu demo đơn giản)

---

### ✅ 4. Incident simulation

Chạy:

```bash
python scripts/inject_incident.py --scenario rag_slow
python scripts/inject_incident.py --scenario tool_fail
python scripts/inject_incident.py --scenario cost_spike
```

---

### ✅ 5. Debug flow (QUAN TRỌNG)

Bạn phải giải thích được:

| Incident   | Dấu hiệu     |
| ---------- | ------------ |
| rag_slow   | latency tăng |
| tool_fail  | error tăng   |
| cost_spike | tokens tăng  |

---

## 🎯 Tiêu chí đạt 10 điểm

| Tiêu chí     | Yêu cầu                    |
| ------------ | -------------------------- |
| Traces       | ≥ 10 traces                |
| Trace đầy đủ | có metadata + usage        |
| Dashboard    | đủ 6 panels                |
| Metrics      | đọc được từ API            |
| Debug        | giải thích được root cause |

---

## 📊 Có cần logs không?

👉 KHÔNG cần xử lý logs
👉 NHƯNG cần dùng logs để:

* chứng minh error_type
* show correlation_id

---

---

# 🔥 Tổng hợp trách nhiệm (KHÔNG ĐỤNG FILE NHAU)

| Task       | Member A | Member B |
| ---------- | -------- | -------- |
| Middleware | ✅        | ❌        |
| Logging    | ✅        | ❌        |
| PII        | ✅        | ❌        |
| Tracing    | ❌        | ✅        |
| Metrics    | ❌        | ✅        |
| Dashboard  | ❌        | ✅        |
| Incident   | ❌        | ✅        |

---

# 🧠 Strategy để ăn điểm cao

👉 Làm đúng thứ tự:

### 1. Member A:

* Fix logs → PASS validate_logs

### 2. Member B:

* Generate traces + dashboard

### 3. Cả team:

* Demo 1 incident:

  * bật `rag_slow`
  * show:

    * metrics ↑
    * trace slow
    * log ok

👉 Đây là phần giảng viên thích nhất 🔥

---

# ⚡ Kết luận

* Lab này KHÔNG phải coding nhiều
* Nó là:

> 🔥 “Bạn debug system như 1 AI Engineer thật”

---

Nếu bạn muốn, mình có thể:
👉 viết sẵn code chuẩn cho Member A (pass 100/100 validate_logs)
👉 hoặc mock luôn dashboard + kịch bản demo nói gì để ăn điểm tối đa 😈
