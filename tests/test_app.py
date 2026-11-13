"""Arayüz duman testi: uygulama hatasız açılıyor, cevap kontrol edilip kaydediliyor."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import progress

UYGULAMA = Path(__file__).resolve().parent.parent / "app.py"


@pytest.fixture
def gecici_ilerleme(tmp_path, monkeypatch):
    dosya = tmp_path / "progress.json"
    monkeypatch.setattr(progress, "DOSYA", dosya)
    return dosya


def _parkura_git(at, parkur_etiketi, bolum_indeksi):
    at.radio(key="parkur").set_value(parkur_etiketi).run()
    bolum_anahtari = "bolum_python" if "Python" in parkur_etiketi else "bolum_sql"
    etiket = at.radio(key=bolum_anahtari).options[bolum_indeksi]
    at.radio(key=bolum_anahtari).set_value(etiket).run()
    return at


def test_uygulama_hatasiz_aciliyor(gecici_ilerleme):
    at = AppTest.from_file(str(UYGULAMA), default_timeout=60).run()
    assert not at.exception
    # Varsayılan parkur Python'dur; ikinci radio o parkurun bölüm listesidir.
    assert any("Bölüm 1" in etiket for etiket in at.radio(key="bolum_python").options)
    assert any("🗄️ SQL" in etiket for etiket in at.radio(key="parkur").options)


def test_sql_parkuruna_gecilebilir(gecici_ilerleme):
    at = AppTest.from_file(str(UYGULAMA), default_timeout=60).run()
    at.radio(key="parkur").set_value("🗄️ SQL").run()
    assert not at.exception
    assert any("SQL temelleri" in etiket for etiket in at.radio(key="bolum_sql").options)


def test_yanlis_cevap_kontrol_edilir_ve_kaydedilir(gecici_ilerleme):
    at = AppTest.from_file(str(UYGULAMA), default_timeout=60).run()
    _parkura_git(at, "🗄️ SQL", 2)  # SQL parkurunda 3. bölüm: Bölüm 15 (SQL ve Python)
    at.text_area(key="kod_b15-s01").input("SELECT sehir FROM siparisler").run()
    at.button(key="gun15_kontrol").click().run()

    assert not at.exception
    assert any("farklı" in e.value for e in at.error)
    kayit = progress.yukle(gecici_ilerleme)
    assert kayit["sorular"]["b15-s01"]["yanlis"] == 1


def test_sozdizimi_hatasi_cokme_yaratmaz(gecici_ilerleme):
    at = AppTest.from_file(str(UYGULAMA), default_timeout=60).run()
    _parkura_git(at, "🗄️ SQL", 2)  # Bölüm 15: SQL ve Python
    at.text_area(key="kod_b15-s01").input("SELEC * FRM siparisler").run()
    at.button(key="gun15_calistir").click().run()

    assert not at.exception
    assert any("Sözdizimi" in e.value for e in at.error)


def test_dogru_cevap_kaydedilir(gecici_ilerleme):
    from curriculum import TUM_SORULAR

    at = AppTest.from_file(str(UYGULAMA), default_timeout=60).run()
    # Varsayılan parkur Python, varsayılan bölüm Bölüm 1.
    at.radio(key="gun1_soru").set_value(1).run()
    at.text_area(key="kod_b1-s02").input(TUM_SORULAR["b1-s02"].cozum).run()
    at.button(key="gun1_kontrol").click().run()

    assert not at.exception
    assert any("Doğru" in s.value for s in at.success)
    assert progress.yukle(gecici_ilerleme)["sorular"]["b1-s02"]["cozuldu"] is True
