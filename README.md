# Moodle Sync Aggregate
ist ein Programm zur Notenberechnung. Es verbindet sich zu einem Moodle Server und lädt alle Bewertungen aller
Schülerinnen und Schüler herunter um sie dann in ein Excel zu exportieren. Zur Verwendung wird ein Moodle Authorization
Token benötigt. 

## Funktionalität

- Automatisierter Download aller SchülerInnen Bewertungen in einem Kurs
- Gruppen werden exportiert
- Automatisiertes Matching der SchülerInnen Namen zur Jahrgangszuordnung (Schülerliste mit Klassen wird benötigt)
- Auswahl der zu speichernden Bewertungen über die Grafische Benutzeroberfläche
- Verkürzung der Kompetenzorientierten Bewertungen (GKü, GKv, ...)
- Export der Bewertungen als leicht zu bearbeitendes Excel

## Vorraussetzungen

- Moodle Server URL
- Moodle Authorization Key
- Studentlist.csv *optional
- (Certifi Zertifikat) only for run from source

### Python Dependencies

- Python 3.10
- PyQt5 5.15.6
- certifi 2021.10.8
- openpyxl 3.0.9
- requests 2.26.0
- pandas 1.3.5

## TODOs

- Create Negative Competences Column (ie. 1.1;1.3)
- Berechnung und Streichungen von WH/Wiederholung/SMÜ
- Download multiple and export into one file
- Download Progress Bar (multiprozessing?)
- Download and Merge Grundkompetenzüberprüfungen
- Create Grundkompetenzüberprüfungen list
- Using LDAP for studentlist
- Login to Moodle using Username and Password
- Kompetenzzähler?
- andere Berechnungen?
- ~~Schwellwerte für bedingte Formatierung in Excel~~
- ~~Sort Gruppe/Klasse before Name~~
- ~~Bedingte Formatierung Gruppe != Klasse~~
- ~~Error Messages~~
- ~~no classes without studentlist~~
- ~~include email adress~~
- ~~Studentlist standartpath to sharpoint~~
- ~~Get Students Jahrgang from moodle Group~~
- ~~Add ALLE/KEINE Checkbox~~
- ~~Startup Config (Splitter, elearning-URL, elearning-Key, export filepath, ...)~~
- ~~Filename generation (timestamp-kursname-klassen.xlsx)~~
- ~~Format exported excel~~
- ~~Auto Numbers detection and format as number in excel~~
- ~~Auto GK/EK detection~~
- ~~bedingte formatierung für EKv/EKü~~
- ~~bedingte formatierung rot für GK wenn -/n~~
- ~~bedingte formatierung für v/ü wenn EK~~
- ~~bedingte formatierung für Wiederholung~~
- ~~zusammenfassen der Kompetenzbereiche abhängig von Modulnummer~~
- ~~Kompetenzbereiche Formular instead of python calculated~~
- ~~Notenberechnung aus Notenschlüssel~~
- ~~Bedingte Formatierung für Notenvorschlag~~
- ~~Bedingte Formatierung für Kompetenzbereiche~~

Credit Moodle API by [mrcinv](https://github.com/mrcinv/moodle_api.py)

