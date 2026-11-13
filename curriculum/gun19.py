"""Bölüm 19: Uçtan uca vaka — e-ticaret satış analizi."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=19,
    baslik="Uçtan uca vaka: e-ticaret satış analizi",
    anlatim=(
        "Yöneticinin mesajı: \"Yıllık performansı özetleyen bir sayfa hazırlar mısın? Hangi "
        "kategori öne çıkıyor, mevsimsellik var mı, iadeler ne durumda?\" Bu bölümde "
        "temizlikten KPI'lara, kategori kırılımından mevsimselliğe ve yöneticiye giden "
        "özete kadar bütün adımları, gerçekçi şekilde kirletilmiş bir e-ticaret veri "
        "setinde (`vaka_siparisler`, ~6000 satır; `musteriler`, 800 satır) uygulayacaksın."
    ),
    metrikler=[
        Metrik(
            baslik="Yöntem notu",
            aciklama="Her alt soru, temizliği (tarih çevir, kategori düzelt, tekrarları at, geçersiz tutarı çıkar) baştan uygular — gerçek işte de her analiz, aynı ham veriden tekrar başlar.",
        ),
    ],
)

_PIPELINE_IPUCU = (
    "Sıra: tarihi/kategoriyi düzelt, drop_duplicates(), tutarı boş/negatif olan satırları çıkar, "
    "net_tutar = np.where(s['iade'], 0, s['tutar']) ekle."
)

SORULAR = [
    Soru(
        id="b19-s01",
        gun=19,
        tur="python",
        kavram="Vaka: temizlik sayımı",
        anlatim="""
Görev belirsiz görünüyor ama aslında dört soru içeriyor: (1) toplam performans (KPI'lar),
(2) kategori kırılımı, (3) zaman içindeki örüntü, (4) iadeler. Analize başlamadan önce bu
soruları yazmak, her tablo ve grafiğin bunlardan birine cevap vermesini sağlar.

`vaka_siparisler` gerçek hayattaki sorunları taşıyor: Türkçe biçimli bir CSV'den yeni
okunmuş gibi `tarih` hâlâ metin (`gg.aa.yyyy`), bazı kategoriler büyük harfli ve fazladan
boşluklu (`"ELEKTRONIK "`), bazı tutarlar boş ya da negatif, ve tekrar eden satırlar var.
Her temizlik adımından sonra satır sayısını yazdırmak ("6.030 satırla başladım, 58'i
çıktı, 5.972 kaldı") hem bir kontrol hem de raporun ilk cümlesidir.
""",
        ornek="""toy = pd.DataFrame({"id": [1, 1, 2, 3], "tutar": [100, 100, -5, None]})
basla = len(toy)
toy = toy.drop_duplicates()
toy = toy[toy["tutar"].notna() & (toy["tutar"] > 0)]
print(basla, "->", len(toy))    # -> 4 -> 1   (1 tekrar, 1 negatif, 1 boş çıktı)""",
        ornek_dili="python",
        soru=(
            "`vaka_siparisler` tablosunu temizle: `kategori`'yi `.str.strip().str.title()` ile düzelt, "
            "tekrar eden satırları at, `tutar`'ı boş (NaN) veya 0/negatif olan satırları çıkar. "
            "Başlangıç satır sayısı, bitiş satır sayısı ve çıkan satır sayısını `{'basla':.., "
            "'bitti':.., 'cikan':..}` biçiminde `result`'a yaz."
        ),
        beklenen="result = {'basla': 6030, 'bitti': 5972, 'cikan': 58}",
        ipucu=_PIPELINE_IPUCU,
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "basla = len(s)\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "result = {'basla': basla, 'bitti': len(s), 'cikan': basla - len(s)}"
        ),
        tablo="vaka_siparisler",
        kirlilik="6030 satırdan 30'u birebir tekrar, 25'i boş tutar, 3'ü negatif tutar.",
    ),
    Soru(
        id="b19-s02",
        gun=19,
        tur="python",
        kavram="Vaka: ana göstergeler (KPI)",
        anlatim="""
KPI (key performance indicator, temel performans göstergesi), bir işin sağlığını
özetleyen birkaç sayıdır: toplam ciro, sipariş sayısı, müşteri sayısı, ortalama/medyan
sepet, iade oranı. İade edilen bir sipariş gerçek geliri temsil etmez; bu yüzden
`net_tutar` sütunu iade edilenlerde 0'dır (`np.where(s["iade"], 0, s["tutar"])`) ve KPI'lar
bu sütun üzerinden hesaplanır. Ortalama ile medyan arasındaki fark burada da önemlidir:
ikisi birbirinden uzaksa, birkaç büyük sipariş ortalamayı yukarı çekiyordur; "tipik
sipariş" için medyanı raporla.
""",
        ornek="""toy = pd.DataFrame({"musteri": ["A", "A", "B"], "tutar": [100, 300, 50], "iade": [False, True, False]})
toy["net_tutar"] = np.where(toy["iade"], 0, toy["tutar"])
print({"ciro": float(toy["net_tutar"].sum()), "musteri": int(toy["musteri"].nunique())})
# -> {'ciro': 150.0, 'musteri': 2}   (300'lük iade ciroya katılmadı)""",
        ornek_dili="python",
        soru=(
            "Temizlikten sonra (b19-s01'deki gibi) `net_tutar` sütununu ekle (iade edilen sipariş 0). "
            "`{'net_ciro':.., 'siparis':.., 'musteri':.., 'ort_sepet':.., 'medyan_sepet':.., "
            "'iade_orani':..}` sözlüğünü `result`'a yaz: ciro ve sepet tutarları en yakın tam sayıya, "
            "iade oranı 0-1 arası 3 ondalığa yuvarlanmış olsun."
        ),
        beklenen="result = {'net_ciro': 5035451, 'siparis': 5972, 'musteri': 771, 'ort_sepet': 918, 'medyan_sepet': 647, 'iade_orani': 0.09}",
        ipucu="Ortalama medyandan belirgin yüksek çıkabilir: birkaç pahalı elektronik siparişi ortalamayı çekiyor.",
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "s['net_tutar'] = np.where(s['iade'], 0, s['tutar'])\n"
            "result = {\n"
            "    'net_ciro': round(float(s['net_tutar'].sum())),\n"
            "    'siparis': int(len(s)),\n"
            "    'musteri': int(s['musteri_id'].nunique()),\n"
            "    'ort_sepet': round(float(s['tutar'].mean())),\n"
            "    'medyan_sepet': round(float(s['tutar'].median())),\n"
            "    'iade_orani': round(float(s['iade'].mean()), 3),\n"
            "}"
        ),
        tablo="vaka_siparisler",
        kirlilik="Temizlik yapılmazsa tutar toplamına NaN ve negatif değerler karışır, sayı anlamsızlaşır.",
    ),
    Soru(
        id="b19-s03",
        gun=19,
        tur="python",
        kavram="Vaka: kategori özeti",
        anlatim="""
"Hangi kategori öne çıkıyor?" sorusunun cevabı bir `groupby("kategori").agg(...)`
tablosudur: sipariş sayısı, brüt (iade dahil) ve net (iade hariç) ciro, iade oranı,
ortalama sepet — hepsi aynı anda. `net`'e göre azalan sıralamak, en büyük katkıyı yapan
kategoriyi en üste getirir. Bir kategorinin **sipariş sayısında** önde olması, **ciroda**
da önde olacağı anlamına gelmez (Bölüm 10'daki Ankara/İstanbul örneği gibi); ikisini
birlikte raporlamak gerekir.
""",
        ornek="""toy = pd.DataFrame({
    "kategori": ["A", "A", "B"], "tutar": [100, 50, 400], "iade": [False, False, True],
})
toy["net_tutar"] = np.where(toy["iade"], 0, toy["tutar"])
ozet = toy.groupby("kategori").agg(siparis=("tutar", "count"), net=("net_tutar", "sum")).sort_values("net", ascending=False)
print(ozet)
# kategori  siparis  net
#        A        2  150
#        B        1    0""",
        ornek_dili="python",
        soru=(
            "Temizlikten sonra her kategori için `siparis` (sayı), `brut` (tutar toplamı), `net` "
            "(net_tutar toplamı), `iade_orani` (ortalama) ve `ort_sepet` (tutar ortalaması) sütunlarını "
            "hesapla (hepsi 1 ondalığa yuvarlı), `net`'e göre azalan sırala. Sonucu `result`'a yaz."
        ),
        beklenen="5 satır (kategoriler), net azalan sırada: Elektronik, Ev, Giyim, Kozmetik, Kitap.",
        ipucu="groupby('kategori').agg(...).sort_values('net', ascending=False).round(1), sonra reset_index().",
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "s['net_tutar'] = np.where(s['iade'], 0, s['tutar'])\n"
            "kat = (s.groupby('kategori')\n"
            "         .agg(siparis=('siparis_no', 'count'), brut=('tutar', 'sum'), net=('net_tutar', 'sum'),\n"
            "              iade_orani=('iade', 'mean'), ort_sepet=('tutar', 'mean'))\n"
            "         .sort_values('net', ascending=False).round(1))\n"
            "result = kat.reset_index()"
        ),
        tablo="vaka_siparisler",
        sirali=True,
        kirlilik="Kategori temizlenmezse 'ELEKTRONIK ' ayrı bir grup olarak sayılır ve tablo bozulur.",
    ),
    Soru(
        id="b19-s04",
        gun=19,
        tur="python",
        kavram="Vaka: mevsimsellik (Kasım etkisi)",
        anlatim="""
"Mevsimsellik var mı?" sorusu, belirli bir tarih aralığının toplam içindeki payına
bakılarak cevaplanır: `s[(s["tarih"] >= baslangic) & (s["tarih"] <= bitis)]` ile o
aralığı filtrele, `net_tutar` toplamını genel toplama böl. Yılın küçük bir yüzdesini
oluşturan birkaç günün (ör. büyük bir indirim dönemi), cironun şaşırtıcı derecede büyük
bir kısmını getirmesi mümkündür — bu tür pencereler stok ve kampanya planlamasının en
kritik noktasıdır. Bölüm 12'deki uyarı burada da geçerli: `tarih` metin olduğu sürece bu
karşılaştırma çalışmaz, önce `pd.to_datetime(..., format=...)` ile çevirmen gerekir.
""",
        ornek="""gunler = pd.date_range("2026-01-01", "2026-01-10", freq="D")
toy = pd.DataFrame({"tarih": gunler, "net_tutar": [10, 10, 10, 10, 10, 10, 10, 10, 100, 100]})
pencere = toy[(toy["tarih"] >= "2026-01-09") & (toy["tarih"] <= "2026-01-10")]
print(round(float(pencere["net_tutar"].sum() / toy["net_tutar"].sum()), 3))    # -> 0.714""",
        ornek_dili="python",
        soru=(
            "Temizlikten sonra `net_tutar` ekle. 20-30 Kasım 2025 (dahil) arasındaki net cironun, "
            "yıllık net ciro içindeki payını (0-1 arası, 3 ondalık) `result`'a yaz."
        ),
        beklenen="result = 0.082",
        ipucu="tarih'i datetime'a çevir, iki tarih arasını filtrele, toplamı genel toplama böl.",
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "s['tarih'] = pd.to_datetime(s['tarih'], format='%d.%m.%Y')\n"
            "s['net_tutar'] = np.where(s['iade'], 0, s['tutar'])\n"
            "kasim_sonu = s[(s['tarih'] >= '2025-11-20') & (s['tarih'] <= '2025-11-30')]\n"
            "result = round(float(kasim_sonu['net_tutar'].sum() / s['net_tutar'].sum()), 3)"
        ),
        tablo="vaka_siparisler",
        kirlilik="tarih sütunu metin (gg.aa.yyyy) olarak geliyor; önce datetime'a çevrilmeli.",
    ),
    Soru(
        id="b19-s05",
        gun=19,
        tur="python",
        kavram="Vaka: müşteri yoğunlaşması (Pareto)",
        anlatim="""
Bölüm 10'daki Pareto fikrinin aynısı burada da geçerli: müşterileri `net_tutar` toplamına
göre azalan sırala, en büyük dilimin payına bak. `mc.head(int(len(mc) * 0.1))` müşterilerin
en büyük %10'luk dilimini seçer; bu dilimin payı yüksekse (örn. cironun yarısından
fazlasıysa), o müşteri grubunun kaybı işi doğrudan sarsar — sadakat programı ve kişisel
iletişim için ilk aday listesi budur.
""",
        ornek="""toy = pd.Series([500, 300, 100, 50, 50], index=["M1", "M2", "M3", "M4", "M5"])  # zaten azalan
en_buyuk_tek = toy.head(1)
print(round(float(en_buyuk_tek.sum() / toy.sum()), 3))    # -> 0.5   (M1 tek başına yarısı)""",
        ornek_dili="python",
        soru=(
            "Temizlikten sonra `net_tutar` ekle. Müşterileri net_tutar toplamına göre sırala; en "
            "büyük %10'luk dilimin toplam net ciro içindeki payını (0-1 arası, 3 ondalık) `result`'a yaz."
        ),
        beklenen="result = 0.577",
        ipucu="musteri_id bazında net_tutar topla, azalan sırala, len(mc)*0.1 kadarının toplamını genel toplama böl.",
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "s['net_tutar'] = np.where(s['iade'], 0, s['tutar'])\n"
            "mc = s.groupby('musteri_id')['net_tutar'].sum().sort_values(ascending=False)\n"
            "result = round(float(mc.head(int(len(mc) * 0.1)).sum() / mc.sum()), 3)"
        ),
        tablo="vaka_siparisler",
        kirlilik="Tekrar eden satırlar temizlenmezse bazı müşterilerin cirosu yanlışlıkla iki katına çıkar.",
    ),
    Soru(
        id="b19-s06",
        gun=19,
        tur="python",
        kavram="Vaka: yöneticiye giden özet",
        anlatim="""
Analizin son ürünü kod değil, bir buçuk dakikada okunan bir metindir. İyi bir özetin dört
özelliği vardır: **her cümlede bir sayı** (soyut değil somut), bölümün başında yazdığın
dört soruyu (KPI, kategori, zaman, iade) **cevaplaması**, **tek bir öneri** (on tane değil)
ve **sınırlamaların dürüstçe belirtilmesi** ("X satır temizlik sırasında çıkarıldı" gibi).
Bu alıştırmada önceki beş noktada hesapladığın sayıları tek bir yerde topluyor ve bu
disipline uyan bir özet yazıyorsun.
""",
        ornek="""# Önceki noktalardaki hesapları birleştirip tek sözlükte topla:
ozet = {"net_ciro": 150.0, "musteri": 2, "en_riskli_kategori": "B"}
print(ozet)
# Sonra: "Toplam net ciro 150 TL, 2 müşteriden geldi. B kategorisinde iade oranı yüksek;
#         ürün açıklamalarının gözden geçirilmesini öneririm. Küçük örneklem nedeniyle
#         bu bulgu önümüzdeki ay teyit edilmeli."    <- 3 cümle, her birinde somut bir şey""",
        ornek_dili="python",
        soru=(
            "Temizlikten sonra şu beş göstergeyi hesapla ve `{'net_ciro':.., 'iade_orani_giyim':.., "
            "'kasim_sonu_payi':.., 'top10_pay':.., 'musteri':..}` biçiminde `result`'a yaz: net ciro "
            "(en yakın tam sayı), yalnızca Giyim kategorisinin iade oranı (3 ondalık), 20-30 Kasım "
            "payı (3 ondalık, b19-s04'teki gibi), en büyük %10 müşterinin payı (3 ondalık, b19-s05'teki "
            "gibi) ve tekil müşteri sayısı. Ardından aşağıdaki kutuya, bu beş sayıyı kullanarak "
            "yöneticiye 3 cümlelik bir özet yaz."
        ),
        beklenen=(
            "result = {'net_ciro': 5035451, 'iade_orani_giyim': 0.189, 'kasim_sonu_payi': 0.082, "
            "'top10_pay': 0.577, 'musteri': 771}. Ayrıca 3 cümlelik bir özet."
        ),
        ipucu="Her alt hesap önceki sorularla aynı; burada tek bir sözlükte topluyorsun.",
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "s['tarih'] = pd.to_datetime(s['tarih'], format='%d.%m.%Y')\n"
            "s['net_tutar'] = np.where(s['iade'], 0, s['tutar'])\n"
            "giyim = s[s['kategori'] == 'Giyim']\n"
            "kasim_sonu = s[(s['tarih'] >= '2025-11-20') & (s['tarih'] <= '2025-11-30')]\n"
            "mc = s.groupby('musteri_id')['net_tutar'].sum().sort_values(ascending=False)\n"
            "result = {\n"
            "    'net_ciro': round(float(s['net_tutar'].sum())),\n"
            "    'iade_orani_giyim': round(float(giyim['iade'].mean()), 3),\n"
            "    'kasim_sonu_payi': round(float(kasim_sonu['net_tutar'].sum() / s['net_tutar'].sum()), 3),\n"
            "    'top10_pay': round(float(mc.head(int(len(mc) * 0.1)).sum() / mc.sum()), 3),\n"
            "    'musteri': int(s['musteri_id'].nunique()),\n"
            "}"
        ),
        tablo="vaka_siparisler",
        ozet_gerekli=True,
        kirlilik="Tüm vaka boyunca kullanılan temizlik adımları (tekrar, boş/negatif tutar, kirli kategori, metin tarih) burada bir araya geliyor.",
        rubrik=(
            "1) Net ciro, müşteri sayısı ve tipik (medyan) sipariş tutarını bir cümlede veriyor mu?\n"
            "2) Giyim'in yüksek iade oranını ve Kasım sonu etkisini somut sayılarla belirtiyor mu?\n"
            "3) Tek bir öneri (ör. Giyim beden rehberi, Kasım stok planlaması) ve bir sınırlama notu içeriyor mu?"
        ),
    ),
]
