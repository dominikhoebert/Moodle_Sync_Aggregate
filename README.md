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

- **rework export function object oriented, more stable**
- add config JSON to every course
- Low Priority
  - improve import functionality
  - bestehungsgrenze aus modul
  - statistics? anzahl an noten, kompetenzen, schüler, ...
  - graphes for statistics?
  - andere Berechnungen?
  - export as json
