from weasyprint import HTML
from django.conf import settings
from pathlib import Path

class WeasyprintAdapter:
    def render_contract(self, *, booking_id: int, context: dict) -> str:
        html = f"<h1>Contract #{booking_id}</h1><p>{context}</p>"
        file_path = Path(settings.MEDIA_ROOT) / f"contracts/contract_{booking_id}.pdf"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        HTML(string=html).write_pdf(file_path)
        return str(file_path)
