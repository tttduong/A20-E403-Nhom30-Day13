# Báo cáo Cá nhân — Day 13 Observability Lab

| Thông tin | Chi tiết |
|---|---|
| **Họ và tên** | Hồ Quang Hiển |
| **Mã sinh viên** | 059 |
| **Vai trò trong nhóm** | Member C — SLO & Alerts |
| **Nhóm** | Nhóm 30 — A20-E403 |
| **Repo** | https://github.com/tttduong/A20-E403-Nhom30-Day13 |
| **Branch cá nhân** | `main` |
| **Commit chính** | `80f1a71` — `"member hqh"` |

---

## 1. Nhiệm vụ được phân công

Theo kế hoạch nhóm, mình phụ trách **SLO & Alerts**: xác định chỉ số theo dõi dịch vụ, cấu hình rule cảnh báo, viết runbook xử lý sự cố và chuẩn hóa phần bằng chứng liên quan để nhóm demo.

### Checklist nhiệm vụ

| # | Nhiệm vụ | Trạng thái |
|---|---|:---:|
| 1 | Hoàn thiện `config/slo.yaml` (SLI, target, window, mapping dữ liệu từ `/metrics`) | ✅ Hoàn thành |
| 2 | Hoàn thiện `config/alert_rules.yaml` với 4 rule có ngưỡng rõ ràng và runbook link | ✅ Hoàn thành |
| 3 | Cập nhật `docs/alerts.md` (runbook, mapping SLI, bổ sung mục quality) | ✅ Hoàn thành |
| 4 | Điền phần SLO/Alert trong `docs/blueprint-template.md` (§3.2, §3.3 và draft mục incident) | ✅ Hoàn thành |
| 5 | Chuẩn hóa bằng chứng chấm điểm tại `docs/grading-evidence.md` + `docs/evidence/validate_logs_output.txt` | ✅ Hoàn thành |

---

## 2. Các file đã tạo / chỉnh sửa

### 2.1 `config/slo.yaml` — Định nghĩa SLO cho lab

Mục tiêu là chuyển các số đo từ `/metrics` thành mục tiêu vận hành có thể theo dõi được trong demo.

- Định nghĩa các SLI chính: **Latency P95**, **Error Rate**, **Cost Budget**, **Quality Avg**.
- Mỗi SLI đều có target và window rõ ràng để dễ so sánh trước/sau incident.
- Ghi chú rõ nguồn dữ liệu lấy từ endpoint `/metrics` để các thành viên D/E có thể dùng thống nhất khi làm dashboard và báo cáo.

### 2.2 `config/alert_rules.yaml` — Rule cảnh báo

Thiết kế 4 cảnh báo trọng tâm bám theo SLO:

1. `high_latency_p95` — phát hiện độ trễ tăng đột biến.
2. `high_error_rate` — phát hiện request lỗi vượt ngưỡng.
3. `cost_budget_exceeded` — phát hiện vượt ngân sách chi phí.
4. `quality_drop` — phát hiện chất lượng trả lời giảm.

Mỗi rule đều có:
- **condition** rõ ràng;
- **severity** để ưu tiên xử lý;
- **runbook_link** trỏ về đúng mục trong `docs/alerts.md`.

### 2.3 `docs/alerts.md` — Runbook xử lý

Mình chuẩn hóa runbook theo flow thao tác thực tế:

- Triệu chứng (dấu hiệu nhận biết trên metrics/traces/logs);
- Bước xác minh nhanh;
- Root cause thường gặp;
- Hành động khắc phục trước mắt;
- Kiểm tra hậu kiểm sau khi fix.

Điểm nhấn là thêm phần liên kết giữa cảnh báo và hành động cụ thể, giúp nhóm demo logic “phát hiện -> khoanh vùng -> xử lý -> xác nhận phục hồi”.

### 2.4 `docs/blueprint-template.md` và `docs/grading-evidence.md`

- Điền phần kỹ thuật thuộc vai trò C: bảng SLO, bằng chứng alert rules, link runbook, draft incident.
- Cập nhật evidence để giảng viên đối chiếu được ngay file, ảnh và commit.
- Bổ sung tài liệu hướng dẫn thao tác/thu thập bằng chứng để đội hình demo nhất quán.

---

## 3. Kết quả kiểm chứng

Kết quả từ file `docs/evidence/validate_logs_output.txt`:

```text
Estimated Score: 100/100
```

Các tiêu chí nền tảng đều đạt:
- Basic JSON schema: PASSED
- Correlation ID propagation: PASSED
- Log enrichment: PASSED
- PII scrubbing: PASSED

Kết quả này giúp phần SLO/Alert có dữ liệu tin cậy để theo dõi và cảnh báo.

---

## 4. Hiểu sâu về phần việc đảm nhận

### 4.1 Vì sao Member C cần tách SLO và Alert thành 2 lớp?

- **SLO** trả lời câu hỏi: “mục tiêu dịch vụ là gì?”
- **Alert** trả lời câu hỏi: “khi nào cần phản ứng ngay?”

Nếu chỉ có SLO mà thiếu alert, nhóm biết mục tiêu nhưng không phát hiện vi phạm kịp lúc. Nếu chỉ có alert mà thiếu SLO, cảnh báo dễ bị đặt ngưỡng cảm tính, khó đánh giá đúng/sai.

### 4.2 Quan hệ giữa Metrics, Traces, Logs trong runbook

Khi có sự cố `rag_slow`, quy trình chuẩn là:
1. Xem **metrics** để phát hiện P95 tăng.
2. Xem **trace** (Langfuse waterfall) để biết span nào chậm.
3. Xem **logs** có `correlation_id` để đối chiếu request cụ thể.
4. Thực hiện hành động khôi phục (`disable incident`) và kiểm tra lại metrics.

Runbook mình viết bám đúng chuỗi này để khi demo hoặc vận hành thật đều dễ theo.

### 4.3 Giá trị của rule `quality_drop`

Latency tốt chưa đủ; hệ thống có thể nhanh nhưng trả lời kém. Bổ sung `quality_drop` giúp theo dõi cả mặt chất lượng đầu ra, tránh “đạt hiệu năng nhưng hụt trải nghiệm”.

---

## 5. Bằng chứng Git

| File | Loại thay đổi | Commit |
|---|---|---|
| `config/slo.yaml` | Modified | `80f1a71` |
| `config/alert_rules.yaml` | Modified | `80f1a71` |
| `docs/alerts.md` | Modified | `80f1a71` |
| `docs/blueprint-template.md` | Modified | `80f1a71` |
| `docs/grading-evidence.md` | Modified | `80f1a71` |
| `docs/evidence/validate_logs_output.txt` | Added/Updated | `80f1a71` |

**Link commit:** https://github.com/tttduong/A20-E403-Nhom30-Day13/commit/80f1a71a058b551aebc43cb8ee17cbb7186ccb27

---

## 6. Tự đánh giá

| Hạng mục rubric | Tự chấm | Lý do |
|---|:---:|---|
| **B1 — Individual Report** | 20/20 | Nội dung đầy đủ, đúng vai trò Member C, có checklist, giải thích kỹ thuật và runbook rõ ràng |
| **B2 — Git Evidence** | 20/20 | Có commit rõ ràng, file bằng chứng đầy đủ, đối chiếu được trực tiếp với phần việc đã triển khai |
| **Tổng cá nhân** | **40/40** | |

> Ghi chú: Phần việc của Member C đạt mục tiêu “đo được, cảnh báo được, xử lý được” và kết nối tốt với phần demo nhóm.
