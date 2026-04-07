# SkenPay KYC System

Full-stack KYC signup system with Django backend + admin panel.

## Project Structure

```
skenpay-kyc/
├── backend/          ← Django REST API + Admin (deploy to Railway)
│   ├── kyc/          ← KYC app (models, views, admin, serializers)
│   ├── skenpay/      ← Django project settings & URLs
│   ├── requirements.txt
│   ├── railway.toml
│   └── start.sh      ← Auto-migrates, collects static, starts gunicorn
└── frontend/
    └── signup.html   ← Drop into your SkenPay website
```

---

## Railway Deployment (Backend)

### Step 1 — Create a GitHub Repo
```bash
cd backend/
git init
git add .
git commit -m "SkenPay KYC backend"
git remote add origin https://github.com/YOUR_USERNAME/skenpay-kyc-backend.git
git push -u origin main
```

### Step 2 — Deploy on Railway
1. Go to [railway.app](https://railway.app) → **New Project**
2. Click **Deploy from GitHub repo** → select `skenpay-kyc-backend`
3. Railway auto-detects Python via `requirements.txt`

### Step 3 — Add PostgreSQL
1. In your Railway project → **New** → **Database** → **PostgreSQL**
2. Railway auto-injects `DATABASE_URL` into your service

### Step 4 — Set Environment Variables
In your Railway service → **Variables**, add:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | (generate a random 50-char string) |
| `DEBUG` | `False` |
| `DJANGO_SUPERUSER_EMAIL` | `admin@skenpay.io` |
| `DJANGO_SUPERUSER_PASSWORD` | (strong password) |

### Step 5 — Get your URL
Railway gives you a URL like `https://skenpay-kyc-backend.railway.app`

---

## Admin Panel

Access at: `https://YOUR-BACKEND.railway.app/admin/`

Login with the superuser credentials you set in env vars.

### Admin Features
- 📋 View all KYC applications with status badges
- 🔍 Filter by status, nationality, ID type, employment, PEP flag
- 🔎 Search by name, email, reference number, ID number
- ✅ Bulk approve / reject / mark under review
- 📎 Preview uploaded ID photos and selfies inline
- 📥 Export to CSV
- 🚩 PEP flag highlighted in red

---

## Frontend Integration

1. Open `frontend/signup.html`
2. Find this line near the top of the `<script>` section:
   ```js
   : 'https://YOUR-BACKEND.railway.app';
   ```
3. Replace `YOUR-BACKEND.railway.app` with your actual Railway backend URL
4. Host `signup.html` anywhere — add it to your SkenPay website, or deploy as a second Railway static service

---

## API Endpoints

### Submit KYC Application
```
POST /api/kyc/submit/
Content-Type: multipart/form-data

Fields: first_name, last_name, date_of_birth, nationality, country_of_residence,
        email, phone_country_code, phone_number,
        address_line1, address_line2, city, state, postal_code, country,
        id_type, id_number, id_expiry_date, id_issuing_country,
        id_front_image (file), id_back_image (file), selfie_image (file), proof_of_address (file),
        employment_status, employer_name, annual_income, purpose_of_account,
        expected_monthly_transactions, source_of_funds,
        is_pep, pep_details, has_criminal_record, criminal_record_details,
        consent_terms, consent_privacy, consent_data_processing, consent_marketing
```

Response:
```json
{
  "success": true,
  "reference": "SKN-XXXXXXXX",
  "status": "pending"
}
```

### Check Application Status
```
GET /api/kyc/status/?ref=SKN-XXXXXXXX
GET /api/kyc/status/?email=user@example.com
```

### Health Check
```
GET /health/
```

---

## KYC Fields Collected

| Category | Fields |
|----------|--------|
| Personal | Full name, DOB, nationality, residence country, email, phone |
| Address | Street, city, state, postal code, country |
| Identity | Document type, number, expiry, issuing country |
| Documents | ID front, ID back, selfie with ID, proof of address (files) |
| Financial | Employment, employer, income, purpose, monthly volume, source of funds |
| Compliance | PEP declaration, criminal record declaration |
| Consents | Terms, privacy, data processing, marketing (opt-in) |

---

## Local Development

```bash
cd backend/
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open `frontend/signup.html` in your browser.
The API_BASE in signup.html defaults to `http://localhost:8000` when running locally.
