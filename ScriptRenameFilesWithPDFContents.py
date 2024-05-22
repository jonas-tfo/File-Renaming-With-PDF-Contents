'''
Infos zum Python-Skript:
- Benennt Dateien um, basierend auf den Inhalt einer Clinical Report (.pdf), welche beim Auslesen von Actigraphen generiert werden kann.
- Basiert darauf, dass eine Gruppe von Dateien zu jeder individuellen ID + Testzeitpunkt gehört. Dabei enthält jede Gruppe von Dateien eine Kombination von 
  Actigraphnummer und Datum, was individuell zur jeweiligen individuellen ID + Testzeitpunkt ist, es wiederholt sich also nicht; so werden alle Dateien, die 
  zu einer ID + Zeitpunkt gehören entsprechend umbenannt (alle Dateinamen für jeweilige ID + Zeitpunkt erhalten den gleichen Anfang).
------------------------------------------------------------------------------------------------------------------------------------------------------------
- Um den Laufwerk festzustellen:
  als "directory" den Laufwerk angeben (directory = "C:\...")
------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

# benötigte Pakete
import os
import re
import pypdf
from pathlib import Path

# ordner festlegen, wo die Dateien liegen
directory = ""

# funktion, um Name (ID + Zeitpunkt) von der PDF zu extrahieren
def extract_subject_name(pdf_path):
    with open(pdf_path, 'rb') as openedpdf:
        reader = pypdf.PdfReader(openedpdf)				    # liest die geöffnete PDF
        page = reader.pages[0]                                              # bestimmt, dass Name auf der ersten Seite ist
        text = page.extract_text()                             		    # extrahiert Text, was auf erster Seite steht
        subject_name = re.search(r'Name: (.+)', text)         		    # Name wird extrahiert (mit regex) -> "Name:" + individuelle ID_Zeitpunkt
        if subject_name:
            return subject_name.group(1).strip()               		    # isoliert subject_name
        else:
            return None

# loop, der durch alle Dateien geht 
for filename in os.listdir(path=directory):
    if filename.endswith('.pdf'):                               	    # selectiert eine PDF nach dem anderen (aus dem Laufwerk)
        pdf_path = os.path.join(directory, filename)            	    # erstellt Pfad zur PDF
        subject_name = extract_subject_name(pdf_path)           	    # ID und Zeitpunkt wird aus PDF gezogen
        if subject_name:                                         	    # Wenn ID + Zeitpunkt vorhanden                                 
            pdf_first_26 = filename[0:26]                       	    # ersten 26 Charakter des Dateinamens

            for file in os.listdir(directory):                  	    # für JEDE Datei im Laufwerk
                if file.startswith(pdf_first_26):                	    # selectiert Dateien, die mit den ersten 25 Charaktern der PDF Datei anfangen
                    new_filename = f"{subject_name}_{file}"      	    # extrahierte ID + Zeitpunkt wird zur Dateiname hinzugefügt

                    old_file_path = os.path.join(directory, file)           # alter Pfad zur Datei
                    new_file_path = os.path.join(directory, new_filename)   # neuer Pfad zur Datei (mit CogniFiT_ID_Zeitpunkt am anfang)

                    os.rename(old_file_path, new_file_path)      	    # benennt die Datei um 