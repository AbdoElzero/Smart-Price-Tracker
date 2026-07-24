"""
سكريبت لتعبئة البيانات الأساسية (Seed Data) — بيانات حقيقية فقط:
- عملات الدول العربية الأساسية
- الدول العربية
- التصنيفات الرئيسية والفرعية
- العلامات التجارية المعروفة
- المتاجر المعروفة بأسمائها ومواقعها الحقيقية (بدون أي بيانات وهمية)

⚠️ ملاحظة: حقل is_scraping_enabled = False لكل متجر افتراضيًا.
لا يتم تفعيله إلا بعد مراجعة شروط الاستخدام (ToS) لكل متجر على حدة،
أو الحصول على API رسمي من المتجر.

التشغيل (بعد تفعيل venv وتشغيل migrations):
    python seed.py
"""
from app import create_app
from app.extensions import db
from app.models import Currency, Country, Category, Brand, Store


def seed_currencies():
    data = [
        {"code": "SAR", "name_ar": "ريال سعودي", "name_en": "Saudi Riyal", "symbol": "ر.س", "exchange_rate_to_usd": 3.75},
        {"code": "EGP", "name_ar": "جنيه مصري", "name_en": "Egyptian Pound", "symbol": "ج.م", "exchange_rate_to_usd": 49.0},
        {"code": "AED", "name_ar": "درهم إماراتي", "name_en": "UAE Dirham", "symbol": "د.إ", "exchange_rate_to_usd": 3.67},
        {"code": "KWD", "name_ar": "دينار كويتي", "name_en": "Kuwaiti Dinar", "symbol": "د.ك", "exchange_rate_to_usd": 0.31},
        {"code": "QAR", "name_ar": "ريال قطري", "name_en": "Qatari Riyal", "symbol": "ر.ق", "exchange_rate_to_usd": 3.64},
        {"code": "BHD", "name_ar": "دينار بحريني", "name_en": "Bahraini Dinar", "symbol": "د.ب", "exchange_rate_to_usd": 0.38},
        {"code": "OMR", "name_ar": "ريال عماني", "name_en": "Omani Rial", "symbol": "ر.ع", "exchange_rate_to_usd": 0.38},
        {"code": "JOD", "name_ar": "دينار أردني", "name_en": "Jordanian Dinar", "symbol": "د.أ", "exchange_rate_to_usd": 0.71},
        {"code": "IQD", "name_ar": "دينار عراقي", "name_en": "Iraqi Dinar", "symbol": "د.ع", "exchange_rate_to_usd": 1310.0},
        {"code": "MAD", "name_ar": "درهم مغربي", "name_en": "Moroccan Dirham", "symbol": "د.م", "exchange_rate_to_usd": 9.9},
        {"code": "USD", "name_ar": "دولار أمريكي", "name_en": "US Dollar", "symbol": "$", "exchange_rate_to_usd": 1.0},
    ]
    created = {}
    for item in data:
        currency = Currency.query.filter_by(code=item["code"]).first()
        if not currency:
            currency = Currency(**item)
            db.session.add(currency)
            db.session.flush()
        created[item["code"]] = currency
    db.session.commit()
    return created


def seed_countries(currencies):
    data = [
        {"code": "SA", "name_ar": "السعودية", "name_en": "Saudi Arabia", "flag_emoji": "🇸🇦", "currency": "SAR"},
        {"code": "EG", "name_ar": "مصر", "name_en": "Egypt", "flag_emoji": "🇪🇬", "currency": "EGP"},
        {"code": "AE", "name_ar": "الإمارات", "name_en": "United Arab Emirates", "flag_emoji": "🇦🇪", "currency": "AED"},
        {"code": "KW", "name_ar": "الكويت", "name_en": "Kuwait", "flag_emoji": "🇰🇼", "currency": "KWD"},
        {"code": "QA", "name_ar": "قطر", "name_en": "Qatar", "flag_emoji": "🇶🇦", "currency": "QAR"},
        {"code": "BH", "name_ar": "البحرين", "name_en": "Bahrain", "flag_emoji": "🇧🇭", "currency": "BHD"},
        {"code": "OM", "name_ar": "عُمان", "name_en": "Oman", "flag_emoji": "🇴🇲", "currency": "OMR"},
        {"code": "JO", "name_ar": "الأردن", "name_en": "Jordan", "flag_emoji": "🇯🇴", "currency": "JOD"},
        {"code": "IQ", "name_ar": "العراق", "name_en": "Iraq", "flag_emoji": "🇮🇶", "currency": "IQD"},
        {"code": "MA", "name_ar": "المغرب", "name_en": "Morocco", "flag_emoji": "🇲🇦", "currency": "MAD"},
    ]
    for item in data:
        country = Country.query.filter_by(code=item["code"]).first()
        if not country:
            country = Country(
                code=item["code"],
                name_ar=item["name_ar"],
                name_en=item["name_en"],
                flag_emoji=item["flag_emoji"],
                currency_id=currencies[item["currency"]].id,
            )
            db.session.add(country)
    db.session.commit()


def seed_categories():
    main_categories = [
        {"slug": "computers", "name_ar": "أجهزة الكمبيوتر", "name_en": "Computers", "icon": "computer"},
        {"slug": "phones", "name_ar": "الهواتف", "name_en": "Phones", "icon": "smartphone"},
        {"slug": "monitors", "name_ar": "الشاشات", "name_en": "Monitors", "icon": "monitor"},
        {"slug": "pc-parts", "name_ar": "قطع الكمبيوتر", "name_en": "PC Parts", "icon": "cpu"},
    ]
    parents = {}
    for item in main_categories:
        cat = Category.query.filter_by(slug=item["slug"]).first()
        if not cat:
            cat = Category(**item)
            db.session.add(cat)
            db.session.flush()
        parents[item["slug"]] = cat
    db.session.commit()

    sub_categories = [
        {"slug": "laptops", "name_ar": "لابتوب", "name_en": "Laptops", "parent": "computers"},
        {"slug": "desktops", "name_ar": "ديسكتوب", "name_en": "Desktops", "parent": "computers"},
        {"slug": "mini-pc", "name_ar": "ميني بي سي", "name_en": "Mini PC", "parent": "computers"},
        {"slug": "gaming-pc", "name_ar": "كمبيوتر قيمنق", "name_en": "Gaming PC", "parent": "computers"},
        {"slug": "workstations", "name_ar": "ووركستيشن", "name_en": "Workstations", "parent": "computers"},
        {"slug": "cpu", "name_ar": "المعالجات", "name_en": "CPUs", "parent": "pc-parts"},
        {"slug": "gpu", "name_ar": "كروت الشاشة", "name_en": "GPUs", "parent": "pc-parts"},
        {"slug": "ram", "name_ar": "الرامات", "name_en": "RAM", "parent": "pc-parts"},
        {"slug": "motherboards", "name_ar": "اللوحات الأم", "name_en": "Motherboards", "parent": "pc-parts"},
        {"slug": "storage", "name_ar": "وحدات التخزين", "name_en": "Storage (SSD/HDD/NVMe)", "parent": "pc-parts"},
        {"slug": "psu", "name_ar": "مزودات الطاقة", "name_en": "Power Supplies", "parent": "pc-parts"},
        {"slug": "cases", "name_ar": "الكيسات", "name_en": "Cases", "parent": "pc-parts"},
        {"slug": "cooling", "name_ar": "أنظمة التبريد", "name_en": "Cooling", "parent": "pc-parts"},
    ]
    for item in sub_categories:
        cat = Category.query.filter_by(slug=item["slug"]).first()
        if not cat:
            cat = Category(
                slug=item["slug"],
                name_ar=item["name_ar"],
                name_en=item["name_en"],
                parent_id=parents[item["parent"]].id,
            )
            db.session.add(cat)
    db.session.commit()


def seed_brands():
    brands = [
        "Apple", "Samsung", "Xiaomi", "Realme", "Oppo", "Huawei", "Honor", "Vivo",
        "Google", "OnePlus", "Nothing", "Motorola", "Infinix", "Tecno", "Nokia", "Sony", "Asus",
        "Intel", "AMD", "NVIDIA", "MSI", "Gigabyte", "Dell", "HP", "Lenovo", "LG", "BenQ", "AOC",
        "Acer", "ViewSonic", "Corsair", "Kingston", "Western Digital", "Seagate", "Crucial",
    ]
    for name in brands:
        slug = name.lower().replace(" ", "-")
        brand = Brand.query.filter_by(slug=slug).first()
        if not brand:
            brand = Brand(name_ar=name, name_en=name, slug=slug)
            db.session.add(brand)
    db.session.commit()


def seed_stores(countries_by_code):
    stores = [
        {"slug": "amazon-sa", "name": "Amazon السعودية", "url": "https://www.amazon.sa", "country": "SA"},
        {"slug": "noon-sa", "name": "Noon السعودية", "url": "https://www.noon.com/saudi-en", "country": "SA"},
        {"slug": "jarir", "name": "جرير", "url": "https://www.jarir.com", "country": "SA"},
        {"slug": "extra", "name": "إكسترا", "url": "https://www.extra.com", "country": "SA"},
        {"slug": "amazon-eg", "name": "Amazon مصر", "url": "https://www.amazon.eg", "country": "EG"},
        {"slug": "noon-eg", "name": "Noon مصر", "url": "https://www.noon.com/egypt-en", "country": "EG"},
        {"slug": "2b", "name": "2B", "url": "https://2b.com.eg", "country": "EG"},
        {"slug": "btech", "name": "B.TECH", "url": "https://btech.com", "country": "EG"},
    ]
    for item in stores:
        store = Store.query.filter_by(slug=item["slug"]).first()
        if not store:
            store = Store(
                name_ar=item["name"],
                name_en=item["name"],
                slug=item["slug"],
                website_url=item["url"],
                country_id=countries_by_code[item["country"]].id,
                is_scraping_enabled=False,
            )
            db.session.add(store)
    db.session.commit()


def run():
    app = create_app()
    with app.app_context():
        print("🌱 بدء تعبئة البيانات الأساسية...")

        currencies = seed_currencies()
        print("✅ العملات تمت إضافتها")

        seed_countries(currencies)
        print("✅ الدول تمت إضافتها")

        seed_categories()
        print("✅ التصنيفات تمت إضافتها")

        seed_brands()
        print("✅ العلامات التجارية تمت إضافتها")

        countries_by_code = {c.code: c for c in Country.query.all()}
        seed_stores(countries_by_code)
        print("✅ المتاجر تمت إضافتها")

        print("🎉 تمت تعبئة البيانات الأساسية بنجاح!")


if __name__ == "__main__":
    run()
