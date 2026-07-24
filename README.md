# Smart Price Tracker 🛒📉

موقع عربي لتتبع وتحليل أسعار المنتجات التقنية (كمبيوترات، هواتف، شاشات) في الدول العربية،
مع نظام تحليل أسعار يساعد المستخدم على اتخاذ قرار الشراء.

## التقنيات المستخدمة

### Backend
- Python 3.11 / Flask
- SQLAlchemy + PostgreSQL
- Redis + Celery
- JWT Authentication
- Swagger (OpenAPI)

### Frontend
- Vue.js 3 + Vite
- Pinia
- Vue Router
- Tailwind CSS (RTL/LTR + Dark Mode)

## التشغيل محليًا

```bash
# 1. نسخ ملفات البيئة
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. تشغيل كل الخدمات
docker-compose up --build

# الواجهة: http://localhost:8080
# الـ API: http://localhost:5000/api/v1
# Swagger: http://localhost:5000/api/v1/docs
```

## بنية المشروع

راجع `backend/` و `frontend/` لمزيد من التفاصيل في كل جزء من التنفيذ.

## الحالة

🚧 المشروع قيد البناء التدريجي (جزء بجزء).

- [x] الجزء 1: هيكل المشروع الكامل
- [x] الجزء 2: Database Models
- [x] الجزء 3: Authentication Backend
- [ ] الجزء 4: صفحات Login/Register Frontend
- [ ] ... (المزيد قادم)
