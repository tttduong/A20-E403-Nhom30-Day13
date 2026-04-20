# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Nhóm 30 — A20-E403
- [REPO_URL]: https://github.com/tttduong/A20-E403-Nhom30-Day13
- [MEMBERS]:
  - Member A: Tạ Thị Thuỳ Dương | Role: Logging & PII
  - Member B: Nguyễn Thị Thu Hiền | Role: Tracing & Enrichment
  - Member C: Hồ Quang Hiển | Role: SLO & Alerts
  - Member D: Trịnh Đức An | Role: Load Test & Dashboard
  - Member E: Lương Thanh Hậu | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: ≥ 20 (xác nhận qua Langfuse UI sau khi chạy load_test.py --concurrency 5)
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/evidence/correlation-id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/evidence/pii-redaction.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/evidence/trace-waterfall.png (chụp từ Langfuse UI — span "rag_retrieval" chiếm >90% tổng duration khi inject rag_slow)
- [TRACE_WATERFALL_EXPLANATION]: Span thú vị nhất là "rag_retrieval" — khi inject sự cố rag_slow, span này kéo dài từ ~50ms lên >4500ms, chiếm >90% tổng thời gian request. Điều này trực tiếp gây vi phạm SLO latency P95 (<3000ms) và kích hoạt alert high_latency_p95. Root cause là mock delay nhân tạo trong mock_rag.py, fix bằng cách tắt toggle qua POST /incidents/rag_slow/disable.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: `docs/evidence/dashboard_latency.png` (và các file `dashboard_*.png` khác)
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 150 ms (`latency_p95`; nội bộ agent, khác RTT client) |
| Error Rate | < 2% | 28d | 0% (110 request, `error_breakdown` rỗng) |
| Cost Budget | < $2.5/day | 1d | $0.2334 (`total_cost_usd`; `avg_cost_usd` ≈ 0.0021/request) |
| Quality (avg heuristic) | ≥ 0.75 | 28d | 0.88 (`quality_avg`) |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: `docs/evidence/alert-rules-screenshot.png`
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Latency P95 tăng vọt từ ~800ms lên hơn 26,000ms. Số lượng request thành công không đổi nhưng thời gian phản hồi vi phạm SLO nặng nề.
- [ROOT_CAUSE_PROVED_BY]: Log ghi nhận latency tăng đột biến sau khi kích hoạt incident thông qua API. Trace trên Langfuse cho thấy các span retrieval bị kéo dài.
- [FIX_ACTION]: Gọi API `POST /incidents/rag_slow/disable` để khôi phục trạng thái hệ thống.
- [PREVENTIVE_MEASURE]: Cấu hình Alert `high_latency_p95` để tự động phát hiện khi P95 vượt ngưỡng 5s.

---

## 5. Individual Contributions & Evidence

### [Tạ Thị Thuỳ Dương]
- [TASKS_COMPLETED]: Implement correlation ID middleware (app/middleware.py): clear_contextvars(), extract x-request-id header, bind_contextvars(), thêm x-request-id + x-response-time-ms vào response headers. Bổ sung regex PII (app/pii.py): Passport VN, CMND/CCCD, địa chỉ VN (phường/quận/thành phố). Uncomment scrub_event processor trong logging_config.py.
- [EVIDENCE_LINK]: https://github.com/tttduong/A20-E403-Nhom30-Day13/commit/0228cf554620421bb7bcd58a21176242e0e60f98

### [Nguyễn Thị Thu Hiền]
- [TASKS_COMPLETED]: Implement log enrichment trong app/main.py: bind_contextvars với user_id_hash (SHA-256), session_id, feature, model, env cho mỗi request /query. Xác nhận decorator @observe trên agent pipeline trong app/agent.py. Verify Langfuse client khởi tạo đúng từ .env.
- [EVIDENCE_LINK]: https://github.com/tttduong/A20-E403-Nhom30-Day13/commit/a3aa355fc48ea24b26e300e77f1b6c1cfe82dcdc

### [Hồ Quang Hiển]
- [TASKS_COMPLETED]: Hoàn thiện `config/slo.yaml` (SLI + map `/metrics`); 4 rule `config/alert_rules.yaml` + runbook `docs/alerts.md` (thêm mục quality); điền blueprint mục 3.2–3.3 + draft mục 4; thêm `docs/huong-dan-bao-cao-va-chung-minh.md`; cập nhật `docs/grading-evidence.md`.
- [EVIDENCE_LINK]: https://github.com/tttduong/A20-E403-Nhom30-Day13/commit/80f1a71a058b551aebc43cb8ee17cbb7186ccb27

### [Trịnh Đức An]
- [TASKS_COMPLETED]: Triển khai Load Test baseline và stress test (≥100 requests, concurrency 5); Giả lập sự cố `rag_slow` — P95 tăng từ ~800ms lên >26,000ms; Xây dashboard tự động 6 panels từ Metrics API (scripts/generate_dashboard.py); Thêm scripts/check_langfuse.py để verify traces; Upload 6 dashboard screenshots vào docs/evidence/.
- [EVIDENCE_LINK]: https://github.com/tttduong/A20-E403-Nhom30-Day13/commit/b9bea5ef03f160087abab42694837c042c061d79

### [Lương Thanh Hậu]
- [TASKS_COMPLETED]: Điền đầy đủ tất cả tag còn trống trong docs/blueprint-template.md (screenshot paths §3.1, TOTAL_TRACES_COUNT §2, tên + task tất cả 5 thành viên §5). Cập nhật docs/grading-evidence.md với link commit/PR cụ thể của từng thành viên. Tạo docs/mock-debug-qa.md (kịch bản Q&A cho demo live). Chạy python scripts/validate_logs.py lần cuối — đạt 100/100. Soạn kịch bản demo live (thứ tự: start app → load test → xem logs → xem traces → xem dashboard → demo alert).
- [EVIDENCE_LINK]: https://github.com/tttduong/A20-E403-Nhom30-Day13/commit/HEAD (commit của Member E — blueprint hoàn chỉnh)

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
