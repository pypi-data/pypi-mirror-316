# Mistral Image Generator

مكتبة Python لتوليد الصور باستخدام Mistral AI API.

## التثبيت

```bash
pip install mistral-image-gen
```

## الاستخدام الأساسي

```python
from mistral_image_gen import MistralImageGenerator

# إنشاء نسخة من المولد
generator = MistralImageGenerator()

# توليد صورة واحدة
image_path = generator.generate_image("سيارة رياضية حمراء جميلة")
print(f"تم حفظ الصورة في: {image_path}")

# توليد عدة صور دفعة واحدة
prompts = [
    "قطة صغيرة تلعب بكرة",
    "غروب الشمس على الشاطئ",
    "حديقة مليئة بالزهور"
]
image_paths = generator.batch_generate(prompts, prefix="my_images_")
print(f"تم إنشاء {len(image_paths)} صور")
```

## المميزات

- توليد صور من وصف نصي
- دعم توليد صور متعددة دفعة واحدة
- إمكانية تخصيص مجلد حفظ الصور
- معالجة الأخطاء وإعادة المحاولة تلقائياً
- تنسيق أسماء الملفات تلقائياً

## المساهمة

نرحب بمساهماتكم! يرجى إرسال pull requests أو فتح issues على GitHub.

## الترخيص

هذا المشروع مرخص تحت MIT License.
