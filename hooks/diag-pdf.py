"""Diagnostic temporaire : affiche les messages de WeasyPrint dans le journal CI."""
import logging
class Montre(logging.Handler):
    vus = set()
    def emit(self, record):
        m = record.getMessage()[:160]
        if m not in Montre.vus:
            Montre.vus.add(m)
            print("[WEASY]", m, flush=True)
def on_config(config, **kwargs):
    lg = logging.getLogger("weasyprint")
    lg.addHandler(Montre()); lg.setLevel(logging.DEBUG)
    return config
