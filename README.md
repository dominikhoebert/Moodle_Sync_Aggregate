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
- python-ldap 3.4.0

## Run from Source
1. pip install -r requirements.txt
2. Copy content of additional_cert.pem into venv(or other python environment folter)/lib/python3.10/site-packages/certifi/cacert.pem

Credit Moodle API by [mrcinv](https://github.com/mrcinv/moodle_api.py)

## TODOs

- ~~Download aggregated grade report~~
- rework export function object oriented, more stable
- improve import functionality
- bestehungsgrenze aus modul
- statistics? anzahl an noten, kompetenzen, schüler, ...
- graphes for statistics?
- andere Berechnungen?
- export as json
- ~~Only starts in debug mode?~~
- ~~statusbar~~
- ~~import excel for merging~~
- ~~Download Progress Bar (multiprocessing?, asyncio?)~~
- ~~BUG: self.current_course switches when changing course without downloading it!~~
- ~~Catch Error LDAP not working when not in school~~
- ~~override page instead of error message~~
- ~~add configparser~~
- ~~rework gui~~
- ~~adding negative kompetenzen for GKüberprüfung/merged~~
- ~~remove warnings~~
- ~~Download and Merge Grundkompetenzüberprüfungen~~
- ~~Download multiple and export into one file~~
- ~~Using LDAP for studentlist~~
- ~~BUG: some conditional formatting not working~~
- ~~Dont save when page already exists~~
- ~~Kompetenzzähler~~
- ~~Berechnung und Streichungen von WH/Wiederholung/SMÜ~~
- ~~add Cancel Number in settings~~
- ~~add load and merge button~~
- ~~add open... button for studentlistpath~~
- ~~add download LDAP Button in settings~~
- ~~Opendialog for studentlistpath~~
- ~~Create Negative Competences Column (ie. 1.1;1.3)~~
- ~~Competences Names to json file~~
- ~~Login to Moodle using Username and Password~~
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
