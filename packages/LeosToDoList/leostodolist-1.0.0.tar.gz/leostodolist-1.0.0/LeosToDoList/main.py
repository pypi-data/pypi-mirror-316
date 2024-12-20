from .back_end import Back
from .front_end import Front
import logging
import argparse

# Logger-Konfiguration
def setup_logger(debug: bool):
    # Root-Logger konfigurieren
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[])

    # FileHandler für "all_logs.log" (alle Logs ab DEBUG)
    file_handler_all = logging.FileHandler("all_logs.log")
    file_handler_all.setLevel(logging.DEBUG)  # Speichert alle Logs (DEBUG und höher)
    formatter_all = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler_all.setFormatter(formatter_all)
    logging.getLogger().addHandler(file_handler_all)

    # FileHandler für "info_logs.log" (nur Logs ab INFO)
    file_handler_info = logging.FileHandler("info_logs.log")
    file_handler_info.setLevel(logging.INFO)  # Speichert nur Logs ab INFO
    formatter_info = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler_info.setFormatter(formatter_info)
    logging.getLogger().addHandler(file_handler_info)

    # Wenn der --debug-Parameter gesetzt ist, auch Debug-Logs an die Konsole ausgeben
    if debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Konsole gibt alle Logs (ab DEBUG) aus
        console_handler.setFormatter(formatter_all)
        logging.getLogger().addHandler(console_handler)


# Kommandozeilen-Argumente verarbeiten
def parse_args():
    parser = argparse.ArgumentParser(description="Beispiel für Logging mit verschiedenen Log-Leveln und Dateien.")
    parser.add_argument("--debug", action="store_true", help="Aktiviere Debug-Logs für Konsole und Dateien")
    return parser.parse_args()


def main():
    # Kommandozeilen-Argumente einlesen
    args = parse_args()

    # Logger konfigurieren
    setup_logger(args.debug)

    logging.info("Gui wird gestartet...")
    back = Back()
    Front(back)


if __name__ == "__main__":
    main()
