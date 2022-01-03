# Moodle Sync Aggregate
ist ein Programm zur Notenberechnung. Es verbindet sich zu einem Moodle Server und lädt alle Bewertungen aller
Schülerinnen und Schüler herunter um sie dann in ein Excel zu exportieren. Zur Verwendung wird ein Moodle Authorization
Token benötigt. 

## Funktionalität

- Automatisierter Download aller SchülerInnen Bewertungen in einem Kurs
- Automatisiertes Matching der SchülerInnen Namen zur Jahrgangszuordnung (Schülerliste mit Klassen wird benötigt)
- Auswahl der zu speichernden Bewertungen über die Grafische Benutzeroberfläche
- Verkürzung der Kompetenzorientierten Bewertungen (GKü, GKv, ...)
- Export der Bewertungen als leicht zu bearbeitendes Excel

## TODOs

- Get Students Jahrgang from moodle Group
- Add Scrollbar to Modules List
- ~~Add ALLE/KEINE Checkbox~~
- Startup Config (~~Splitter, elearning-URL, elearning-Key,~~ export filepath, ...)
- ~~Filename generation (timestamp-kursname-klassen.xlsx)~~
- Format exported excel
- Add Dialog for Students without Class

Credit Moodle API by [mrcinv](https://github.com/mrcinv/moodle_api.py)

