"""Bölüm 6: NumPy temelleri — array ve vektörleştirme."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=6,
    baslik="NumPy temelleri",
    anlatim=(
        "Bu bölümde NumPy dizileriyle vektörleştirilmiş işlemleri, çok boyutlu dizilerde "
        "axis kavramını, eksik değer (NaN) ile çalışmayı ve tekrarlanabilir rastgele sayı "
        "üretimini öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="Bir milyon satırda vektörleştirilmiş bir toplama işlemi, aynı işi yapan bir for döngüsünden genellikle 50-100 kat hızlıdır.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b6-s01",
        gun=6,
        tur="python",
        kavram="Vektörleştirilmiş çarpım",
        anlatim="""
NumPy, sayı dizileriyle (array) hızlı çalışmanın kütüphanesidir; pandas'ın altyapısıdır.
Bir `np.array` üzerindeki işlem tek tek elemanlara değil, dizinin tamamına birden uygulanır
(**vektörleştirme**); bu, aynı işi Python döngüsüyle yapmaktan onlarca kat hızlıdır, çünkü
döngü her elemanı tek tek Python seviyesinde işlerken, vektörleştirilmiş işlem dizinin
tamamını optimize edilmiş C koduyla birden işler.
""",
        ornek="""birim = np.array([100, 250, 80])
adet = np.array([3, 2, 5])
ciro = birim * adet          # eleman eleman çarpım, döngü yazmadan
print(ciro, ciro.sum())      # -> [300 500 400] 1200""",
        ornek_dili="python",
        soru="`fiyatlar = np.array([750, 2400, 1100, 180, 1900])` ve `adetler = np.array([2, 1, 1, 3, 1])` dizilerini eleman eleman çarpıp toplamını (toplam ciro) `result`'a float olarak yaz.",
        beklenen="result = 7440.0",
        ipucu="(fiyatlar * adetler).sum() döngü yazmadan toplam ciroyu verir.",
        cozum=(
            "fiyatlar = np.array([750, 2400, 1100, 180, 1900])\n"
            "adetler = np.array([2, 1, 1, 3, 1])\n"
            "result = float((fiyatlar * adetler).sum())"
        ),
    ),
    Soru(
        id="b6-s02",
        gun=6,
        tur="python",
        kavram="2 boyutlu dizi ve axis",
        anlatim="""
İki boyutlu bir dizide (satır × sütun) bir işlemin hangi yönde yapılacağını `axis`
parametresi belirler: `axis=0` **sütun yönünde** (aşağı doğru, her sütunu kendi içinde),
`axis=1` **satır yönünde** (yana doğru, her satırı kendi içinde) işler. Ezberlemenin
kolay yolu: `axis=1` dediğinde sonucun satır sayısı kadar eleman çıkar (her satır için bir
değer).
""",
        ornek="""matris = np.array([[10, 20], [1, 2], [100, 200]])
print(matris.sum(axis=1))   # -> [30  3 300]   (her SATIRın toplamı, 3 değer)
print(matris.sum(axis=0))   # -> [111 222]     (her SÜTUNun toplamı, 2 değer)""",
        ornek_dili="python",
        soru="`matris = np.array([[1, 2, 3], [4, 5, 6]])` için her satırın toplamını bir liste olarak `result`'a yaz.",
        beklenen="result = [6, 15]",
        ipucu="axis=1 satır yönünde (yana) toplar: matris.sum(axis=1).tolist().",
        cozum="matris = np.array([[1, 2, 3], [4, 5, 6]])\nresult = matris.sum(axis=1).tolist()",
    ),
    Soru(
        id="b6-s03",
        gun=6,
        tur="python",
        kavram="NaN ile çalışmak",
        anlatim="""
**Eksik değer**: NumPy'de eksik sayısal değer `np.nan` ile gösterilir. Sıradan `np.mean([1,
np.nan])` çağrısı, içinde NaN olan her hesaplamayı "kirletir" ve sonuç `nan` çıkar;
`np.nanmean(...)` ise NaN'ları yok sayarak geri kalanların ortalamasını alır.
`np.isnan(dizi)` her eleman için True/False döner, `.sum()` ile kaç tane NaN olduğunu
sayabilirsin.

**Rastgele sayı**: `rng = np.random.default_rng(tohum)` tekrarlanabilir bir üretici verir;
aynı tohumla her çalıştırmada birebir aynı sayılar çıkar. Bu uygulamadaki bütün örnek
veriler böyle üretildi; `rng.uniform` (aralıkta ondalıklı), `rng.integers` (aralıkta tam
sayı), `rng.normal` (normal dağılım), `rng.choice` (bir listeden rastgele seçim) en sık
kullanılanlardır.
""",
        ornek="""veri = np.array([5.0, np.nan, 15.0])
print(np.mean(veri))         # -> nan  (NaN her şeyi kirletir)
print(np.nanmean(veri))      # -> 10.0  (NaN atlanır)
print(np.isnan(veri).sum())  # -> 1""",
        ornek_dili="python",
        soru="`veri = np.array([10, np.nan, 20, 30])` için NaN'ları atlayarak ortalamayı ve kaç tane NaN olduğunu `(ortalama, nan_sayisi)` biçiminde `result`'a yaz.",
        beklenen="result = (20.0, 1)",
        ipucu="np.nanmean NaN'ları atlar; np.isnan(veri).sum() NaN sayısını verir.",
        cozum="veri = np.array([10, np.nan, 20, 30])\nresult = (float(np.nanmean(veri)), int(np.isnan(veri).sum()))",
    ),
]
