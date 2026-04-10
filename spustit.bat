@echo off
chcp 65001 > nul
REM ==== Spouštěč QR generování + PDF ====

REM Vyčištění starých výstupů
echo Mazu staré QR soubory...
if exist qr_out (
    rmdir /s /q qr_out
)
if exist qr_codes.pdf (
    del /q qr_codes.pdf
)
if exist qr_out\qr_codes.zip (
    del /q qr_out\qr_codes.zip
)

REM Generování QR kódů
echo =====================================
echo 1) Generuji QR kódy z urls.txt...
echo =====================================
python bulk_qr.py --input urls.txt --format png --ec H --scale 12 --out qr_out --zip
if %errorlevel% neq 0 (
    echo CHYBA při generování QR kódů!
    pause
    exit /b
)

REM Vytvoření PDF
echo =====================================
echo 2) Tvořím PDF s QR kódy...
echo =====================================
python qr2pdf.py
if %errorlevel% neq 0 (
    echo CHYBA při generování PDF!
    pause
    exit /b
)

echo =====================================
echo HOTOVO! Otevři qr_codes.pdf a tiskni.
echo =====================================
pause
