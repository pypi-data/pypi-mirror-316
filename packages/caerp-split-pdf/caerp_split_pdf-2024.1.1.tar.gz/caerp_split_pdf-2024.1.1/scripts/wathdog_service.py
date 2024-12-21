import time
import configparser
import sys
from endi_split_pdf.service import (
    SplitPdfFileHandler,
    AccountingFileHandler,
)
from watchdog.observers import Observer


def _load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    for section in config.sections():
        print(f"Section {section}")
        yield config[section]["user"], config[section]["directory"], config[section][
            "handler"
        ], config[section]["pattern"].split(",")


def _build_observers(config_path):
    # Création de l'observeur
    observers = []
    for user, directory, handler_name, patterns in _load_config(config_path):
        if handler_name == "split_pdf":
            handler = SplitPdfFileHandler(user, directory, patterns=patterns)
        elif handler_name == "accounting_files":
            handler = AccountingFileHandler(user, directory, patterns=patterns)

        observer = Observer()
        # Création du lien
        observer.schedule(handler, path=directory, recursive=False)
        observers.append(observer)
    return observers


def run(config_path):
    observers = _build_observers(config_path)
    if observers:
        try:
            for observer in observers:
                # Démarrage de l'observateur
                observer.start()

            while True:  # Boucle infinie bloquant l'execution du script
                time.sleep(1)  # petite attente d'une milliseconde
        except KeyboardInterrupt:  # Prise en charge de l'interuption par le clavier
            for observer in observers:
                observer.stop()  # Arret de l'observateur
        for observer in observers:
            observer.join()


if __name__ == "__main__":
    config_path = sys.argv[1]
    run(config_path)
