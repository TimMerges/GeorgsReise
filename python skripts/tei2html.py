import xml.etree.ElementTree as ET
import os

def convert_tei_to_html(tei_file, html_file):
    tree = ET.parse(tei_file)
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    body = root.find('.//tei:body', ns)
    page_number_elem = root.find('.//tei:page-number', ns)
    page_number = page_number_elem.text if page_number_elem is not None else ""

    # Nur die Seitenzahl ausgeben
    html_content = f'<span class="page-number">{page_number}</span>'

    # Verarbeite die einzelnen Elemente im Body
    for elem in body:
        tag = elem.tag.split('}')[-1]  # Entfernt den Namespace-Teil

        if tag in ['header', 'heading']:
            heading_text = process_text_with_links(elem)
            html_content += f'<h2>{heading_text}</h2>'
        elif tag == 'paragraph':
            paragraph_text = process_text_with_links(elem)
            if paragraph_text.strip():  # Nur nicht-leere Absätze hinzufügen
                html_content += f'<p>{paragraph_text}</p>'
        elif tag == 'footer':
            footer_text = process_text_with_links(elem)
            html_content += f'<div class="footer">{footer_text}</div>'

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


def process_text_with_links(element):
    """Verwandelt TEI-Tags wie <place> und <persName> in HTML-Links."""
    text_content = ""
    for part in element.iter():
        part_tag = part.tag.split('}')[-1]

        # Tags mit Referenzen in anklickbare Links umwandeln
        if part_tag in ['persName', 'place', 'date', 'name'] and 'ref' in part.attrib:
            ref_link = part.attrib['ref']
            text = part.text if part.text else ""
            text_content += f'<a href="{ref_link}" target="_blank">{text}</a>'
        elif part.text:
            text_content += part.text  # Normaler Text

        if part.tail:
            text_content += part.tail  # Nachfolgender Text (tail) hinzufügen

    return text_content


def batch_convert_tei_to_html(tei_folder, html_folder):
    if not os.path.exists(html_folder):
        os.makedirs(html_folder)

    for filename in os.listdir(tei_folder):
        if filename.endswith(".tei.xml"):
            tei_path = os.path.join(tei_folder, filename)
            html_path = os.path.join(html_folder, filename.replace(".tei.xml", ".html"))
            convert_tei_to_html(tei_path, html_path)
            print(f"Converted: {tei_path} -> {html_path}")


# Beispielaufruf
batch_convert_tei_to_html("pfad/zum/input", "pfad/zum/output")
