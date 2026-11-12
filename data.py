"""Kitapçığın kendi veri setleri.

"Veri Analisti Stajyeri için Python: Sıfırdan Uygulamalı Kitapçık" kaynak alınarak,
her bölümün kullandığı örnek veri burada birebir (aynı tohum, aynı değerler) yeniden üretilir.
Böylece bir alıştırmanın beklenen sonucu, kitapçıktaki yazılı sayıyla her zaman eşleşir.

Tablolar:
- siparisler        (10 satır)  Bölüm 7-13'ün ortak e-ticaret sipariş tablosu
- musteriler_kucuk  (6 satır)  Bölüm 11'in merge örneği (C06 müşteri tablosunda yok, C07 siparişte yok)
- kirli             (6 satır)  Bölüm 9'un temizlik örneği; sütun adları bilerek dağınık
- musteriler        (800 satır) Bölüm 19 vakasının müşteri tablosu
- vaka_siparisler   (~6030 satır) Bölüm 19 vakasının sipariş tablosu; sep=';' decimal=',' ile
                     okunmuş hâldeki gibi (tarih hâlâ metin, tutarda boş/negatif var)
- gunluk_satis      (90 satır)  Bölüm 12'nin günlük satış zaman serisi
- reklam_satis      (60 satır)  Bölüm 14'ün korelasyon/regresyon örneği
- sepet_testi       (600 satır) Bölüm 14'ün iki grup t-testi örneği (A/B sepet tutarı)

Ayrıca iki Python nesnesi (tablo değil) Bölüm 17 için hazır gelir: API_ORNEGI, KUR_JSON_METNI.
"""

from __future__ import annotations

import json
import sqlite3
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

VAKA_TOHUMU = 2026
SATIS_SERISI_TOHUMU = 7
ISTATISTIK_TOHUMU = 3

VERI_KLASORU = Path(__file__).resolve().parent / "veri"


# ---------------------------------------------------------------------------
# Bölüm 7-13: ortak e-ticaret sipariş tablosu (10 satır, kitapçıkla birebir aynı)
# ---------------------------------------------------------------------------

def _siparisler() -> pd.DataFrame:
    veri = {
        "siparis_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
        "tarih": [
            "2026-01-05", "2026-01-09", "2026-01-17", "2026-02-02", "2026-02-14",
            "2026-02-20", "2026-03-03", "2026-03-11", "2026-03-15", "2026-03-28",
        ],
        "musteri_id": ["C01", "C02", "C03", "C01", "C04", "C02", "C05", "C03", "C06", "C01"],
        "sehir": [
            "İstanbul", "Ankara", "İzmir", "İstanbul", "Bursa",
            "Ankara", "İstanbul", "İzmir", "Ankara", "İstanbul",
        ],
        "kategori": [
            "Elektronik", "Giyim", "Elektronik", "Kitap", "Giyim",
            "Elektronik", "Giyim", "Kitap", "Elektronik", "Elektronik",
        ],
        "urun": ["Kulaklık", "Mont", "Klavye", "Roman", "Ayakkabı", "Mouse", "Tişört", "Ders Kitabı", "Monitör", "Şarj Aleti"],
        "adet": [2, 1, 1, 3, 1, 2, 4, 2, 1, 3],
        "birim_fiyat": [750, 2400, 1100, 180, 1900, 450, 300, 520, 6500, 350],
    }
    return pd.DataFrame(veri)


# ---------------------------------------------------------------------------
# Bölüm 11: merge örneği için küçük müşteri tablosu (C06 yok, C07 fazladan var)
# ---------------------------------------------------------------------------

def _musteriler_kucuk() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "musteri_id": ["C01", "C02", "C03", "C04", "C05", "C07"],
            "ad": ["Ayşe", "Mehmet", "Zeynep", "Can", "Elif", "Deniz"],
            "segment": ["Gold", "Silver", "Gold", "Bronze", "Silver", "Bronze"],
            "kayit_yili": [2022, 2024, 2023, 2025, 2026, 2025],
        }
    )


# ---------------------------------------------------------------------------
# Bölüm 9: veri temizleme örneği (sütun adları bilerek dağınık)
# ---------------------------------------------------------------------------

def _kirli() -> pd.DataFrame:
    return pd.DataFrame(
        {
            " Müşteri Adı ": ["  ayşe yılmaz", "MEHMET KAYA ", "Ayşe Yılmaz", None, "Can Demir", "Can Demir"],
            "Şehir": ["istanbul", "ANKARA", "İstanbul ", "izmir", "Ankara", "Ankara"],
            "Tutar": ["1.250,50", "980", "1.250,50", "abc", "2.100", "2.100"],
            "Tarih": ["05.01.2026", "2026-01-09", "05.01.2026", "17/01/2026", "02.02.2026", "02.02.2026"],
            "Puan": [4, np.nan, 4, 5, 120, 120],
        }
    )


# ---------------------------------------------------------------------------
# Bölüm 19-20: e-ticaret vakası (800 müşteri, ~6000 sipariş, bilerek kirli)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _vaka_uret(tohum: int = VAKA_TOHUMU) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(tohum)
    n_musteri, n_siparis = 800, 6000
    musteri_ids = [f"M{i:04d}" for i in range(1, n_musteri + 1)]
    musteriler = pd.DataFrame(
        {
            "musteri_id": musteri_ids,
            "sehir": rng.choice(["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"], n_musteri, p=[.40, .20, .15, .13, .12]),
            "kayit_tarihi": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 540, n_musteri), unit="D"),
        }
    )

    kategoriler = {"Elektronik": (1800, 0.9), "Giyim": (650, 0.6), "Ev": (900, 0.7), "Kitap": (220, 0.4), "Kozmetik": (380, 0.5)}
    kat = rng.choice(list(kategoriler), n_siparis, p=[.22, .28, .18, .17, .15])
    mu = np.array([kategoriler[k][0] for k in kat])
    sg = np.array([kategoriler[k][1] for k in kat])
    tutar = np.exp(np.log(mu) + rng.normal(0, 1, n_siparis) * sg * 0.6).round(2)
    agirlik = rng.pareto(1.5, n_musteri) + 1
    agirlik /= agirlik.sum()
    mus = rng.choice(musteri_ids, n_siparis, p=agirlik)
    gun = pd.date_range("2025-07-01", "2026-06-30", freq="D")
    gw = np.ones(len(gun))
    gw[gun.dayofweek >= 5] *= 1.4
    gw[(gun.month == 11) & (gun.day >= 20)] *= 3.0
    gw[gun.month == 12] *= 1.3
    gw *= np.linspace(1, 1.35, len(gun))
    gw /= gw.sum()
    siparis = pd.DataFrame(
        {
            "siparis_no": np.arange(500001, 500001 + n_siparis),
            "tarih": rng.choice(gun, n_siparis, p=gw),
            "musteri_id": mus,
            "kategori": kat,
            "kanal": rng.choice(["Web", "Mobil", "Pazaryeri"], n_siparis, p=[.35, .45, .20]),
            "tutar": tutar,
            "iade": rng.random(n_siparis) < np.where(kat == "Giyim", .18, .05),
        }
    ).sort_values("tarih").reset_index(drop=True)

    # --- kasıtlı kirlilik (kitapçıktaki sırayla) ---
    ix = rng.choice(n_siparis, 40, replace=False)
    siparis.loc[ix, "kategori"] = siparis.loc[ix, "kategori"].str.upper() + " "
    ix = rng.choice(n_siparis, 25, replace=False)
    siparis.loc[ix, "tutar"] = np.nan
    ix = rng.choice(n_siparis, 3, replace=False)
    siparis.loc[ix, "tutar"] = -siparis.loc[ix, "tutar"].abs()
    siparis = pd.concat([siparis, siparis.sample(30, random_state=1)]).sort_values("tarih").reset_index(drop=True)
    return musteriler, siparis


def _vaka_okunmus_hali(siparis: pd.DataFrame) -> pd.DataFrame:
    """`pd.read_csv(..., sep=';', decimal=',')` ile okunmuş hâliyle birebir aynı tabloyu, diske
    gitmeden üretir: tarih metin (gg.aa.yyyy) kalır, tutar zaten sayı olduğu için değişmez."""
    d = siparis.copy()
    d["tarih"] = d["tarih"].dt.strftime("%d.%m.%Y")
    return d


def _vaka_csv_yaz(musteriler: pd.DataFrame, siparis: pd.DataFrame, klasor: Path) -> dict[str, Path]:
    """Kitapçıktaki gibi Türkçe biçimli CSV yazar: noktalı virgül, virgüllü ondalık, gg.aa.yyyy tarih.

    Her çağrıda yeniden yazılır (önbelleğe alınmaz); böylece data.py değiştiğinde eski bir
    dosyadan okuma riski olmaz.
    """
    klasor.mkdir(parents=True, exist_ok=True)
    siparis_dosya = klasor / "vaka_siparisler.csv"
    musteri_dosya = klasor / "vaka_musteriler.csv"
    d = siparis.copy()
    d["tarih"] = d["tarih"].dt.strftime("%d.%m.%Y")
    d["tutar"] = d["tutar"].map(lambda x: "" if pd.isna(x) else f"{x:.2f}".replace(".", ","))
    d.to_csv(siparis_dosya, sep=";", index=False, encoding="utf-8-sig")
    musteriler.to_csv(musteri_dosya, index=False, encoding="utf-8-sig")
    return {"vaka_siparisler": siparis_dosya, "vaka_musteriler": musteri_dosya}


# ---------------------------------------------------------------------------
# Bölüm 12: günlük satış zaman serisi (90 gün)
# ---------------------------------------------------------------------------

def _gunluk_satis() -> pd.DataFrame:
    rng = np.random.default_rng(SATIS_SERISI_TOHUMU)
    gunler = pd.date_range("2026-01-01", "2026-03-31", freq="D")
    taban = np.where(gunler.dayofweek >= 5, 160, 100)
    trend = np.linspace(0, 30, len(gunler))
    satis = (taban + trend + rng.normal(0, 15, len(gunler))).round()
    return pd.DataFrame({"tarih": gunler, "satis": satis})


# ---------------------------------------------------------------------------
# Bölüm 14: korelasyon/regresyon (60 hafta) ve t-testi (2x300) örnekleri
# Kitapçıkta aynı rng nesnesi art arda kullanıldığı için buradaki sıra önemlidir.
# ---------------------------------------------------------------------------

def _istatistik_verileri() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(ISTATISTIK_TOHUMU)
    n = 60
    reklam = rng.uniform(10, 100, n).round(1)
    kampanya = rng.integers(0, 2, n)
    satis = (50 + 2.0 * reklam + 30 * kampanya + rng.normal(0, 20, n)).round(1)
    reklam_satis = pd.DataFrame({"reklam": reklam, "kampanya": kampanya, "satis": satis})

    a = rng.normal(420, 120, 300).round()
    b = rng.normal(445, 120, 300).round()
    sepet_testi = pd.DataFrame(
        {"grup": ["A"] * 300 + ["B"] * 300, "tutar": np.concatenate([a, b])}
    )
    return reklam_satis, sepet_testi


# ---------------------------------------------------------------------------
# Bölüm 17: API / JSON örnekleri (tablo değil, düz Python nesneleri)
# ---------------------------------------------------------------------------

API_ORNEGI = [
    {
        "id": 1,
        "musteri": {"ad": "Ayşe", "sehir": "İzmir"},
        "urunler": [{"ad": "Kulaklık", "fiyat": 750}, {"ad": "Kılıf", "fiyat": 120}],
    },
    {
        "id": 2,
        "musteri": {"ad": "Can", "sehir": "Bursa"},
        "urunler": [{"ad": "Mont", "fiyat": 2400}],
    },
]

KUR_JSON_METNI = json.dumps(
    {
        "tarih": "2026-11-04",
        "kurlar": [
            {"kod": "USD", "alis": 41.95, "satis": 42.10},
            {"kod": "EUR", "alis": 48.30, "satis": 48.55},
        ],
        "meta": {"sayfa": 1, "toplam_sayfa": 1},
    },
    ensure_ascii=False,
)


# ---------------------------------------------------------------------------
# Hepsini bir araya getiren önbellekli fonksiyon
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def tablolari_uret() -> dict[str, pd.DataFrame]:
    """Tüm tabloları üretir ve önbelleğe alır. Kullanıcı kodu kopya üzerinde çalışmalı."""
    musteriler, vaka_siparis_ham = _vaka_uret()
    # Bölüm 19'un "pd.read_csv(..., sep=';', decimal=',')" ile okunmuş hâline birebir eşit
    # (tarih hâlâ metin, tutar zaten sayı) bir tablo; CSV'ye gitmeden üretilir.
    vaka_siparisler = _vaka_okunmus_hali(vaka_siparis_ham)
    # Ayrı bir pd.read_csv alıştırması için gerçek CSV dosyasını da yaz.
    _vaka_csv_yaz(musteriler, vaka_siparis_ham, VERI_KLASORU)

    reklam_satis, sepet_testi = _istatistik_verileri()

    return {
        "siparisler": _siparisler(),
        "musteriler_kucuk": _musteriler_kucuk(),
        "kirli": _kirli(),
        "musteriler": musteriler,
        "vaka_siparisler": vaka_siparisler,
        "gunluk_satis": _gunluk_satis(),
        "reklam_satis": reklam_satis,
        "sepet_testi": sepet_testi,
    }


def sqlite_baglantisi_olustur(tablolar: dict[str, pd.DataFrame]):
    """Verilen tablolardan yeni bir in-memory SQLite veritabanı kurar."""
    baglanti = sqlite3.connect(":memory:")
    for ad, df in tablolar.items():
        df.copy().to_sql(ad, baglanti, index=False)
    return baglanti


def csv_dosyalari(klasor: Path | None = None) -> dict[str, Path]:
    """Tabloları CSV olarak yazar (read_csv alıştırmaları için). `_vaka_uret` önbellekli
    olduğu için bu, veriyi yeniden üretmez; sadece diske yazar."""
    hedef = Path(klasor) if klasor else VERI_KLASORU
    hedef.mkdir(parents=True, exist_ok=True)
    yollar = {}
    for ad, df in tablolari_uret().items():
        yol = hedef / f"{ad}.csv"
        df.to_csv(yol, index=False)
        yollar[ad] = yol
    musteriler, vaka_siparis_ham = _vaka_uret()
    yollar.update(_vaka_csv_yaz(musteriler, vaka_siparis_ham, hedef))
    return yollar
