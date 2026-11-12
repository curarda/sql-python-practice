"""Bölüm 1: Kurulum ve çalışma ortamı."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=1,
    baslik="Kurulum ve çalışma ortamı",
    anlatim="""
Python'u kullanmak için üç şey gerekir: **dilin kendisi** (yorumlayıcı), **kütüphaneler**
(pandas gibi hazır araç kutuları) ve bir **editör**. En pratik yol: Anaconda'yı kurmak ya da
hiç kurulum yapmadan **Google Colab** kullanmak.

- **Jupyter Notebook/Lab**: kodu hücrelere bölüp ayrı çalıştırdığın, çıktının hemen altında
  göründüğü arayüz. Keşifsel analiz (EDA) için ana çalışma masası.
- **VS Code**: tekrar tekrar çalışacak `.py` betikleri, otomatik raporlar, Git için.
- **Terminal**: kütüphane kurmak ve betik çalıştırmak için.

`pip`, Python'un paket yöneticisidir: `ModuleNotFoundError: No module named 'openpyxl'`
görürsen o kütüphane kurulu değildir. Terminalde `pip install openpyxl`, Jupyter
hücresinde başına `%` koyarak `%pip install openpyxl` yazılır.

**Sanal ortam** (virtual environment), bir projenin kütüphanelerini diğerlerinden
yalıtan ayrı bir klasördür; takımın `requirements.txt` dosyasını `pip install -r
requirements.txt` ile kurarsın.
""",
    ornek="""import pandas as pd
import numpy as np
print(pd.__version__, np.__version__)
# -> 3.0.5 2.5.3   (senin sürüm numaraların farklı olabilir)""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Kısa kural",
            aciklama="Soruyu keşfederken notebook, cevabı her hafta yeniden üreteceksen script.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b1-s01",
        gun=1,
        tur="python",
        kavram="pip ile kütüphane kurmak",
        soru="Terminalde `openpyxl` kütüphanesini kurmak için yazılması gereken komutu `result` değişkenine tam olarak (metin olarak) yaz.",
        beklenen="result = \"pip install openpyxl\"",
        ipucu="pip install <kütüphane adı> kalıbını kullan.",
        cozum='result = "pip install openpyxl"',
    ),
    Soru(
        id="b1-s02",
        gun=1,
        tur="python",
        kavram="Jupyter hücresinde kurulum",
        soru="Aynı kurulumu terminalde değil bir **Jupyter hücresinde** yapmak için yazılması gereken komutu `result`'a yaz. Başındaki işareti unutma.",
        beklenen='result = "%pip install openpyxl"',
        ipucu="Jupyter'de terminal komutlarının başına % konur.",
        cozum='result = "%pip install openpyxl"',
    ),
    Soru(
        id="b1-s03",
        gun=1,
        tur="python",
        kavram="Sanal ortam etkinleştirme",
        soru="macOS/Linux'ta `.venv` adlı bir sanal ortamı etkinleştiren komutu `result`'a yaz.",
        beklenen='result = "source .venv/bin/activate"',
        ipucu="Önce python -m venv .venv ile oluşturulur, sonra bu komutla etkinleştirilir.",
        cozum='result = "source .venv/bin/activate"',
    ),
]
