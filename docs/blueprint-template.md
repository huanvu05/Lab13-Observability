# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]&#58; Observability Team 01
- [REPO_URL]&#58; https://github.com/your-repo/observability-lab
- [MEMBERS]&#58;   - Member A: [Tên của bạn] | Role: Logging & PII
  - Member B: [Tên teammate] | Role: Tracing & Enrichment

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]&#58; 100/100
- [TOTAL_TRACES_COUNT]&#58; N/A
- [PII_LEAKS_FOUND]&#58; 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]&#58; screenshots/correlation_id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]&#58; screenshots/pii_redaction.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]&#58; N/A
- [TRACE_WATERFALL_EXPLANATION]&#58; N/A (Phần tracing do Member B phụ trách)

---

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]&#58; N/A
- [SLO_TABLE]&#58; | SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | N/A |
| Error Rate | < 2% | 28d | N/A |
| Cost Budget | < $2.5/day | 1d | N/A |

---

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]&#58; N/A
- [SAMPLE_RUNBOOK_LINK]&#58; N/A

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]&#58; N/A
- [SYMPTOMS_OBSERVED]&#58; N/A
- [ROOT_CAUSE_PROVED_BY]&#58; N/A
- [FIX_ACTION]&#58; N/A
- [PREVENTIVE_MEASURE]&#58; N/A

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]&#58;  
Đã triển khai hệ thống logging dạng JSON chuẩn production, bao gồm correlation_id để theo dõi request, enrich context (user_id_hash, session_id, feature, model, env) vào log.  
Thực hiện PII scrubbing để ẩn các thông tin nhạy cảm như email, số điện thoại, thẻ tín dụng.  
Đảm bảo toàn bộ log pass validate_logs.py với score 100/100, không thiếu field và không rò rỉ dữ liệu nhạy cảm.
- [EVIDENCE_LINK]&#58; https://github.com/your-repo/commit/logging-feature

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]&#58;  
Phụ trách phần tracing và observability (không thuộc phạm vi của Member A).
- [EVIDENCE_LINK]&#58; https://github.com/your-repo/commit/tracing-setup

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]&#58; N/A
- [BONUS_AUDIT_LOGS]&#58;  
Log được thiết kế theo dạng structured logging, có thể dùng cho audit và truy vết request thông qua correlation_id.
- [BONUS_CUSTOM_METRIC]&#58; N/A