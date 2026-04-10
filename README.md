EN:

INSTRUCTIONS: GENERATING AND PRINTING QR CODES FROM A URL LIST

WHAT'S INCLUDED:

    bulk_qr.py  ........ script for generating QR codes from urls.txt

    qr2pdf.py   ......... script for laying out QR codes into a PDF (A4, 3x3 cm or larger)

    urls.txt    .......... text file containing links (each link on a new line or comma-separated)

PREREQUISITES (one-time setup):

    Have Python installed: https://www.python.org/downloads/

    Open Command Prompt (CMD/PowerShell) and install the required libraries:
    pip install segno reportlab

HOW TO GENERATE QR CODES:

    Open urls.txt and insert/update your list of links (comma-separated or one per line).

    In the Command Prompt, navigate to the folder containing the scripts, for example:
    cd %USERPROFILE%\Desktop\QR

    Run the QR code generation (image size can be increased using the --scale parameter, e.g., 12):
    python bulk_qr.py --input urls.txt --format png --ec H --scale 12 --out qr_out --zip

        This creates a qr_out folder with PNG QR codes and a qr_codes.zip archive.

HOW TO CREATE A PDF FOR PRINTING (A4):

    Adjust the QR code size by changing this line in qr2pdf.py:
    qr_size = 3 * cm
    -> change 3 to 4 or 5 for larger codes.

    Run the script:
    python qr2pdf.py

    A qr_codes.pdf file ready for printing will be generated.
    Set your printer scale to 100% to ensure correct sizing.

TIPS:

    You can change parameters (--scale, --border) in bulk_qr.py to adjust the QR codes' appearance.

    The PNG files can also be used elsewhere (web, posters, etc.).

    All steps work offline; no data is sent anywhere.


-----------------------------------------------------------------------------------------------------------

CZ:

NÁVOD: GENEROVÁNÍ A TISK QR KÓDŮ Z URL SEZNAMU
=============================================

CO JE PŘIPRAVENO:
- bulk_qr.py  ........ skript pro generování QR kódů z urls.txt
- qr2pdf.py  ......... skript pro vysázení QR kódů do PDF (A4, 3x3 cm nebo víc)
- urls.txt  .......... textový soubor s odkazy (každý odkaz na nový řádek nebo čárkami)

PŘEDPOKLADY (jednorázová instalace):
-----------------------------------
1. Mít nainstalovaný Python: https://www.python.org/downloads/
2. Otevřít příkazový řádek (CMD/PowerShell) a nainstalovat knihovny:
   pip install segno reportlab

JAK GENEROVAT QR KÓDY:
----------------------
1. Otevři urls.txt a vlož/aktualizuj seznam odkazů (oddělené čárkou nebo každý na nový řádek).
2. V příkazovém řádku přejdi do složky se skripty, například:
   cd %USERPROFILE%\Desktop\QR
3. Spusť generování QR kódů (velikost obrázků lze zvětšit parametrem --scale, např. 12):
   python bulk_qr.py --input urls.txt --format png --ec H --scale 12 --out qr_out --zip

   - Vytvoří složku qr_out s PNG QR kódy a archiv qr_codes.zip.

JAK VYTVOŘIT PDF PRO TISK (A4):
-------------------------------
1. Uprav si velikost QR kódů změnou řádku v qr2pdf.py:
     qr_size = 3 * cm
   -> změň 3 na 4 nebo 5 pro větší kódy.

2. Spusť skript:
   python qr2pdf.py

3. Vznikne soubor qr_codes.pdf připravený pro tisk.
   V tiskárně nastav měřítko 100 %, aby seděla velikost.

TIPY:
-----
- V souboru bulk_qr.py můžeš měnit parametry (--scale, --border) pro vzhled QR kódů.
- Soubory PNG můžeš použít i jinde (web, plakáty, atd.).
- Všechny kroky fungují offline, data se nikam neposílají.
