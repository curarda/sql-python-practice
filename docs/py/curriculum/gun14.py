"""Bölüm 14: Temel istatistik ve analiz — korelasyon, A/B testi, regresyon."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=14,
    baslik="Temel istatistik ve analiz",
    anlatim="""
Tablolar "ne oldu?" sorusunu cevaplar; istatistik "bu fark gerçek mi, yoksa şans mı?"
sorusuna geçer. Kullanılan kütüphane: `scipy.stats`.

**Korelasyon (r)**, iki sayısal değişkenin birlikte ne kadar doğrusal hareket ettiğini
-1 ile +1 arasında ölçer (`df[["a","b"]].corr()`, `stats.pearsonr(...)`). Korelasyon
**nedensellik değildir**: üçüncü bir değişken (confounder) ikisini birlikte hareket
ettiriyor olabilir.

**Hipotez testi terimleri**: **H0** ("gerçek fark yok"), **p değeri** (H0 doğruysa, en az bu
büyüklükte bir farkı şans eseri görme olasılığı), **alfa** (karar eşiği, genelde 0,05;
p < alfa ise "istatistiksel olarak anlamlı"). p değeri "B'nin daha iyi olma olasılığı"
**değildir**.

**İki ortalamayı karşılaştırmak** için Welch t-testi kullanılır:
`stats.ttest_ind(b, a, equal_var=False)` — varyansların eşit olduğunu varsaymaz, güvenli
varsayılan budur.

**Güç (power)**: gerçekten bir fark varken testin onu yakalama olasılığı (hedef ~%80).
Küçük bir örneklemle "anlamlı fark çıkmadı" demek çoğu zaman "bu örneklemle yakalama
şansımız düşüktü" demektir — "B işe yaramıyor" değil. Regresyon (`statsmodels`), bir
sonucun açıklayıcı değişkenlerle ilişkisini sayıya döker; katsayıyı "neden olur" değil
"ilişkilidir" diye yorumla.
""",
    ornek="""from scipy import stats
r, p = stats.pearsonr(reklam_satis["reklam"], reklam_satis["satis"])
print(round(r, 2), round(p, 4))   # -> 0.85 çok küçük bir p değeri""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="100 testten 10'u gerçekten etkili olsa bile, p<0,05 ile 'anlamlı' çıkan sonuçların yaklaşık %36'sı aslında etkisizdir (taban oranı düşükse yanlış pozitifler çoğalır).",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b14-s01",
        gun=14,
        tur="python",
        kavram="Korelasyon",
        soru="`reklam_satis` tablosunda `reklam` ile `satis` arasındaki korelasyon katsayısını (2 ondalık) `result`'a yaz.",
        beklenen="result = 0.85",
        ipucu="df[['reklam','satis']].corr() 2x2'lik bir tablo döndürür; .iloc[0,1] ile köşegen dışı değeri al.",
        cozum="result = round(reklam_satis[['reklam', 'satis']].corr().iloc[0, 1], 2)",
        tablo="reklam_satis",
    ),
    Soru(
        id="b14-s02",
        gun=14,
        tur="python",
        kavram="İki grup t-testi",
        soru=(
            "`sepet_testi` tablosunda `grup` sütunu 'A' ve 'B' değerlerini taşıyor. İki grubun ortalama "
            "`tutar`'ını Welch t-testiyle (`equal_var=False`) karşılaştır. A ve B'nin ortalamalarını "
            "(1 ondalık) ve p değerinin 0,05'ten küçük olup olmadığını `(ort_a, ort_b, anlamli_mi)` "
            "biçiminde `result`'a yaz."
        ),
        beklenen="result = (427.8, 454.5, True)",
        ipucu="from scipy import stats; a = sepet_testi[sepet_testi['grup']=='A']['tutar']; stats.ttest_ind(b, a, equal_var=False).",
        cozum=(
            "from scipy import stats\n"
            "a = sepet_testi[sepet_testi['grup'] == 'A']['tutar']\n"
            "b = sepet_testi[sepet_testi['grup'] == 'B']['tutar']\n"
            "_, p = stats.ttest_ind(b, a, equal_var=False)\n"
            "result = (round(a.mean(), 1), round(b.mean(), 1), bool(p < 0.05))"
        ),
        tablo="sepet_testi",
    ),
]
