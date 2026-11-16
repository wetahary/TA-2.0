# Company Game Master — Hybrid HE Pilot 1.0
Prototype interaktif Streamlit dengan data sintetis.

## Run locally
Python 3.10+
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
## Isi prototype
Command Center, My Mission, Mission Board, Team Arena, Live Operations, Performance & Rank, Challenge Lab, Mission Detail, Bug & Feedback.

## Privasi dan batasan
Semua JO, customer, nilai, task, tanggal, dan skor adalah sintetis. Tidak ada koneksi Odoo, API AI, atau layanan eksternal. Role selector hanya simulasi UI, bukan autentikasi. Data session tidak menjadi database bersama/permanen. Jangan masukkan data aktual/confidential dan jangan deploy publik sebelum review keamanan dan persetujuan IT.

## Sebelum produksi
Tambahkan autentikasi/MFA, RBAC, PostgreSQL, audit log, verifier separation, persistent event store, backup, SLA calendar, dependency engine, Odoo connector, monitoring, dan security review.
