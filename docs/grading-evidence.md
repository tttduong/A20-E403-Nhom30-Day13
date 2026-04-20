# Evidence Collection Sheet

## Required screenshots
- Langfuse trace list with >= 10 traces
- One full trace waterfall
- JSON logs showing correlation_id
- Log line with PII redaction
- Dashboard with 6 panels
- Alert rules with runbook link

## Optional screenshots
- Incident before/after fix
- Cost comparison before/after optimization
- Auto-instrumentation proof

## Member C — SLO & Alerts (Hồ Quang Hiển)

| Việc đã làm (file) | Trạng thái |
|--------------------|------------|
| `config/slo.yaml` | Đã chỉnh (SLI + ghi chú map metrics) |
| `config/alert_rules.yaml` | 4 rule + runbook link |
| `docs/alerts.md` | Runbook + mapping SLI + mục 4 quality |
| `docs/blueprint-template.md` | Điền mục 1 (nhóm/repo/C), 2 (validate/PII), 3.2–3.3 (SLO + link runbook), 4 (draft incident), 5 (Member C) |
| `docs/huong-dan-bao-cao-va-chung-minh.md` | Hướng dẫn lệnh + chụp ảnh |
| `docs/evidence/validate_logs_output.txt` | Output validate 100/100 (nếu có) |

**Còn thiếu cho bằng chứng đầy đủ:** ảnh `docs/evidence/alert-rules-screenshot.png`; link **commit** sau `git push`; xác nhận `[TOTAL_TRACES_COUNT]` trên Langfuse; A/B/D/E tự điền tên + mục 5 tương ứng.
