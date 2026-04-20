# Alert Rules and Runbooks

Runbook được tham chiếu từ `config/alert_rules.yaml` (Member C).

## Mapping SLI → ứng dụng lab

| SLI trong SLO / alert | Nguồn đo trong lab |
|----------------------|-------------------|
| `latency_p95_ms` | `GET /metrics` → `latency_p95` (ms) |
| `error_rate_pct` | Từ `traffic` và `error_breakdown` (tự tính %) |
| `hourly_cost_usd` / baseline | Từ `total_cost_usd` hoặc dashboard cost (Grafana) khi tích hợp thật |
| `quality_score_avg` | `GET /metrics` → `quality_avg` |

---

## 1. High latency P95

- Severity: P2
- Trigger: `latency_p95_ms > 5000 for 30m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs LLM span
  3. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - truncate long queries
  - fallback retrieval source
  - lower prompt size

## 2. High error rate

- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are LLM, tool, or schema related
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model

## 3. Cost budget spike

- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache

## 4. Low average quality score

- Severity: P3
- Trigger: `quality_score_avg < 0.75 for 1h`
- Impact: câu trả lời kém (heuristic), rủi ro trải nghiệm người dùng
- First checks:
  1. Xem `GET /metrics` → `quality_avg` và phân bố request theo `feature` trong log
  2. Mở vài trace Langfuse: input có quá ngắn / RAG trả về rỗng?
  3. Kiểm tra incident ảnh hưởng chất lượng (nếu có)
- Mitigation:
  - điều chỉnh prompt hoặc ngưỡng RAG
  - bật fallback model cho feature đang thấp điểm
  - rà soát scrub PII có làm mất ngữ cảnh cần thiết không
