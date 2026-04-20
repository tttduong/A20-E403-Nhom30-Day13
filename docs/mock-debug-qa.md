# Mock Debug Q&A — Demo Prep (Day 13 Observability Lab)

> Danh sách câu hỏi giảng viên thường hỏi trong buổi demo. Mỗi thành viên nên thuộc phần mình phụ trách.

---

## Phần 1 — Logging & Correlation ID (Member A)

**Q1: Correlation ID là gì và tại sao cần nó?**
> Correlation ID là một chuỗi định danh duy nhất gắn vào mỗi HTTP request và được truyền qua tất cả các log liên quan. Nó cho phép engineer truy vết toàn bộ vòng đời của một request qua hệ thống phân tán mà không cần grep thủ công. Trong lab này, giá trị dạng `req-<8 hex chars>` được bind vào structlog context để mọi log entry trong cùng request đều mang cùng `correlation_id`.

**Q2: Nếu client gửi header `x-request-id`, hệ thống xử lý thế nào?**
> Middleware kiểm tra header `x-request-id` trong incoming request. Nếu có, giá trị đó được dùng làm correlation ID (cho phép distributed tracing end-to-end từ phía client). Nếu không có, system tự sinh `req-{secrets.token_hex(4)}`.

**Q3: PII scrubbing hoạt động như thế nào trong code?**
> Hàm `scrub_event` trong `app/pii.py` chạy regex trên toàn bộ serialized event trước khi log ra. Nó redact: email (`\S+@\S+`), số thẻ tín dụng (pattern Luhn-like), Passport VN (`[A-Z]\d{7}`), CMND/CCCD (`\d{9}|\d{12}`), và địa chỉ chứa từ khóa "phường/quận/thành phố". Processor này được đăng ký trong chain của structlog, chạy trước khi format JSON.

**Q4: Tại sao cần gọi `clear_contextvars()` đầu mỗi request?**
> Structlog lưu context trong thread-local (hoặc async context var). Nếu không clear, context của request trước có thể "rò" vào request sau — đặc biệt nguy hiểm với async frameworks như FastAPI vì worker reuse. `clear_contextvars()` đảm bảo mỗi request bắt đầu với slate trắng.

---

## Phần 2 — Tracing & Enrichment (Member B)

**Q5: Trace waterfall trong Langfuse cho thấy gì?**
> Trace waterfall hiển thị timeline các spans của một request: span `rag_retrieval` (tìm kiếm context), span `llm_call` (gọi LLM), và span `tool_use` (nếu có). Trong kịch bản bình thường, RAG chiếm ~50ms và LLM chiếm ~200ms. Khi inject `rag_slow`, span `rag_retrieval` tăng lên >4500ms — dễ dàng nhìn thấy ngay trên waterfall.

**Q6: `user_id_hash` khác `user_id` như thế nào? Tại sao dùng hash?**
> `user_id_hash` là SHA-256 của `user_id` gốc, lấy 12 ký tự đầu. Dùng hash để tránh lưu PII (user ID thật) vào log system trong khi vẫn giữ khả năng group/filter logs theo user. Nếu cần tra cứu user cụ thể, engineer có thể hash lại ID gốc để so sánh.

**Q7: Decorator `@observe` làm gì?**
> `@observe` là decorator của Langfuse SDK, tự động tạo một span mới cho mỗi lần hàm được gọi, ghi lại input/output và duration. Không cần code thủ công để start/end trace — decorator xử lý hết qua context manager.

---

## Phần 3 — SLO & Alerts (Member C)

**Q8: SLO là gì? Nhóm đặt SLO nào?**
> SLO (Service Level Objective) là mục tiêu đo lường chất lượng dịch vụ:
> - Latency P95 < 3000ms (trong cửa sổ 28 ngày)
> - Error Rate < 2% (28 ngày)
> - Cost Budget < $2.5/ngày (1 ngày)
> - Quality (heuristic score) ≥ 0.75 (28 ngày)
> 
> Sau load test: P95 ~150ms, error rate 0%, cost ~$0.23/ngày, quality ~0.88 — tất cả đều trong ngưỡng SLO.

**Q9: Alert `high_latency_p95` kích hoạt khi nào?**
> Alert này trigger khi P95 latency vượt ngưỡng 5000ms trong cửa sổ đánh giá 30 phút. Runbook link trỏ đến `docs/alerts.md#1-high-latency-p95` để engineer biết cần làm gì: check RAG span, kiểm tra incident toggles, xem xét timeout/fallback.

**Q10: Sự khác biệt giữa SLI, SLO, và SLA?**
> - **SLI** (Service Level Indicator): Số đo thực tế (ví dụ: P95 latency = 150ms).
> - **SLO** (Service Level Objective): Mục tiêu nội bộ (P95 < 3000ms).
> - **SLA** (Service Level Agreement): Cam kết pháp lý với khách hàng, thường lỏng hơn SLO (ví dụ: P95 < 5000ms, không đạt → hoàn tiền).

---

## Phần 4 — Load Test & Incident (Member D)

**Q11: Làm sao phát hiện incident `rag_slow` qua observability?**
> Flow phát hiện: Dashboard cho thấy P95 latency tăng vọt (>26,000ms) → alert `high_latency_p95` kích hoạt → mở Langfuse, lọc traces có duration cao → xem waterfall, thấy span `rag_retrieval` chiếm >90% thời gian → kiểm tra incident toggles trong `/incidents` endpoint → xác nhận `rag_slow` đang bật.

**Q12: Dashboard 6 panels là gì? Tại sao cần 6 panels đó?**
> 1. **Latency P50/P95/P99** — phân biệt median vs tail latency, phát hiện outlier
> 2. **Traffic (QPS)** — biết hệ thống đang chịu tải bao nhiêu
> 3. **Error rate** — theo dõi % requests lỗi, breakdown theo loại lỗi
> 4. **Cost over time** — kiểm soát chi phí LLM API không vượt budget
> 5. **Tokens in/out** — hiểu usage pattern, phát hiện prompt quá dài
> 6. **Quality proxy** — heuristic score để proxy cho answer quality mà không cần human eval

---

## Phần 5 — Demo & Report (Member E)

**Q13: `validate_logs.py` kiểm tra những gì và nhóm đạt bao nhiêu?**
> Script kiểm tra 4 tiêu chí: (1) JSON schema hợp lệ (có `ts`, `level`, `event`), (2) Correlation ID propagation (≥2 unique IDs), (3) Log enrichment (có `user_id_hash`, `session_id`, `feature`, `model`), (4) PII scrubbing (không có `@` hoặc test credit card). Nhóm đạt **100/100** — tất cả 4 mục đều PASSED.

**Q14: Nếu `validate_logs.py` chỉ đạt 70/100, nhóm cần sửa gì đầu tiên?**
> Kiểm tra output để xem mục nào FAILED:
> - FAILED Basic JSON schema → kiểm tra `logging_config.py`, đảm bảo format JSON
> - FAILED Correlation ID → kiểm tra `middleware.py`, đảm bảo `bind_contextvars` chạy
> - FAILED Log enrichment → kiểm tra `main.py`, đảm bảo `bind_contextvars` với user context
> - FAILED PII scrubbing → kiểm tra `pii.py`, đảm bảo `scrub_event` trong processors list

**Q15: Tại sao cần cả Logs VÀ Traces? Chỉ một trong hai không đủ sao?**
> Logs và Traces bổ trợ nhau:
> - **Logs** cho biết *gì đã xảy ra* với đầy đủ context (user, session, PII-safe data) — tốt để audit và search text.
> - **Traces** cho biết *mất bao lâu ở đâu* qua distributed system — tốt để profile performance và root cause analysis.
> Logs không có timing breakdown; Traces không có application-level data. Dùng cả hai mới cho observability hoàn chỉnh theo "3 pillars": Metrics, Logs, Traces.

---

## Câu hỏi bonus (nếu giảng viên hỏi sâu hơn)

**Q16: Structured logging vs unstructured logging — ưu nhược điểm?**
> **Structured** (JSON): machine-readable, dễ query/filter/aggregate (dùng jq, Loki, ELK). Nhược: verbose hơn, khó đọc bằng mắt thường.
> **Unstructured** (plain text): dễ đọc, nhưng phải parse bằng regex để aggregate — brittle và chậm ở scale lớn.
> Lab dùng structlog với JSON renderer vì logs sẽ được ingest vào log aggregator.

**Q17: Sampling traces có nên dùng không?**
> Với production traffic lớn, nên sample (ví dụ: 10% traces) để giảm cost và storage. Tuy nhiên trong lab này (< 200 requests), sample rate = 100% là phù hợp để có đủ dữ liệu phân tích. Langfuse hỗ trợ cấu hình sample rate trong SDK initialization.
