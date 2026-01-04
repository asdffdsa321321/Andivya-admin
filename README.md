# Andivya Admin Dashboard

Internal admin dashboard for Andivya (kurti manufacturing brand).

This is **not public-facing**.
Built for daily internal operations.

---

## Features (MVP)

### ✅ Product Uploader
- Image upload (Cloudinary)
- Variant-safe slug logic: `title + color + group_key`
- Single color per product (stored uppercase)
- Safe DB upsert
- No accidental overwrites

### ✅ Orders Dashboard
- View latest orders
- Update order status
- No delete actions

### ✅ Invoice Generator
- Generate HTML invoices
- Print-ready
- Downloadable

---

## Tech Stack

- **Frontend:** Streamlit
- **Database:** PostgreSQL (Neon)
- **ORM:** SQLAlchemy Core
- **Image Storage:** Cloudinary
- **Templates:** Jinja2

---

## Setup (Local)

### 1. Create virtualenv (recommended)

```bash
python -m venv venv
source venv/bin/activate


### DEVELOPER
Ayush Saini
https://linkedin.com/in/the-ayush-factor    