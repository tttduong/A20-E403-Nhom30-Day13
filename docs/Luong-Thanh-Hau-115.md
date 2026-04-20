# Báo cáo Cá nhân — Day 13 Observability Lab

| Thông tin | Chi tiết |
|---|---|
| **Họ và tên** | Lương Thanh Hậu |
| **Mã sinh viên** | 115 |
| **Vai trò trong nhóm** | Member E — Demo & Report |
| **Nhóm** | Nhóm 30 — A20-E403 |
| **Repo** | https://github.com/haubelerche/A20-E403-Nhom30-Day13 |
| **Branch cá nhân** | `hault115` |
| **Commit chính** | `cbd536d` — `feat(member-E): hoan thien blueprint, grading-evidence, mock-debug-qa` |

---

## 1. Nhiệm vụ được phân công

Theo kế hoạch nhóm, Member E chịu trách nhiệm **Demo & Report** — tổng hợp toàn bộ kết quả của nhóm, đảm bảo báo cáo hoàn chỉnh và hệ thống sẵn sàng demo live trước giảng viên.

### Checklist nhiệm vụ

| # | Nhiệm vụ | Trạng thái |
|---|---|:---:|
| 1 | Điền tất cả tag `[...]` còn trống trong `docs/blueprint-template.md` | ✅ Hoàn thành |
| 2 | Cập nhật `docs/grading-evidence.md` với link commit/PR cụ thể của 5 thành viên | ✅ Hoàn thành |
| 3 | Tạo `docs/mock-debug-qa.md` — kịch bản Q&A cho demo live | ✅ Hoàn thành |
| 4 | Chạy `python scripts/validate_logs.py` lần cuối — xác nhận ≥ 80/100 | ✅ Đạt **100/100** |
| 5 | Soạn kịch bản demo live (thứ tự 7 bước) | ✅ Hoàn thành |

---

## 2. Các file đã tạo / chỉnh sửa

### 2.1 `docs/blueprint-template.md` — Hoàn thiện báo cáo nhóm

**Vấn đề ban đầu:** Nhiều tag `[...]` vẫn còn placeholder chưa được điền sau khi các thành viên A, B, C, D hoàn thành phần kỹ thuật của mình.

**Những gì tôi đã làm:**

- **§2 — Group Performance**: Điền `[TOTAL_TRACES_COUNT]` (≥ 20 traces xác nhận từ Langfuse sau load test)
- **§3.1 — Logging & Tracing**: Điền đường dẫn screenshot thực tế:
  - `[EVIDENCE_CORRELATION_ID_SCREENSHOT]` → `docs/evidence/correlation-id.png`
  - `[EVIDENCE_PII_REDACTION_SCREENSHOT]` → `docs/evidence/pii-redaction.png`
  - `[EVIDENCE_TRACE_WATERFALL_SCREENSHOT]` → `docs/evidence/trace-waterfall.png`
  - `[TRACE_WATERFALL_EXPLANATION]` → Viết giải thích span `rag_retrieval` bất thường khi inject `rag_slow`
- **§5 — Individual Contributions**: Điền tên thật, task cụ thể và commit link cho tất cả 5 thành viên (A, B, C, D, E)
- Sửa `[MEMBER_E_NAME]` → `[Lương Thanh Hậu]` và điền đầy đủ tasks
- Cập nhật `[EVIDENCE_LINK]` của Member D từ đường dẫn ảnh → commit URL chính xác

### 2.2 `docs/grading-evidence.md` — Bảng bằng chứng toàn nhóm

Viết lại toàn bộ file với **5 section riêng biệt** cho từng thành viên, mỗi section gồm:
- Bảng chi tiết file đã làm + trạng thái
- Đường dẫn screenshot bằng chứng
- Link commit Git cụ thể trên GitHub

**Link commit của từng thành viên đã xác minh:**

| Thành viên | Commit |
|---|---|
| Tạ Thị Thuỳ Dương (A) | `0228cf5` — "duong, Logging & PII" |
| Nguyễn Thị Thu Hiền (B) | `a3aa355` — "feat: update main.py" |
| Hồ Quang Hiển (C) | `80f1a71` — "member hqh" |
| Trịnh Đức An (D) | `b9bea5e` — "taskD" |
| Lương Thanh Hậu (E) | `cbd536d` — "feat(member-E): hoan thien..." |

### 2.3 `docs/mock-debug-qa.md` — Tài liệu chuẩn bị demo (Tạo mới)

Soạn **17 câu hỏi + đáp án chi tiết** theo từng phần kỹ thuật, giúp cả nhóm chuẩn bị trả lời câu hỏi của giảng viên:

| Phần | Số câu | Chủ đề |
|---|:---:|---|
| Logging & Correlation ID | Q1–Q4 | clear_contextvars, x-request-id, PII regex |
| Tracing & Enrichment | Q5–Q7 | Langfuse waterfall, user_id_hash, @observe |
| SLO & Alerts | Q8–Q10 | SLI/SLO/SLA, ngưỡng alert, runbook |
| Load Test & Incident | Q11–Q12 | Flow phát hiện rag_slow, 6 dashboard panels |
| Demo & Report | Q13–Q15 | validate_logs, debug flow, 3 pillars |
| Bonus | Q16–Q17 | Structured vs unstructured, trace sampling |

### 2.4 `ke-hoach-thuc-hien.md` — Kế hoạch phân công nhóm

Ghi lại kế hoạch phân công chi tiết cho 5 thành viên, bao gồm checklist từng bước, code gợi ý và bằng chứng cần nộp.

---

## 3. Kết quả `validate_logs.py`

```
--- Lab Verification Results ---
Total log records analyzed: 99
Records with missing required fields: 0
Records with missing enrichment (context): 0
Unique correlation IDs found: 44
Potential PII leaks detected: 0

--- Grading Scorecard (Estimates) ---
+ [PASSED] Basic JSON schema
+ [PASSED] Correlation ID propagation
+ [PASSED] Log enrichment
+ [PASSED] PII scrubbing

Estimated Score: 100/100
```

Tất cả 4 tiêu chí đều **PASSED** — nhóm đạt **100/100**, vượt điều kiện passing (≥ 80/100).

---

## 4. Kịch bản Demo Live

Thứ tự demo trước giảng viên (7 bước):

| Bước | Hành động | Điểm cần chỉ ra |
|:---:|---|---|
| 1 | `uvicorn app.main:app --reload` | App khởi động không lỗi |
| 2 | `python scripts/load_test.py --concurrency 5` | Sinh ≥ 100 requests song song |
| 3 | Mở `data/logs.jsonl` | Chỉ `"correlation_id": "req-xxxx"` và `"user_id_hash"` trong JSON |
| 4 | Mở Langfuse UI | Chỉ ≥ 20 traces, waterfall spans (RAG, LLM) |
| 5 | Mở dashboard 6 panels | Chỉ SLO threshold lines, P95 < 3000ms, cost < $2.5/ngày |
| 6 | `python scripts/inject_incident.py --scenario rag_slow` | P95 tăng vọt → alert `high_latency_p95` kích hoạt |
| 7 | `POST /incidents/rag_slow/disable` | Latency trở về bình thường → giải thích runbook |

---

## 5. Hiểu sâu về phần việc đảm nhận (B1 — Individual Report Quality)

### Tại sao vai trò Demo & Report quan trọng?

Trong một hệ thống observability thực tế, giá trị của toàn bộ hạ tầng (logs, traces, dashboard, alerts) chỉ được hiện thực hóa khi **người dùng cuối hiểu và tin tưởng vào dữ liệu đó**. Member E đóng vai trò này:

1. **Tổng hợp cross-cutting**: Không thành viên nào có đủ ngữ cảnh toàn cục — Member E là người duy nhất đọc và hiểu output của cả 4 thành viên còn lại để tạo ra báo cáo nhất quán.

2. **Quality gate cuối cùng**: `validate_logs.py` là automated check, nhưng Member E là người quyết định *giải thích* kết quả đó — 100/100 không chỉ có nghĩa là kỹ thuật đúng, mà còn là toàn bộ pipeline (middleware → structlog → PII scrub → JSON output) hoạt động end-to-end.

3. **Demo script = runbook thực tế**: Kịch bản demo 7 bước tôi soạn không chỉ dùng cho lab — nó phản ánh quy trình on-call thực tế: khi có incident, engineer cần biết *đúng thứ tự* nhìn vào đâu (Metrics → Traces → Logs → Runbook → Fix → Verify).

### Giải thích kỹ thuật: validate_logs.py hoạt động như thế nào?

Script đọc `data/logs.jsonl` và kiểm tra từng dòng JSON theo 4 tiêu chí:

```python
# Tiêu chí 1: Basic schema
if not {"ts", "level", "event"}.issubset(rec.keys()):
    missing_required += 1

# Tiêu chí 2: Correlation ID (chỉ áp dụng cho service=api)
if rec.get("service") == "api":
    if "correlation_id" not in rec or rec.get("correlation_id") == "MISSING":
        missing_required += 1

# Tiêu chí 3: Enrichment fields (chỉ cho service=api)
    if not ENRICHMENT_FIELDS.issubset(rec.keys()):
        missing_enrichment += 1

# Tiêu chí 4: PII check (naive — tìm @ hoặc "4111")
raw = json.dumps(rec)
if "@" in raw or "4111" in raw:
    pii_hits.append(rec.get("event", "unknown"))
```

**Điểm quan trọng tôi nhận ra khi review**: Script chỉ check `@` và `4111` (test Visa card) — đây là *minimum bar*. PII scrubber của nhóm đã implement thêm regex cho Passport VN, CMND, địa chỉ — vượt yêu cầu của script nhưng cần thiết cho production.

### Giải thích: Tại sao "3 pillars of observability"?

- **Metrics**: Số tổng hợp theo thời gian (P95 latency, QPS, error rate) — nhanh, rẻ, cho biết *có vấn đề không*
- **Logs**: Sự kiện rời rạc với đầy đủ context — chậm hơn, đắt hơn, cho biết *chuyện gì xảy ra*
- **Traces**: Luồng thực thi qua nhiều service/hàm — cho biết *mất thời gian ở đâu*

Trong lab này, flow debug incident `rag_slow` minh họa rõ cả 3: Dashboard (metrics) báo hiệu → Langfuse (traces) chỉ ra span nào chậm → Logs xác nhận thời điểm toggle được bật.

---

## 6. Bằng chứng Git

| File | Loại thay đổi | Commit |
|---|---|---|
| `docs/blueprint-template.md` | Modified | `cbd536d` |
| `docs/grading-evidence.md` | Modified | `cbd536d` |
| `docs/mock-debug-qa.md` | Created | `cbd536d` |
| `ke-hoach-thuc-hien.md` | Created | `cbd536d` |

**Link commit:** https://github.com/haubelerche/A20-E403-Nhom30-Day13/commit/cbd536d

**Branch:** https://github.com/haubelerche/A20-E403-Nhom30-Day13/tree/hault115

---

## 7. Tự đánh giá

| Hạng mục rubric | Tự chấm | Lý do |
|---|:---:|---|
| **B1 — Individual Report** | 18/20 | Báo cáo đầy đủ, có giải thích kỹ thuật sâu; trừ 2đ vì trace waterfall screenshot cần chụp thêm từ Langfuse UI thực |
| **B2 — Git Evidence** | 19/20 | Commit rõ ràng, 4 files; trừ 1đ vì chưa tạo PR chính thức vào main |
| **Tổng cá nhân** | **37/40** | |

> **Ghi chú**: Điểm nhóm phụ thuộc vào toàn bộ hệ thống — validate_logs 100/100, dashboard 6 panels, ≥10 traces, alert rules đã cấu hình → ước tính đóng góp vào Group Score đầy đủ.
