"""Bölüm 18: İyi pratikler — kod düzeni, Git, performans, hata ayıklama."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=18,
    baslik="İyi pratikler",
    anlatim="""
Bir analiz notebook'u genelde şu iskeleti izler: kütüphaneleri içe aktar → veriyi oku →
temizle → keşfet/özetle → grafik → sonuç. Her bölümü ayrı bir hücrede tut; bir hücre
yukarıdan aşağı tekrar çalıştırılabilmeli.

`assert koşul, "mesaj"` kodun kendi kendini kontrol etmesini sağlar: koşul yanlışsa program
orada durur ve mesajı gösterir (Bölüm 19'da `assert s["siparis_no"].is_unique` gibi).
Sessizce yanlış bir sonuç üretmektense erken ve gürültülü durmak tercih edilir.

**Git**, kodun zaman makinesidir: `git add`, `git commit -m "mesaj"`, `git push`. Takımda
kendi dalını (branch) açıp değişikliklerini orada yapmak, ana koda yanlışlıkla hata
eklemeni engeller. Veri dosyalarını `.gitignore`'a ekle — büyük ve genelde gizli veriler
depoya girmemeli.

**Performans**: veri büyüdüğünde döngü yerine vektörleştirilmiş işlem kullan (Bölüm 6);
gereksiz sütunları `usecols` ile en baştan ele; tekrar okunan büyük dosyaları `.parquet`
olarak sakla.

**Hata ayıklama**: hatayı küçük bir örnekle yeniden üret, `print()` ile ara adımları
göster, hatanın son satırını (traceback) dikkatle oku — genelde tam olarak hangi satırda
ve ne tür bir hata olduğunu söyler.
""",
    ornek="""def guvenli_bolme(a, b):
    if b == 0:
        return None
    return a / b

assert guvenli_bolme(10, 0) is None, "sıfıra bölme None dönmeli\"""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Mülakatta sık sorulan soru",
            aciklama="\"Neden for döngüsü yerine vektörleştirilmiş işlem?\" — çünkü NumPy/pandas işlemi C seviyesinde, tüm diziye birden uygular; Python döngüsü her elemanı ayrı ayrı yorumlar.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b18-s01",
        gun=18,
        tur="python",
        kavram="assert ile kendi kendini kontrol eden kod",
        soru="`guvenli_bolme(a, b)` fonksiyonunu yaz: `b` sıfırsa `None`, değilse `a / b` döndürsün. `result = [guvenli_bolme(10, 2), guvenli_bolme(10, 0)]` yaz.",
        beklenen="result = [5.0, None]",
        ipucu="if b == 0: return None satırını en başa koy.",
        cozum=(
            "def guvenli_bolme(a, b):\n"
            "    if b == 0:\n"
            "        return None\n"
            "    return a / b\n\n"
            "result = [guvenli_bolme(10, 2), guvenli_bolme(10, 0)]"
        ),
    ),
    Soru(
        id="b18-s02",
        gun=18,
        tur="python",
        kavram="Döngü yerine vektörleştirme",
        soru=(
            "`fiyatlar = [750, 2400, 1100, 180, 1900]` listesindeki her fiyata %20 KDV eklenmiş toplamı, "
            "for döngüsü **yazmadan**, NumPy ile vektörleştirilmiş şekilde hesapla ve `result`'a float olarak yaz."
        ),
        beklenen="result = 7596.0",
        ipucu="np.array(fiyatlar) * 1.20 bütün diziye birden uygulanır; .sum() ile topla.",
        cozum="fiyatlar = [750, 2400, 1100, 180, 1900]\nresult = float((np.array(fiyatlar) * 1.20).sum())",
    ),
]
