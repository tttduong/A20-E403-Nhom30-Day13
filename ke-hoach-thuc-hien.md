# Kế hoạch thực hiện — Day 13 Observability Lab

> Nhóm 30 | Lớp A20-E403 | Mô hình chấm: **60 điểm Nhóm / 40 điểm Cá nhân**

---

## Bảng phân công tổng quan

| Thành viên | Vai trò | File chính | Điểm cá nhân liên quan |
|---|---|---|---|
| **A** | Logging & PII | `app/middleware.py`, `app/logging_config.py`, `app/pii.py` | B1 + B2 (40đ) |
| **B** | Tracing & Enrichment | `app/main.py`, `app/tracing.py`, `app/agent.py` | B1 + B2 (40đ) |
| **C** | SLO & Alerts | `config/slo.yaml`, `config/alert_rules.yaml`, `docs/alerts.md` | B1 + B2 (40đ) |
| **D** | Load Test & Dashboard | `scripts/load_test.py`, `scripts/inject_incident.py` | B1 + B2 (40đ) |
| **E** | Demo & Report | `docs/blueprint-template.md`, `docs/grading-evidence.md` | B1 + B2 (40đ) |

---

## Thứ tự ưu tiên thực hiện

```
Bước 1 (Member A) → Bước 2 (Member B) → Bước 3 (Member C + D song song) → Bước 4 (Member E)
```

> **Lý do**: B phụ thuộc A (cần correlation_id đã bind trước khi enrich context). C và D độc lập nhau. E tổng hợp sau cùng.

---

## Member A — Logging & PII

**Mục tiêu**: Đảm bảo mọi request đều có correlation ID duy nhất và không lộ PII trong logs.

### Checklist chi tiết

- [ ] **[middleware.py:13]** Gọi `clear_contextvars()` đầu hàm `dispatch()` để tránh rò context giữa các request
- [ ] **[middleware.py:16]** Extract `x-request-id` từ header, nếu không có thì sinh `req-<8 ký tự hex ngẫu nhiên>`
- [ ] **[middleware.py:20]** Gọi `bind_contextvars(correlation_id=correlation_id)` để gắn ID vào structlog context
- [ ] **[middleware.py:28]** Thêm 2 response header: `x-request-id` và `x-response-time-ms` (tính bằng ms)
- [ ] **[logging_config.py:45]** Uncomment / thêm `scrub_event` vào danh sách processors của structlog
- [ ] **[pii.py:11]** Thêm regex cho Passport (VN: `[A-Z]\d{7}`), CMND/CCCD (`\d{9}|\d{12}`), địa chỉ VN (từ khóa: `"phường"`, `"quận"`, `"thành phố"`)

### Code gợi ý

```python
# middleware.py — dispatch()
clear_contextvars()
correlation_id = request.headers.get("x-request-id") or f"req-{secrets.token_hex(4)}"
bind_contextvars(correlation_id=correlation_id)
# ... sau khi có response:
response.headers["x-request-id"] = correlation_id
response.headers["x-response-time-ms"] = str(round((time.perf_counter() - start) * 1000, 2))
```

### Bằng chứng cần nộp (commit)
- Screenshot log line có `"correlation_id": "req-xxxxxxxx"`
- Screenshot log line **không** có email/số thẻ rõ ràng (đã redact)
- Link commit cụ thể cho từng file đã sửa

---

## Member B — Tracing & Enrichment

**Mục tiêu**: Mỗi log request đều mang đầy đủ context (user, session, feature, model). Có ít nhất 10 traces trên Langfuse.

### Checklist chi tiết

- [ ] **[main.py:47]** Thêm `bind_contextvars()` với các field: `user_id_hash`, `session_id`, `feature`, `model`, `env`
- [ ] Kiểm tra `app/agent.py` đã có decorator `@observe` trên hàm chạy pipeline chưa — nếu chưa thì thêm
- [ ] Kiểm tra `app/tracing.py` đã khởi tạo Langfuse client đúng từ `.env` chưa
- [ ] Chạy `python scripts/load_test.py --concurrency 5` để sinh ít nhất 20 requests
- [ ] Vào Langfuse UI xác nhận ≥10 traces hiển thị với đầy đủ spans (RAG, LLM, tool)
- [ ] Chụp **trace waterfall screenshot** của 1 trace tiêu biểu

### Code gợi ý

```python
# main.py — trong endpoint /query, sau khi parse body
bind_contextvars(
    user_id_hash=hashlib.sha256(body.user_id.encode()).hexdigest()[:12],
    session_id=body.session_id,
    feature=body.feature,
    model=body.model,
    env=settings.ENV,
)
```

### Bằng chứng cần nộp (commit)
- Log line có `"user_id_hash"`, `"session_id"`, `"feature"`, `"model"` trong JSON
- Screenshot Langfuse hiện ≥10 traces với waterfall đầy đủ
- Giải thích được 1 span thú vị (ví dụ: span RAG lâu bất thường)

---

## Member C — SLO & Alerts

**Mục tiêu**: 3 alert rules hoạt động với runbook link hợp lệ. SLO table được điền đầy đủ với số liệu thực.

### Checklist chi tiết

- [ ] Đọc kỹ `config/alert_rules.yaml` — xác nhận 3 rules đã đúng cú pháp
- [ ] Đảm bảo mỗi alert có trường `runbook:` trỏ đúng đến section trong `docs/alerts.md`
  - `high_latency_p95` → `docs/alerts.md#high-latency-p95`
  - `high_error_rate` → `docs/alerts.md#high-error-rate`
  - `cost_budget_spike` → `docs/alerts.md#cost-budget-spike`
- [ ] Điền SLO table trong `docs/blueprint-template.md` (section 3.2) với giá trị thực đo được sau khi Member D chạy load test
- [ ] Chụp screenshot alert rules (từ Grafana hoặc config file)
- [ ] (Bonus +2đ) Thêm alert rule thứ 4 tùy chọn (ví dụ: quality_score thấp)

### Giá trị SLO cần điền

| SLI | Target | Window | Current Value (điền sau load test) |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | _đo từ metrics_ |
| Error Rate | < 2% | 28d | _đo từ logs_ |
| Cost Budget | < $2.5/day | 1d | _đo từ traces_ |

### Bằng chứng cần nộp (commit)
- File `config/alert_rules.yaml` với runbook links hợp lệ
- Screenshot alert rules đã cấu hình
- SLO table đã điền số liệu thực

---

## Member D — Load Test & Dashboard

**Mục tiêu**: Sinh đủ dữ liệu thực, xây dashboard 6 panel đúng spec, ghi lại incident response.

### Checklist chi tiết

- [ ] Chạy load test baseline: `python scripts/load_test.py --concurrency 5` (ít nhất 100 requests)
- [ ] Inject incident: `python scripts/inject_incident.py --scenario rag_slow`
- [ ] Ghi lại **symptoms quan sát được** (latency tăng? error rate tăng? logs bất thường?)
- [ ] Xác định root cause và điền vào section 4 của `blueprint-template.md`
- [ ] Xây dashboard với đúng **6 panels** theo `docs/dashboard-spec.md`:
  1. Latency P50 / P95 / P99
  2. Traffic (request count / QPS)
  3. Error rate với breakdown
  4. Cost over time
  5. Tokens in / out
  6. Quality proxy (heuristic score)
- [ ] Mỗi panel phải có: đơn vị rõ ràng, SLO threshold line, auto-refresh 15-30s
- [ ] Chụp screenshot dashboard đủ 6 panels

### Incident Response cần ghi lại

```
Scenario: rag_slow
Symptoms: (ví dụ) P95 latency tăng từ 800ms lên >5000ms, RAG span chiếm >90% tổng thời gian
Root cause: Inject toggle rag_slow làm mock RAG thêm delay nhân tạo
Trace/Log evidence: Trace ID xxx, span "rag_retrieval" duration = 4500ms
Fix: Tắt toggle, cân nhắc timeout + fallback retrieval
Prevention: Alert high_latency_p95 kích hoạt sau 30m
```

### Bằng chứng cần nộp (commit)
- Screenshot dashboard 6 panels
- Ghi chú incident response trong blueprint-template.md section 4

---

## Member E — Demo & Report

**Mục tiêu**: Blueprint report hoàn chỉnh, validate_logs ≥80/100, demo live mượt mà.

### Checklist chi tiết

- [ ] Điền **tất cả** các tag `[...]` trong `docs/blueprint-template.md`:
  - `[GROUP_NAME]`, `[REPO_URL]`, `[MEMBERS]` (tên thật 5 người)
  - `[VALIDATE_LOGS_FINAL_SCORE]` — chạy `python scripts/validate_logs.py` lấy số
  - `[TOTAL_TRACES_COUNT]` — đếm từ Langfuse
  - `[PII_LEAKS_FOUND]` — lấy từ output validate_logs
  - Tất cả `[EVIDENCE_*_SCREENSHOT]` — điền đường dẫn ảnh thực tế
  - Tất cả `[MEMBER_*_NAME]`, `[TASKS_COMPLETED]`, `[EVIDENCE_LINK]`
- [ ] Điền `docs/grading-evidence.md` với link commit/PR cụ thể của từng thành viên
- [ ] Chuẩn bị kịch bản demo live (thứ tự: chạy app → gửi request → xem logs → xem traces → xem dashboard → demo alert)
- [ ] Chuẩn bị trả lời câu hỏi từ `docs/mock-debug-qa.md`
- [ ] Chạy lần cuối `python scripts/validate_logs.py` — phải đạt **≥80/100**

### Script kiểm tra cuối

```bash
# Chạy validate và lưu output
python scripts/validate_logs.py | tee validate_output.txt

# Kiểm tra điều kiện passing
grep "Final score" validate_output.txt
```

### Bằng chứng cần nộp
- File `docs/blueprint-template.md` đã điền đầy đủ (commit)
- Output `validate_logs.py` ≥80/100

---

## Điều kiện PASSING (bắt buộc)

| Điều kiện | Kiểm tra bởi |
|---|---|
| `validate_logs.py` ≥ 80/100 | Member E chạy, cả nhóm xác nhận |
| ≥ 10 traces live trên Langfuse | Member B |
| Dashboard đủ 6 panels | Member D |
| Blueprint report đầy đủ tên thành viên | Member E |
| Tất cả TODO blocks được hoàn thành | Member A + B |

---

## Timeline gợi ý (4 giờ lab)

| Thời gian | Việc làm |
|---|---|
| 0:00 – 0:30 | Đọc README, setup `.env`, chạy app lần đầu, phân chia task |
| 0:30 – 1:30 | **A** implement middleware + PII; **B** implement enrichment + verify tracing |
| 1:00 – 2:00 | **C** hoàn thiện alert rules + runbook; **D** chạy load test + inject incident |
| 1:30 – 2:30 | **D** xây dashboard; **B** chụp Langfuse screenshots |
| 2:30 – 3:00 | **E** điền blueprint report; **A** chạy validate_logs lần đầu |
| 3:00 – 3:30 | Cả nhóm fix lỗi còn lại, validate_logs phải ≥80 |
| 3:30 – 4:00 | Rehearsal demo, chuẩn bị Q&A |

---

## Bonus (nếu có thời gian)

| Bonus | Thành viên thực hiện | Điểm |
|---|---|---|
| Tối ưu chi phí (số liệu trước/sau) | D | +3đ |
| Dashboard đẹp/chuyên nghiệp | D | +3đ |
| Auto-instrumentation / script custom | B | +2đ |
| Audit logs tách riêng (`data/audit.jsonl`) | A | +2đ |
