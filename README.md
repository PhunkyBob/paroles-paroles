# Paroles-paroles

Ce script permet de récupérer toutes les paroles d'un artiste en se basant sur les données du site [paroles.net](https://www.paroles.net). 

## Utilisation
Le script peut s'utiliser de 2 modes : interactif ou ligne de commande.
### Mode interactif
```
python download_lyrics.py
```
```
[?] Artist to search: angele
[?] Choose the desired artist: Angèle
 > Angèle
   Angèle Osinki
   Los Angeles Azules

Songs found: 37
[?] Continue, download and save all to "DOWNLOADS": Yes, but change folder
   Yes
   No
 > Yes, but change folder

[?] Save folder: temp
37 files saved.
```

### Ligne de commande
```
python download_lyrics.py [OPTIONS] [ARTIST_URL]

Options:
  --download-folder TEXT  Download folder.
  --help                  Show this message and exit.
```

Exemple : 
```
python download_lyrics.py --download-folder DOWNLOADS/Angèle https://www.paroles.net/angele
```

## Installation
### Prérequis
- Python 3.10+

### Configuration
```
git clone https://github.com/PhunkyBob/paroles-paroles
cd paroles-paroles
python -m venv venv
venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

## Tests unitaires
```
pytest tests
```
