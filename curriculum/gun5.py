"""Bölüm 5: Fonksiyonlar, modüller, hata yönetimi, dosya işlemleri."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=5,
    baslik="Fonksiyonlar ve hata yönetimi",
    anlatim=(
        "Bu bölümde kendi fonksiyonlarını yazmayı (`def`, `lambda`), bir işlem başarısız "
        "olabileceğinde programın çökmesini önlemeyi (`try/except`) ve kısaca dosya/klasör "
        "işlemlerini öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="Çıplak `except:` her hatayı yutar; hangi hatayı beklediğini (ValueError, KeyError...) her zaman yaz.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b5-s01",
        gun=5,
        tur="python",
        kavram="def ile fonksiyon",
        anlatim="""
`def ad(parametreler):` ile bir fonksiyon tanımlanır, fonksiyonun gövdesi girintili
yazılır, `return` sonucu çağıran yere geri verir. Parametrelere varsayılan değer vermek
için `def ad(parametre=varsayilan):` kullanılır; o parametre verilmezse varsayılan
kullanılır. Bir fonksiyonu bir kez doğru yazıp defalarca çağırmak, aynı kodu her yerde
kopyalamaktan daha az hataya açıktır.
""",
        ornek="""def kdv_dahil(tutar, oran=0.20):
    \"\"\"Tutara KDV ekler; oran verilmezse %20 kullanılır.\"\"\"
    return round(tutar * (1 + oran), 2)

print(kdv_dahil(1000))        # -> 1200.0
print(kdv_dahil(1000, 0.10))  # -> 1100.0""",
        ornek_dili="python",
        soru='`buyume(eski, yeni)` adında, yüzde değişimi virgülden sonra bir basamakla döndüren ve `eski` sıfırsa `None` döndüren bir fonksiyon yaz. `result = [buyume(5000, 3340), buyume(3340, 9790)]` yaz.',
        beklenen="result = [-33.2, 193.1]",
        ipucu="Yüzde değişim: (yeni - eski) / eski * 100. round(..., 1) ile yuvarla.",
        cozum=(
            "def buyume(eski, yeni):\n"
            "    if eski == 0:\n"
            "        return None\n"
            "    return round((yeni - eski) / eski * 100, 1)\n\n"
            "result = [buyume(5000, 3340), buyume(3340, 9790)]"
        ),
    ),
    Soru(
        id="b5-s02",
        gun=5,
        tur="python",
        kavram="try / except",
        anlatim="""
**Hata yönetimi**: bir işlem başarısız olabileceğinde (ör. `float("abc")` sayıya
çevrilemez) programın çökmesini `try / except` ile engellersin: `try` bloğundaki kod
denenir, hata olursa `except` bloğu çalışır ve program devam eder. Belirli bir hata türünü
yakala (`except ValueError`), her şeyi yutan çıplak `except:` yazma — gerçek bir
programlama hatasını da gizleyebilir ve hatayı bulmanı zorlaştırır.
""",
        ornek="""for metin in ["12", "xyz", "7"]:
    try:
        print(int(metin))
    except ValueError:
        print(f"{metin!r} bir sayı değil, atlandı")
# -> 12   "'xyz' bir sayı değil, atlandı"   7""",
        ornek_dili="python",
        soru='`fiyatlar_metin = ["750", "abc", "1900"]` listesindeki her elemanı `float`\'a çevirmeyi dene; çevrilemeyeni (`"abc"`) atla. Çevrilebilenlerin toplamını `result`\'a yaz.',
        beklenen="result = 2650.0",
        ipucu="try/except ValueError içinde float(f) çağır; hata olursa continue ya da pass kullan.",
        cozum=(
            'fiyatlar_metin = ["750", "abc", "1900"]\n'
            "result = 0.0\n"
            "for f in fiyatlar_metin:\n"
            "    try:\n"
            "        result += float(f)\n"
            "    except ValueError:\n"
            "        pass"
        ),
    ),
    Soru(
        id="b5-s03",
        gun=5,
        tur="python",
        kavram="lambda ile sıralama",
        anlatim="""
`lambda parametre: ifade`, tek satırlık, isimsiz bir fonksiyondur; genelde `sorted(...,
key=lambda x: ...)` gibi başka bir fonksiyona "nasıl sıralanacağını" söylemek için
kullanılır — ayrı bir `def` yazmaya değmeyecek kadar küçük işler için pratiktir.

Hatırlatma: `import kutuphane` ile başkasının yazdığı kodu kullanırsın (`import pandas as
pd` gibi bir takma adla); kendi dosyalarını da `import dosya_adi` ile içe aktarabilirsin.
Dosya/klasör işlemleri için `pathlib.Path` kullanılır: `Path("veri").glob("*.csv")` bir
klasördeki bütün CSV dosyalarını listeler (Bölüm 11'de `concat` ile birlikte kullanılır).
""",
        ornek="""urunler = [("Kulaklık", 3), ("Mont", 1), ("Roman", 7)]
result_ornek = sorted(urunler, key=lambda x: x[1])   # ikinci elemana (adet) göre
print(result_ornek)    # -> [('Mont', 1), ('Kulaklık', 3), ('Roman', 7)]""",
        ornek_dili="python",
        soru='`ciftler = [("Mont", 2400), ("Roman", 180), ("Klavye", 1100)]` listesini ikinci elemana (fiyata) göre küçükten büyüğe sırala, `result`\'a yaz.',
        beklenen="result = [('Roman', 180), ('Klavye', 1100), ('Mont', 2400)]",
        ipucu="sorted(ciftler, key=lambda x: x[1]) fiyata göre sıralar.",
        cozum='ciftler = [("Mont", 2400), ("Roman", 180), ("Klavye", 1100)]\nresult = sorted(ciftler, key=lambda x: x[1])',
    ),
]
