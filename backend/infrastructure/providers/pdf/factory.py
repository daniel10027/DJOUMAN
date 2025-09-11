from django.conf import settings
import sys

def get_pdf_port():
    """
    Retourne l’adapter PDF en évitant d’importer weasyprint si non utilisé.
    - Par défaut Windows => reportlab (zéro dépendances natives)
    - Sinon backend configurable via PDF_BACKEND = "weasyprint" | "reportlab"
    """
    default_backend = "reportlab" if sys.platform.startswith("win") else "weasyprint"
    backend = getattr(settings, "PDF_BACKEND", default_backend).lower()

    if backend == "weasyprint":
        # Import seulement si on choisit weasyprint
        from infrastructure.providers.pdf.weasyprint_adapter import WeasyprintAdapter
        return WeasyprintAdapter()
    else:
        from infrastructure.providers.pdf.reportlab_adapter import ReportlabAdapter
        return ReportlabAdapter()
