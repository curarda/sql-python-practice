"""Bölüm 6: NumPy temelleri — array ve vektörleştirme."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=6,
    baslik="NumPy temelleri",
    anlatim="""
NumPy, sayı dizileriyle (array) hızlı çalışmanın kütüphanesidir; pandas'ın altyapısıdır.
Bir `np.array` üzerindeki işlem tek tek elemanlara değil, dizinin tamamına birden uygulanır
(**vektörleştirme**); bu, aynı işi Python döngüsüyle yapmaktan onlarca kat hızlıdır.

```
fiyatlar = np.array([750, 2400, 1100, 180, 1900])
adetler  = np.array([2, 1, 1, 3, 1])
ciro = fiyatlar * adetler        # eleman eleman çarpım, döngü yazmadan
```

İki boyutlu dizilerde `axis=0` sütun yönünde (aşağı), `axis=1` satır yönünde (yana) işlem
yapar: `matris.sum(axis=1)` her satırın toplamını verir.

**Eksik değer**: NumPy'de `np.nan` kullanılır; `np.mean([1, np.nan])` sonucu `nan` olur,
`np.nanmean(...)` NaN'ları atlayarak hesaplar. `np.isnan(dizi)` her eleman için True/False
döndürür.

**Rastgele sayı**: `rng = np.random.default_rng(tohum)` tekrarlanabilir bir üretici verir;
aynı tohumla her çalıştırmada aynı sayılar çıkar. Bu kitapçıktaki bütün örnek veriler böyle
üretildi; `rng.uniform`, `rng.integers`, `rng.normal`, `rng.choice` en sık kullanılanlardır.
""",
    ornek="""rng = np.random.default_rng(7)
print(rng.integers(0, 10, 5))     # -> aynı tohumla her zaman aynı 5 sayı""",
    ornek_dili="python",
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
        soru="`veri = np.array([10, np.nan, 20, 30])` için NaN'ları atlayarak ortalamayı ve kaç tane NaN olduğunu `(ortalama, nan_sayisi)` biçiminde `result`'a yaz.",
        beklenen="result = (20.0, 1)",
        ipucu="np.nanmean NaN'ları atlar; np.isnan(veri).sum() NaN sayısını verir.",
        cozum="veri = np.array([10, np.nan, 20, 30])\nresult = (float(np.nanmean(veri)), int(np.isnan(veri).sum()))",
    ),
]
