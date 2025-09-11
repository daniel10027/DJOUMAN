from reportlab.pdfgen import canvas
from django.conf import settings
from pathlib import Path

class ReportlabAdapter:
    def render_contract(self, *, booking_id: int, context: dict) -> str:
        file_path = Path(settings.MEDIA_ROOT) / f"contracts/contract_{booking_id}.pdf"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(file_path))
        c.drawString(100, 800, f"Contract #{booking_id}")
        c.drawString(100, 780, str(context))
        c.save()
        return str(file_path)
