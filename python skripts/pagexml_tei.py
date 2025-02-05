import xml.etree.ElementTree as ET
import os
import re


def extract_metadata(metadata_path):
    tree = ET.parse(metadata_path)
    root = tree.getroot()

    title = root.find('title').text if root.find('title') is not None else "Unbekannter Titel"
    author = root.find('author').text if root.find('author') is not None else "Unbekannter Autor"
    doc_id = root.find('docId').text if root.find('docId') is not None else "Unbekannt"
    upload_timestamp = root.find('uploadTimestamp').text if root.find('uploadTimestamp') is not None else "Unbekannt"
    uploader = root.find('uploader').text if root.find('uploader') is not None else "Unbekannt"
    authority = root.find('authority').text if root.find('authority') is not None else "Unbekannte Quelle"
    desc = root.find('desc').text if root.find('desc') is not None else "Keine Beschreibung"

    return title, author, doc_id, upload_timestamp, uploader, authority, desc


def convert_pagexml_to_tei(pagexml_path, tei_output_path, metadata):
    title, author, doc_id, upload_timestamp, uploader, authority, desc = metadata

    tree = ET.parse(pagexml_path)
    root = tree.getroot()
    ns = {'p': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'}

    # TEI-Header erstellen
    tei = ET.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    tei_header = ET.SubElement(tei, "teiHeader")
    file_desc = ET.SubElement(tei_header, "fileDesc")
    title_stmt = ET.SubElement(file_desc, "titleStmt")
    ET.SubElement(title_stmt, "title").text = title
    ET.SubElement(title_stmt, "author").text = author
    pub_stmt = ET.SubElement(file_desc, "publicationStmt")
    ET.SubElement(pub_stmt, "publisher").text = uploader
    ET.SubElement(pub_stmt, "pubPlace").text = authority
    ET.SubElement(pub_stmt, "date", when=upload_timestamp).text = upload_timestamp
    source_desc = ET.SubElement(file_desc, "sourceDesc")
    ET.SubElement(source_desc, "p").text = desc

    # Text-Inhalt extrahieren
    text_elem = ET.SubElement(tei, "text")
    body = ET.SubElement(text_elem, "body")

    structure_mapping = {
        'page-number': 'page-number',
        'header': 'header',
        'heading': 'heading',
        'footer': 'footer',
    }

    current_paragraph = None

    for region in root.findall(".//p:TextRegion", ns):
        structure_type = "paragraph"
        custom_data_region = region.get('custom')
        if custom_data_region and 'structure {' in custom_data_region:
            structure_type_parts = custom_data_region.split('structure {type:')
            if len(structure_type_parts) > 1:
                structure_type = structure_type_parts[1].split(';')[0].strip('}')

        element_tag = structure_mapping.get(structure_type, 'paragraph')
        element = ET.SubElement(body, element_tag)

        for line in region.findall(".//p:TextLine", ns):
            unicode_elem = line.find(".//p:TextEquiv/p:Unicode", ns)
            if unicode_elem is not None and unicode_elem.text:
                text_line = unicode_elem.text

                # Wikidata-Metadaten mit Offset und Länge extrahieren
                custom_data_line = line.get('custom')
                if custom_data_line and 'wikiData:' in custom_data_line:
                    wikidata_match = re.search(
                        r'(person|place|date) \{.*?offset:(\d+); length:(\d+);.*?wikiData:(Q\d+);', custom_data_line)
                    if wikidata_match:
                        entity_type, offset, length, wikidata_id = wikidata_match.groups()
                        offset, length = int(offset), int(length)

                        # Extrahiere den spezifischen Text basierend auf Offset und Länge
                        tagged_text = text_line[offset:offset + length]

                        # Füge das Tag basierend auf dem Typ hinzu
                        if entity_type == 'person':
                            tagged_fragment = f'<persName ref="https://www.wikidata.org/wiki/{wikidata_id}">{tagged_text}</persName>'
                        elif entity_type == 'place':
                            tagged_fragment = f'<place ref="https://www.wikidata.org/wiki/{wikidata_id}">{tagged_text}</place>'
                        elif entity_type == 'date':
                            tagged_fragment = f'<date ref="https://www.wikidata.org/wiki/{wikidata_id}">{tagged_text}</date>'
                        else:
                            tagged_fragment = f'<name ref="https://www.wikidata.org/wiki/{wikidata_id}">{tagged_text}</name>'

                        # Ersetze den markierten Text im Text
                        text_line = text_line[:offset] + tagged_fragment + text_line[offset + length:]

                if structure_type == 'paragraph':
                    if current_paragraph is None:
                        current_paragraph = ET.SubElement(body, 'paragraph')
                        current_paragraph.text = text_line
                    else:
                        lb_elem = ET.SubElement(current_paragraph, "lb")
                        lb_elem.tail = f'\n{text_line}'
                else:
                    if element.text:
                        lb_elem = ET.SubElement(element, "lb")
                        lb_elem.tail = f'\n{text_line}'
                    else:
                        element.text = text_line

        if structure_type == 'paragraph':
            current_paragraph = None

    # TEI in Datei speichern
    tree = ET.ElementTree(tei)
    tree.write(tei_output_path, encoding="utf-8", xml_declaration=True)


def batch_convert_pagexml_to_tei(input_folder, output_folder, metadata_path):
    metadata = extract_metadata(metadata_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".xml", ".tei.xml"))
            convert_pagexml_to_tei(input_path, output_path, metadata)
            print(f"Converted: {filename} -> {output_path}")


# Beispielaufruf
batch_convert_pagexml_to_tei("C:\\Users\\Tim\\Desktop\\kap7\\page", "C:\\Users\\Tim\\Desktop\\kap7\\tei",
                             "C:\\Users\\Tim\\Desktop\\kap7\\metadata.xml")
