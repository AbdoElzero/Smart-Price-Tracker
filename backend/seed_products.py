"""
سكريبت اختياري لإضافة منتجات تجريبية (Demo Catalog) لأغراض اختبار الواجهة فقط.

⚠️ ملاحظات مهمة:
- المواصفات التقنية أدناه هي حقائق عامة معروفة (Public Specs) عن هذه المنتجات،
  وليست بيانات وهمية أو مُلفَّقة.
- هذه المنتجات لا تحتوي على أي سعر (Price) عمدًا، لأن الأسعار الحقيقية يجب أن تأتي
  فقط من مصدر بيانات حقيقي (API رسمي، أو Scraper مفعَّل بعد مراجعة ToS لكل متجر).
- الصور أدناه عبارة عن صور placeholder عامة (وليست صور المنتجات الفعلية)، لتجنّب
  أي إشكاليات متعلقة بحقوق الصور قبل ربط مصدر صور رسمي لاحقًا.

التشغيل (اختياري - فقط لو تريد بيانات لتجربة الواجهة):
    python seed_products.py
"""
from datetime import date
from app import create_app
from app.extensions import db
from app.models import Product, Brand, Category, ProductImage, Specification


PRODUCTS = [
    {
        "slug": "apple-iphone-15-128gb",
        "name_ar": "آيفون 15 - 128 جيجابايت",
        "name_en": "Apple iPhone 15 128GB",
        "brand": "apple",
        "category": "phones",
        "model_number": "A3092",
        "release_date": date(2023, 9, 22),
        "description_ar": "آيفون 15 بمعالج A16 Bionic وكاميرا خلفية 48 ميجابكسل ومنفذ USB-C.",
        "image": "https://placehold.co/600x600?text=iPhone+15",
        "specs": [
            ("الشاشة", "الحجم", "6.1 بوصة Super Retina XDR"),
            ("المعالج", "المعالج", "Apple A16 Bionic"),
            ("الكاميرا", "الكاميرا الخلفية", "48 ميجابكسل + 12 ميجابكسل"),
            ("التخزين", "السعة", "128 جيجابايت"),
            ("الاتصال", "منفذ الشحن", "USB-C"),
        ],
    },
    {
        "slug": "samsung-galaxy-s24-256gb",
        "name_ar": "سامسونج جالكسي S24 - 256 جيجابايت",
        "name_en": "Samsung Galaxy S24 256GB",
        "brand": "samsung",
        "category": "phones",
        "model_number": "SM-S921B",
        "release_date": date(2024, 1, 17),
        "description_ar": "جالكسي S24 بشاشة Dynamic AMOLED 2X ومعالج Snapdragon 8 Gen 3 وكاميرا 50 ميجابكسل.",
        "image": "https://placehold.co/600x600?text=Galaxy+S24",
        "specs": [
            ("الشاشة", "الحجم", "6.2 بوصة Dynamic AMOLED 2X"),
            ("المعالج", "المعالج", "Snapdragon 8 Gen 3"),
            ("الكاميرا", "الكاميرا الخلفية", "50 + 12 + 10 ميجابكسل"),
            ("التخزين", "السعة", "256 جيجابايت"),
            ("البطارية", "السعة", "4000 mAh"),
        ],
    },
    {
        "slug": "apple-macbook-air-m2-256gb",
        "name_ar": "ماك بوك إير M2 - 256 جيجابايت",
        "name_en": "Apple MacBook Air M2 256GB",
        "brand": "apple",
        "category": "laptops",
        "model_number": "A2681",
        "release_date": date(2022, 7, 15),
        "description_ar": "ماك بوك إير بمعالج Apple M2 وشاشة Liquid Retina وبطارية تدوم حتى 18 ساعة.",
        "image": "https://placehold.co/600x600?text=MacBook+Air+M2",
        "specs": [
            ("الشاشة", "الحجم", "13.6 بوصة Liquid Retina"),
            ("المعالج", "المعالج", "Apple M2 (8 أنوية)"),
            ("الذاكرة", "الرام", "8 جيجابايت"),
            ("التخزين", "السعة", "256 جيجابايت SSD"),
            ("البطارية", "مدة العمل", "حتى 18 ساعة"),
        ],
    },
    {
        "slug": "asus-rog-strix-g16",
        "name_ar": "أسوس ROG Strix G16",
        "name_en": "ASUS ROG Strix G16",
        "brand": "asus",
        "category": "gaming-pc",
        "model_number": "G614JV",
        "release_date": date(2023, 10, 1),
        "description_ar": "لابتوب قيمنق بمعالج Intel Core i9 وكرت شاشة RTX 4060 وشاشة 165Hz.",
        "image": "https://placehold.co/600x600?text=ROG+Strix+G16",
        "specs": [
            ("الشاشة", "الحجم", "16 بوصة FHD بمعدل تحديث 165Hz"),
            ("المعالج", "المعالج", "Intel Core i9-13980HX"),
            ("كرت الشاشة", "GPU", "NVIDIA GeForce RTX 4060 8GB"),
            ("الذاكرة", "الرام", "16 جيجابايت DDR5"),
            ("التخزين", "السعة", "1 تيرابايت SSD NVMe"),
        ],
    },
    {
        "slug": "nvidia-geforce-rtx-4070",
        "name_ar": "كرت شاشة NVIDIA GeForce RTX 4070",
        "name_en": "NVIDIA GeForce RTX 4070",
        "brand": "nvidia",
        "category": "gpu",
        "model_number": "RTX4070",
        "release_date": date(2023, 4, 13),
        "description_ar": "كرت شاشة بمعمارية Ada Lovelace وذاكرة 12 جيجابايت GDDR6X.",
        "image": "https://placehold.co/600x600?text=RTX+4070",
        "specs": [
            ("الأداء", "المعمارية", "NVIDIA Ada Lovelace"),
            ("الذاكرة", "VRAM", "12 جيجابايت GDDR6X"),
            ("التوصيل", "الواجهة", "PCIe 4.0"),
            ("الطاقة", "الاستهلاك التقريبي", "200 واط"),
        ],
    },
    {
        "slug": "samsung-odyssey-g7-27",
        "name_ar": "شاشة سامسونج Odyssey G7 27 بوصة",
        "name_en": 'Samsung Odyssey G7 27"',
        "brand": "samsung",
        "category": "monitors",
        "model_number": "LC27G75TQSMXUE",
        "release_date": date(2020, 9, 1),
        "description_ar": "شاشة قيمنق منحنية بدقة QHD ومعدل تحديث 240Hz وزمن استجابة 1ms.",
        "image": "https://placehold.co/600x600?text=Odyssey+G7",
        "specs": [
            ("الشاشة", "الدقة", "2560×1440 (QHD)"),
            ("الشاشة", "معدل التحديث", "240 هرتز"),
            ("الشاشة", "زمن الاستجابة", "1 ميلي ثانية"),
            ("التصميم", "الانحناء", "1000R منحنية"),
        ],
    },
]


def run():
    app = create_app()
    with app.app_context():
        print("🌱 بدء إضافة منتجات تجريبية (Demo Catalog)...")

        for item in PRODUCTS:
            existing = Product.query.filter_by(slug=item["slug"]).first()
            if existing:
                print(f"⏭️  موجود مسبقًا: {item['name_ar']}")
                continue

            brand = Brand.query.filter_by(slug=item["brand"]).first()
            category = Category.query.filter_by(slug=item["category"]).first()

            if not brand or not category:
                print(f"⚠️  تخطّي {item['name_ar']} - العلامة التجارية أو التصنيف غير موجود")
                continue

            product = Product(
                name_ar=item["name_ar"],
                name_en=item["name_en"],
                slug=item["slug"],
                description_ar=item["description_ar"],
                model_number=item["model_number"],
                release_date=item["release_date"],
                brand_id=brand.id,
                category_id=category.id,
            )
            db.session.add(product)
            db.session.flush()

            db.session.add(
                ProductImage(
                    product_id=product.id, image_url=item["image"], is_primary=True, sort_order=0
                )
            )

            for sort_order, (group_name, key_ar, value_ar) in enumerate(item["specs"]):
                db.session.add(
                    Specification(
                        product_id=product.id,
                        group_name=group_name,
                        key_ar=key_ar,
                        key_en=key_ar,
                        value_ar=value_ar,
                        value_en=value_ar,
                        sort_order=sort_order,
                    )
                )

            print(f"✅ تمت إضافة: {item['name_ar']}")

        db.session.commit()
        print("🎉 تمت إضافة المنتجات التجريبية بنجاح!")
        print("ℹ️  ملاحظة: هذه المنتجات بدون أسعار حاليًا (لا توجد بيانات سعر حقيقية بعد).")


if __name__ == "__main__":
    run()
