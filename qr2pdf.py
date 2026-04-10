from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import os

# složka s PNG QR kódy
qr_folder = "qr_out"
output_pdf = "qr_codes.pdf"

c = canvas.Canvas(output_pdf, pagesize=A4)
page_width, page_height = A4

# velikost jednoho QR v cm
qr_size = 3 * cm
cols = int(page_width // qr_size)
rows = int(page_height // qr_size)

# pevný okraj 2 cm od kraje
x_margin = 2 * cm
y_margin = 2 * cm


x = x_margin
y = page_height - qr_size - y_margin

for i, filename in enumerate(sorted(os.listdir(qr_folder))):
    if not filename.lower().endswith(".png"):
        continue
    path = os.path.join(qr_folder, filename)
    c.drawImage(path, x, y, qr_size, qr_size)

    x += qr_size
    if x + qr_size > page_width:
        x = x_margin
        y -= qr_size
        if y < 0:
            c.showPage()
            y = page_height - qr_size - y_margin

c.save()
print("Hotovo ->", output_pdf)
