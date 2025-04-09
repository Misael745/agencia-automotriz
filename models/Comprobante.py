from datetime import datetime

class Comprobante:
    def __init__(self, id_comprobante=None, id_servicio=None, fecha_emision=None, monto_total=0.0, detalles=None):
        self.id_comprobante = id_comprobante
        self.id_servicio = id_servicio
        self.fecha_emision = fecha_emision or datetime.now()
        self.monto_total = monto_total
        self.detalles = detalles or "Sin detalles adicionales"

    def __str__(self):
        return f"📄 Comprobante #{self.id_comprobante} | Total: ${self.monto_total:.2f}"

    def generar_comprobante(self, servicio, refacciones):
        """Genera el texto estructurado del comprobante"""
        self.detalles = (
            f"--- COMPROBANTE DE SERVICIO ---\n"
            f"Fecha: {self.fecha_emision.strftime('%d/%m/%Y %H:%M')}\n"
            f"Servicio ID: {servicio.id_servicio}\n"
            f"Vehículo ID: {servicio.id_vehiculo}\n"
            f"Estado: {servicio.estatus}\n"
            f"Refacciones:\n"
        )
        
        for ref in refacciones:
            self.detalles += f"- {ref.nombre} (${ref.precio_unitario:.2f} x {ref.cantidad})\n"
        
        self.detalles += f"\nTOTAL: ${self.monto_total:.2f}"
        return self.detalles