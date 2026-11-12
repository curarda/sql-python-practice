"""Bölüm 19 (uçtan uca vaka) sorularını, pandas groupby KULLANMAYAN saf Python döngüleriyle
bağımsız olarak doğrular. Amaç: referans çözümün (pandas tabanlı) yanlış bir şey
hesaplamadığından emin olmak için farklı bir kod yoluyla aynı sonuca ulaşmak.
"""

import math
import statistics
from collections import defaultdict

import pytest

import checker
import data
from curriculum import TUM_SORULAR

VAKA_IDLERI = ["b19-s01", "b19-s02", "b19-s03", "b19-s04", "b19-s05", "b19-s06"]
OZET = "Giyimde iade oranı yüksek. Kasım sonu ciroyu belirgin artırıyor. Stok ve kampanya buna göre planlanmalı."


def _bos(v) -> bool:
    return v is None or (isinstance(v, float) and math.isnan(v))


def _tr_title(metin: str) -> str:
    return metin.strip().title()


def _temiz_satirlar() -> list[dict]:
    """`vaka_siparisler`i saf Python ile temizler: kategori düzelt, tekrarları at, kötü tutarı çıkar."""
    s = data.tablolari_uret()["vaka_siparisler"]
    gorulen = set()
    satirlar = []
    for r in s.itertuples(index=False):
        kategori = _tr_title(r.kategori)
        anahtar = (r.siparis_no, r.tarih, r.musteri_id, kategori, r.kanal, r.tutar, r.iade)
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        if _bos(r.tutar) or r.tutar <= 0:
            continue
        satirlar.append(
            {
                "siparis_no": r.siparis_no,
                "tarih": r.tarih,  # gg.aa.yyyy metin
                "musteri_id": r.musteri_id,
                "kategori": kategori,
                "kanal": r.kanal,
                "tutar": r.tutar,
                "iade": bool(r.iade),
                "net_tutar": 0.0 if r.iade else r.tutar,
            }
        )
    return satirlar


def test_b19_s01_temizlik_sayisi_bagimsiz_hesapla_eslesir():
    satirlar = _temiz_satirlar()
    sonuc = checker.run_python(TUM_SORULAR["b19-s01"].cozum, "vaka_siparisler")[0]
    assert sonuc["bitti"] == len(satirlar)
    assert sonuc["basla"] - sonuc["cikan"] == sonuc["bitti"]
    assert sonuc == {"basla": 6030, "bitti": len(satirlar), "cikan": 6030 - len(satirlar)}


def test_b19_s02_kpilar_bagimsiz_hesapla_eslesir():
    satirlar = _temiz_satirlar()
    net_ciro = sum(r["net_tutar"] for r in satirlar)
    musteriler = {r["musteri_id"] for r in satirlar}
    tutarlar = [r["tutar"] for r in satirlar]
    iade_orani = sum(r["iade"] for r in satirlar) / len(satirlar)

    sonuc = checker.run_python(TUM_SORULAR["b19-s02"].cozum, "vaka_siparisler")[0]
    assert sonuc["net_ciro"] == round(net_ciro)
    assert sonuc["siparis"] == len(satirlar)
    assert sonuc["musteri"] == len(musteriler)
    assert sonuc["ort_sepet"] == round(statistics.mean(tutarlar))
    assert sonuc["medyan_sepet"] == round(statistics.median(tutarlar))
    assert sonuc["iade_orani"] == pytest.approx(round(iade_orani, 3), abs=0.001)


def test_b19_s03_kategori_ozeti_bagimsiz_hesapla_eslesir():
    satirlar = _temiz_satirlar()
    gruplar: dict[str, list[dict]] = defaultdict(list)
    for r in satirlar:
        gruplar[r["kategori"]].append(r)
    beklenen = {}
    for kategori, grup in gruplar.items():
        beklenen[kategori] = {
            "siparis": len(grup),
            "brut": round(sum(r["tutar"] for r in grup), 1),
            "net": round(sum(r["net_tutar"] for r in grup), 1),
        }

    sonuc = checker.run_python(TUM_SORULAR["b19-s03"].cozum, "vaka_siparisler")[0]
    assert set(sonuc["kategori"]) == set(beklenen)
    for _, satir in sonuc.iterrows():
        k = satir["kategori"]
        assert int(satir["siparis"]) == beklenen[k]["siparis"], k
        assert satir["brut"] == pytest.approx(beklenen[k]["brut"], abs=0.5), k
        assert satir["net"] == pytest.approx(beklenen[k]["net"], abs=0.5), k
    # net'e göre azalan sıralı olmalı
    assert list(sonuc["net"]) == sorted(sonuc["net"], reverse=True)


def test_b19_s04_kasim_sonu_payi_bagimsiz_hesapla_eslesir():
    from datetime import date

    satirlar = _temiz_satirlar()
    toplam = sum(r["net_tutar"] for r in satirlar)
    kasim_sonu = 0.0
    for r in satirlar:
        gun, ay, yil = (int(x) for x in r["tarih"].split("."))
        d = date(yil, ay, gun)
        if date(2025, 11, 20) <= d <= date(2025, 11, 30):
            kasim_sonu += r["net_tutar"]
    beklenen = round(kasim_sonu / toplam, 3)

    sonuc = checker.run_python(TUM_SORULAR["b19-s04"].cozum, "vaka_siparisler")[0]
    assert sonuc == pytest.approx(beklenen, abs=0.001)
    assert sonuc == pytest.approx(0.082, abs=0.001)


def test_b19_s05_musteri_yogunlasmasi_bagimsiz_hesapla_eslesir():
    satirlar = _temiz_satirlar()
    musteri_ciro: dict[str, float] = defaultdict(float)
    for r in satirlar:
        musteri_ciro[r["musteri_id"]] += r["net_tutar"]
    sirali = sorted(musteri_ciro.values(), reverse=True)
    n_ustte = int(len(sirali) * 0.1)
    beklenen = round(sum(sirali[:n_ustte]) / sum(sirali), 3)

    sonuc = checker.run_python(TUM_SORULAR["b19-s05"].cozum, "vaka_siparisler")[0]
    assert sonuc == pytest.approx(beklenen, abs=0.001)
    assert sonuc == pytest.approx(0.577, abs=0.001)


def test_vaka_sorulari_tanimli_ve_rubrikli():
    for sid in VAKA_IDLERI:
        soru = TUM_SORULAR[sid]
        assert soru.kirlilik.strip(), sid
    son = TUM_SORULAR["b19-s06"]
    assert son.ozet_gerekli
    assert son.rubrik.count("\n") >= 2


@pytest.mark.parametrize("sid", VAKA_IDLERI)
def test_vaka_referans_cozumu_ozetle_birlikte_kabul_edilir(sid):
    soru = TUM_SORULAR[sid]
    sonuc = checker.check(soru, soru.cozum, OZET)
    assert sonuc.dogru, f"{sid}: {sonuc.mesaj} {sonuc.detay}"


def test_vaka_ozet_eksikse_kabul_edilmez():
    soru = TUM_SORULAR["b19-s06"]
    sonuc = checker.check(soru, soru.cozum, "Kısa özet.")
    assert sonuc.kategori == "ozet_eksik"
