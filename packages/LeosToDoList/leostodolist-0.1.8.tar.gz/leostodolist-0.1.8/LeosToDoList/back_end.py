import json
import tkinter as tk
from pathlib import Path
from time import strftime
import logging



class Back:
    def __init__(self):
        self.dict_list = []  # Liste der einzelnen task dictionaries

        self.dictionary = {  # Standard task dictionary
            "task": "Aufgabe1",
            "completed": False,
            "beschreibung": "Beschreibung:\n\n",
            "faelligkeit": "-nicht festgelegt-",
            "erstellung": "",
        }

        self.user_list = ["user1"]  # Liste der erstellten User
        self.get_user_list()

    # Liste der User laden bzw. erst erstellen wenn nötig
    def get_user_list(self):
        path = Path("user_list.json")
        if path.exists():
            task_list = path.read_text()
            self.user_list = json.loads(task_list)
        else:
            task_list = json.dumps(self.user_list)
            path.write_text(task_list)

        task_list = path.read_text()
        self.user_list = json.loads(task_list)

        logging.debug("User-Liste abgerufen")

    # Neuen User erstellen
    def new_user_back(self, username):
        logging.info(f"Neuer User: {username}")
        self.user_list.append(username)
        path = Path("user_list.json")
        task_list = json.dumps(self.user_list)
        path.write_text(task_list)
        logging.debug(f"Neue user_liste: {self.user_list}")

    def get_user(self):
        return self.user_list

    # neue task erstellen
    def add_task(self, task):
        logging.debug(f"'{task}' soll hinzugefügt werden.")

        if task == "":
            logging.info("Geben Sie erst eine Aufgabe ein")

        else:
            self.dictionary["task"] = task
            time = strftime("%d.%m.%Y")
            self.dictionary["erstellung"] = time
            new_dict = self.dictionary.copy()
            self.dict_list.append(new_dict)

            logging.debug(self.dict_list)

    # Funktion für Speichern in Json File
    def save_task(self, user):
        path_name = f"mylist_{user}.json"
        path = Path(path_name)

        self.task_list = json.dumps(self.dict_list, indent=4)
        path.write_text(self.task_list)
        logging.debug("task_list wurde gespeichert")

    # Funktion für Laden aus Json File
    def load_task(self, aufgabenliste, user):
        path_name = f"mylist_{user}.json"
        path = Path(path_name)

        if path.exists():
            self.task_list = path.read_text()
            self.dict_list = json.loads(self.task_list)
            for wert in self.dict_list:
                task = wert["task"]
                aufgabenliste.insert(tk.END, task)
        else:
            logging.info("Keine Aufgaben gespeichert")

    # Funktion für Lösch Button
    def delete_task(self, aufgabenliste):
        self.sel_task = aufgabenliste.curselection()
        aufgabenliste.delete(self.sel_task)

        for i in range(100):
            if self.sel_task == (i,):
                del self.dict_list[i]
        logging.debug(f"{self.sel_task} gelöscht.")

    # Werte für Bearbeitungsfenster übergeben
    def get_values(self, sel_task):
        for i in range(100):
            if sel_task == (i,):
                sel_dict = self.dict_list[i]
                task = sel_dict["task"]
                beschreibung = sel_dict["beschreibung"]
        return task, beschreibung, sel_dict

    # speichert Bearbeitung im new_window
    def bearbeitung_speichern(self, eingabe, sel_dict, user):
        sel_dict["beschreibung"] = eingabe

        path_name = f"mylist_{user}.json"
        path = Path(path_name)

        task_list = json.dumps(self.dict_list, indent=4)
        path.write_text(task_list)
        logging.info("Bearbeitung wurde gespeichert")

    # Faelligkeitsdatum abrufen
    def get_datum(self, sel_dict, date):
        sel_dict["faelligkeit"] = date

    # completed-Status abrufen
    def get_check_status(self, sel_dict):
        return "  Abgeschlossen!" if sel_dict["completed"] else "  Noch nicht abgeschlossen"

    # Wert der Checkbox-Variable abrufen
    def checkbox(self, sel_dict, variable):
        if variable == 1:
            sel_dict["completed"] = True
        else:
            sel_dict["completed"] = False

    # mit Doppelklick bearbeiteter Name auch in dictionary speichern
    def accept_edit(self, dict_index, name):
        sel_dict = self.dict_list[dict_index]
        sel_dict["task"] = name

    # entfernt User, falls user_liste leer wäre, wird 'user1' in Liste geschrieben
    def del_user(self, user):
        self.user_list.remove(user)

        path = Path("user_list.json")

        if self.user_list == []:
            self.user_list.append("user1")
            task_list = json.dumps(self.user_list)
            path.write_text(task_list)

        else:
            task_list = json.dumps(self.user_list)
            path.write_text(task_list)

        logging.debug(self.user_list)


