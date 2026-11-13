"""Bölüm 14: Temel istatistik ve analiz — korelasyon, A/B testi, regresyon."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=14,
    baslik="Temel istatistik ve analiz",
    anlatim=(
        "Tablolar \"ne oldu?\" sorusunu cevaplar; istatistik \"bu fark gerçek mi, yoksa "
        "şans mı?\" sorusuna geçer. Bu bölümde korelasyonu ve iki grubu karşılaştıran "
        "t-testini `scipy.stats` ile öğreneceksin."
    ),
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
        anlatim="""
**Korelasyon katsayısı (r)**, iki sayısal değişkenin birlikte ne kadar doğrusal hareket
ettiğini -1 ile +1 arasında ölçer: `df[["a", "b"]].corr()` ya da `stats.pearsonr(a, b)`
(r ve p değerini birlikte verir). Kabaca okuma: 0,3'ün altı zayıf, 0,3-0,7 orta, 0,7'nin
üstü güçlü ilişki. **Korelasyon nedensellik değildir**: üçüncü bir değişken (confounder,
karıştırıcı değişken) iki değişkeni birlikte hareket ettiriyor olabilir — dondurma
satışıyla boğulma vakaları ilişkilidir, çünkü ikisi de sıcak havada artar.
""",
        ornek="""from scipy import stats
sicaklik = [18, 22, 25, 30, 15, 28]
dondurma_satisi = [40, 65, 80, 110, 20, 95]
r, p = stats.pearsonr(sicaklik, dondurma_satisi)
print(round(r, 2))    # -> 0.99  (çok güçlü, ama nedensellik iddiası için yeterli değil)""",
        ornek_dili="python",
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
        anlatim="""
Hipotez testinin terimleri: **H0** (sıfır hipotezi, "gerçek bir fark yok, gördüğüm fark
şans eseri"), **p değeri** (H0 doğru olsaydı, en az bu büyüklükte bir farkı şans eseri
görme olasılığı), **alfa** (karar eşiği, genelde 0,05; `p < alfa` ise "istatistiksel olarak
anlamlı" denir). p değeri "B'nin daha iyi olma olasılığı" **değildir**.

İki grubun **ortalamasını** karşılaştırırken Welch t-testi kullanılır:
`stats.ttest_ind(grup_b, grup_a, equal_var=False)` — varyansların eşit olduğunu
varsaymaz, güvenli varsayılan budur. **Güç (power)**: gerçekten bir fark varken testin onu
yakalama olasılığıdır (hedef ~%80); küçük bir örneklemle "anlamlı çıkmadı" demek çoğu
zaman "yakalama şansımız düşüktü" demektir, "fark yok" değil.
""",
        ornek="""from scipy import stats
eski_sure = [12, 15, 11, 14, 13, 16, 12]
yeni_sure = [10, 9, 11, 8, 10, 12, 9]
t, p = stats.ttest_ind(yeni_sure, eski_sure, equal_var=False)
print(round(p, 4), p < 0.05)   # küçük bir p -> fark muhtemelen tesadüf değil""",
        ornek_dili="python",
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
