"""Bölüm 1: Kurulum ve çalışma ortamı."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=1,
    baslik="Kurulum ve çalışma ortamı",
    anlatim=(
        "Bu bölümde Python'u çalıştırmak için gereken üç şeyi (dil, kütüphaneler, editör), "
        "`pip` ile kütüphane kurmayı ve sanal ortamı öğreneceksin. Her nokta kendi kısa "
        "anlatımı ve örneğiyle geliyor; okuyup örneği gördükten sonra aynı kalıbı kendin yaz."
    ),
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
        kavram="Ortamlar ve pip ile kütüphane kurmak",
        anlatim="""
Python'u kullanmak için üç şey gerekir: **dilin kendisi** (yorumlayıcı, kodunu satır satır
çalıştıran program), **kütüphaneler** (pandas gibi başkalarının yazdığı hazır araç
kutuları) ve bir **editör**. En pratik yol: Anaconda'yı kurmak (Python'u, Jupyter'i,
pandas/NumPy/matplotlib'i birlikte getirir) ya da hiç kurulum yapmadan **Google Colab**
kullanmak.

Üç ortam, üç farklı iş için:

- **Jupyter Notebook/Lab**: kodu hücrelere bölüp ayrı ayrı çalıştırdığın, çıktının hemen
  altında göründüğü arayüz. Keşifsel analiz (veriye ilk bakış, deneme yanılma) için ana
  çalışma masası.
- **VS Code**: tekrar tekrar çalışacak `.py` betikleri, otomatik raporlar, Git ile çalışmak
  için.
- **Terminal**: kütüphane kurmak ve betikleri çalıştırmak için.

`pip`, Python'un paket yöneticisidir (package manager): internetteki resmî depodan (PyPI)
kütüphane indirip kurar. Bir kodu çalıştırdığında `ModuleNotFoundError: No module named
'openpyxl'` gibi bir hata alırsan, o kütüphane kurulu değildir demektir; terminalde
`pip install <kütüphane adı>` ile kurarsın.
""",
        ornek="""import pandas as pd
import numpy as np
print(pd.__version__, np.__version__)
# -> 3.0.5 2.5.3   (senin sürüm numaraların farklı olabilir; hata almıyorsan kurulum tamam)""",
        ornek_dili="python",
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
        anlatim="""
`pip install ...` yalnızca **terminalde** çalışır. Jupyter bir hücre içinde çalıştığı için,
aynı işlemi bir hücreden yapmak istediğinde komutun başına `%` işareti koyman gerekir —
buna "magic command" (sihirli komut) denir ve Jupyter'e "bunu kabuk komutu gibi çalıştır"
der. `%` olmadan yazarsan Python bunu normal bir kod satırı sanıp sözdizimi hatası verir.
""",
        ornek="""%pip install requests
# Terminalde aynı işlem: pip install requests (başında % yok)""",
        ornek_dili="text",
        soru="Aynı kurulumu terminalde değil bir **Jupyter hücresinde** yapmak için yazılması gereken komutu `result`'a yaz. Başındaki işareti unutma.",
        beklenen='result = "%pip install openpyxl"',
        ipucu="Jupyter'de terminal komutlarının başına % konur.",
        cozum='result = "%pip install openpyxl"',
    ),
    Soru(
        id="b1-s03",
        gun=1,
        tur="python",
        kavram="Sanal ortam (virtual environment)",
        anlatim="""
**Sanal ortam**, bir projeye ait kütüphanelerin ve sürümlerinin diğer projelerden
yalıtıldığı ayrı bir klasördür. Bir projede pandas 1.5, diğerinde pandas 2.2 lazımsa,
ikisini aynı bilgisayarda çakıştırmadan tutmanı sağlar. Stajın ilk günlerinde takımın sana
bir `requirements.txt` dosyası (projenin ihtiyaç duyduğu kütüphanelerin listesi) vermesi
olasıdır; sanal ortamı oluşturup bu listeyi içine kurarsın. Oluşturma ve kurma adımları
işletim sisteminden bağımsızdır; yalnızca **etkinleştirme** komutu farklıdır.
""",
        ornek="""python -m venv .venv                  # .venv adında sanal ortam oluştur
pip install -r requirements.txt       # (etkinleştirdikten sonra) listedeki her şeyi kur""",
        ornek_dili="text",
        soru="macOS/Linux'ta `.venv` adlı bir sanal ortamı etkinleştiren komutu `result`'a yaz.",
        beklenen='result = "source .venv/bin/activate"',
        ipucu="Önce python -m venv .venv ile oluşturulur, sonra bu komutla etkinleştirilir.",
        cozum='result = "source .venv/bin/activate"',
    ),
]
