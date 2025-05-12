from DB.database import DB
from models.comprobante import Comprobante
from fpdf import FPDF
import os

class ComprobanteController:
    def __init__(self):
        self.db = DB().get_cursor()

    def obtener_comprobantes(self):
        comprobantes = []
        try:
            self.db.execute("SELECT * FROM comprobantes")
            for row in self.db.fetchall():
                comprobantes.append(Comprobante(id_comprobante=row[0], id_servicio=row[1], fecha_emision=row[2], monto_total=row[3], detalles=row[4]))
        except Exception as e:
            print(f"❌ Error al obtener comprobantes: {e}")
        return comprobantes

    def obtener_detalles_comprobante(self, id_comprobante):
        try:
            self.db.execute("SELECT detalles FROM comprobantes WHERE id_comprobante = %s", (id_comprobante,))
            row = self.db.fetchone()
            return row[0] if row else "No se encontraron detalles."
        except Exception as e:
            print(f"❌ Error al obtener detalles del comprobante: {e}")
            return "Error al obtener detalles."

    def generar_comprobante_pdf(self, id_comprobante):
        detalles = self.obtener_detalles_comprobante(id_comprobante)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, detalles)

        pdf_folder = "comprobantes_pdf"
        os.makedirs(pdf_folder, exist_ok=True)
        pdf.output(f"{pdf_folder}/comprobante_{id_comprobante}.pdf")

        print(f"✅ Comprobante PDF generado: {pdf_folder}/comprobante_{id_comprobante}.pdf")
