import os
import re

def convert_tags_to_links(html_folder):
    # Alle HTML-Dateien im angegebenen Ordner durchsuchen
    for filename in os.listdir(html_folder):
        if filename.endswith(".html"):
            file_path = os.path.join(html_folder, filename)

            # Dateiinhalt lesen
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Tags <place>, <persName>, <name>, <date> in <a> umwandeln
            content = re.sub(r'<(place|persName|name|date) ref="(.*?)">(.*?)</\1>', r'<a href="\2" target="_blank">\3</a>', content)

            # Geänderten Inhalt zurück in die Datei schreiben
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Verlinkungen aktualisiert in: {filename}")

# Pfad zum HTML-Ordner angeben
html_folder = ""
convert_tags_to_links(html_folder)



