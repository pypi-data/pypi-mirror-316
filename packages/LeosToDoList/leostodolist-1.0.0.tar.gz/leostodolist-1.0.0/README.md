# To-Do-list-manager

## Installation:

Geben Sie folgenden Befehl in ihre Konsole ein:
        
        pip install LeosToDoList
    
Um das Programm zu starten geben sie in die Konsole ein:

        LeosToDoList

Nun sollte sich die GUI öffnen. 


## Beschreibung:

Der Benutzer kann eine einfache Aufgabenliste verwalten, indem er Aufgaben über ein Eingabefeld zu einer Übersicht hinzufügt, diese Aufgaben bearbeitet oder wieder löscht. 

Für jede Aufgabe kann ein Fälligkeitsdatum, eine Beschreibung sowie ein "Abgeschlossen"-Status festgelegt werden. 
Die Aufgaben mit den festgelegten Daten werden in einem JSON-file gespeichert. 

Zudem können mehrere Benutzer individuell angelegt werden, sodass jeder Benutzer auf seinen eigenen Json-File mit seiner eigenen Aufgaben-Übersicht zugreifen kann. 

## Mögliche Fehler

Bei dem Fehlercode:
      
         _tkinter.TclError: no display name and no $DISPLAY environment variable

Führen Sie in Ihrer Konsole folgenden Befehl aus:

        export DISPLAY=:0.0

Nun versuchen Sie erneut das Programm zu starten per:

        LeosToDoList

## Autor

- [@leiwa001](https://www.github.com/leiwa001)


## Voraussetzungen

- python
- pip 

