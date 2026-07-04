import os
import sys

# 1. Kök dizini belirliyoruz
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# 2. TEŞHİS MOTORU: Bilgisayardaki gerçek dosya yapısını tarıyoruz
print("\n🔍 [DİZİN TARAMASI] src/core altındaki gerçek klasör yapısı:")
core_path = os.path.join(ROOT_DIR, "src", "core")

if os.path.exists(core_path):
    for root, dirs, files in os.walk(core_path):
        # Sadece python dosyalarını listele (pycache'leri geç)
        py_files = [f for f in files if f.endswith('.py') and not f.startswith('__')]
        if py_files or dirs:
            relative_path = os.path.relpath(root, ROOT_DIR)
            print(f"📁 Klasör: {relative_path}")
            for f in py_files:
                print(f"   📄 Dosya: {f}")
else:
    print("❌ HATA: Projede 'src/core' adında bir klasör bulunamadı!")

print("="*60 + "\n")

# 3. Çevre değişkeni koruması
os.environ["ENVIRONMENT"] = "development"
os.environ["OPENAI_API_KEY"] = "mock"
os.environ["AWS_ACCESS_KEY_ID"] = "mock"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["SLACK_WEBHOOK_URL"] = "mock"

# 4. Dinamik import denemesi
try:
    from src.core.services.optimization_service import OptimizationService
    print("✅ BAĞLANTI BAŞARILI: Modül başarıyla içe aktarıldı!")
except ModuleNotFoundError as e:
    print(f"❌ İMPORT HATASI DETAYI: {str(e)}")
    print("💡 Yukarıdaki dizin taramasına bakarak dosya adını veya klasör yolunu kontrol etmelisin.\n")
    sys.exit(1)