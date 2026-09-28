# Lab 11: Guardrails, HITL & Responsible AI

**Họ và tên:** Nguyễn Quang Huy
**MSSV:** 2A202602461

## Cách chạy
1. Tạo môi trường ảo và cài đặt thư viện:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Tạo file `.env` từ `.env.example` và điền API key.
3. Chạy lệnh sinh kết quả:
   ```bash
   python src/main.py --part 3
   python src/main.py --part 4
   ```
4. Kiểm tra chấm điểm:
   ```bash
   pytest tests/public -q
   python scripts/grade.py --submission-dir . --out outputs/grade_report.json
   ```
