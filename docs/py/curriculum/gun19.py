"""Bölüm 19: Uçtan uca vaka — e-ticaret satış analizi."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=19,
    baslik="Uçtan uca vaka: e-ticaret satış analizi",
    anlatim="""
Yöneticinin mesajı: *"Temmuz 2025 - Haziran 2026 sipariş verisini gönderiyorum. Yıllık
performansı özetleyen bir sayfa hazırlar mısın? Hangi kategori ve kanal öne çıkıyor,
mevsimsellik var mı, iadeler ne durumda?"* Görev belirsiz görünüyor ama dört soru içeriyor:
(1) toplam performans (KPI), (2) kategori/kanal kırılımı, (3) zaman örüntüsü, (4) iadeler.
Analize başlamadan önce bu soruları yaz; her tablo ve grafik bunlardan birine cevap vermeli.

Veri (`vaka_siparisler`, ~6000 satır) gerçek hayattaki sorunları taşıyor: Türkçe biçimli
CSV'den yeni okunmuş gibi `tarih` hâlâ metin (`gg.aa.yyyy`), bazı kategoriler büyük harfli
ve fazladan boşluklu (`"ELEKTRONIK "`), bazı tutarlar boş ya da negatif, ve tekrar eden
satırlar var. `musteriler` tablosu (800 satır) şehir ve kayıt tarihini taşır.

Her alt soru, Bölüm 9'daki temizliği baştan uygular: tarihi çevir, kategoriyi
`.str.strip().str.title()` ile düzelt, tekrarları at, tutarı boş/negatif olan satırları çıkar.
`net_tutar`, iade edilen siparişte 0'dır (`np.where(s["iade"], 0, s["tutar"])`) — iade
ciroya katılmaz. Son adımda (Adım 8), analizin ürünü kod değil, bir buçuk dakikada okunan
bir özet metindir: her cümlede bir sayı, tek bir öneri, sınırlamalar dürüstçe belirtilmiş.
""",
    ornek="""basla = len(s)
s["kategori"] = s["kategori"].str.strip().str.title()
s = s.drop_duplicates()
s = s[s["tutar"].notna() & (s["tutar"] > 0)]
print(basla, "->", len(s))          # -> 6030 -> 5972
s["net_tutar"] = np.where(s["iade"], 0, s["tutar"])   # iade edilen sipariş ciroya katılmaz""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="Yılın sadece 11 günü (Kasım sonu indirimi), yıllık net cironun %8,2'sini getiriyor.",
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
        soru=(
            "Temizlikten sonra (b19-s01'deki gibi) `net_tutar` sütununu ekle (iade edilen sipariş 0). "
            "`{'net_ciro':.., 'siparis':.., 'musteri':.., 'ort_sepet':.., 'medyan_sepet':.., "
            "'iade_orani':..}` sözlüğünü `result`'a yaz: ciro ve sepet tutarları en yakın tam sayıya, "
            "iade oranı 0-1 arası 3 ondalığa yuvarlanmış olsun."
        ),
        beklenen="result = {'net_ciro': 5035451, 'siparis': 5972, 'musteri': 771, 'ort_sepet': 918, 'medyan_sepet': 647, 'iade_orani': 0.09}",
        ipucu="Ortalama (918) medyandan (647) belirgin yüksek: birkaç pahalı elektronik siparişi ortalamayı çekiyor.",
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
