#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from lxml import etree

################################################################################
# 1) HIER EINSTELLEN: Feste Pfade, in & output
################################################################################
INPUT_FOLDER = r"pfad\zum\input"
OUTPUT_FOLDER = r"pfad\zum\output"

Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

################################################################################
# 2) Fester TEI-Header
################################################################################
FIXED_TEI_HEADER = """<teiHeader>
  <fileDesc n="">
    <titleStmt>
      <title>Georg Forster's sämmtliche Schriften: In neun Bänden. 1  Seite</title>
      <editor>
        <persName role="Herausgeber">
          <forename>Tim</forename>
          <surname>Merges</surname>
          <affiliation>Universität Trier (Student)</affiliation>
        </persName>
        <persName role="Herausgeberin">
          <forename>Sarah</forename>
          <surname>Sarkis</surname>
          <affiliation>Universität Trier (Student)</affiliation>
        </persName>
        <persName role="Herausgeberin">
          <forename>Patricia</forename>
          <surname>Folly</surname>
          <affiliation>Universität Trier (Student)</affiliation>
        </persName>
      </editor>
      <respStmt>
        <resp>Mitwirkende an der Transkription</resp>
        <persName>
          <forename>Tim</forename>
          <surname>Merges</surname>
        </persName>
        <persName>
          <forename>Sarah</forename>
          <surname>Sarkis</surname>
        </persName>
        <persName>
          <forename>Patricia</forename>
          <surname>Folly</surname>
        </persName>
      </respStmt>
    </titleStmt>
    <editionStmt>
      <edition>Digitale Edition Georg Forster's Reise um die Welt 1. Band in Teilen 2025</edition>
    </editionStmt>
    <publicationStmt>
      <publisher>
        <persName>
          <forename>Tim</forename>
          <surname>Merges</surname>
        </persName>
        <persName>
          <forename>Patricia</forename>
          <surname>Folly</surname>
        </persName>
        <persName>
          <forename>Sarah</forename>
          <surname>Sarkis</surname>
        </persName>
      </publisher>
      <availability>
        <licence target="https://creativecommons.org/licenses/by-nc-sa/3.0/de/">
          Namensnennung - Nicht-kommerziell - Weitergabe unter gleichen Bedingungen 3.0 Deutschland (CC BY-NC-SA 3.0 DE)
        </licence>
        <ab type="version">version-02-10</ab>
        <ab type="edition">Digitale Edition</ab>
        <ab type="state">Transkription mit Wikidata-Verlinkungen</ab>
      </availability>
      <date when="2025-02-10"/>
      <idno type="url">https://timmerges.github.io/GeorgsReise/index.html</idno>
    </publicationStmt>
    <sourceDesc>
      <bibl>
        <title>Georg Forster's sämmtliche Schriften: In neun Bänden. 1</title>
        <idno type="print">BSB-ID 991123990369707356</idno>
      </bibl>
      <msDesc>
        <msIdentifier>
          <institution>Leipzig: F. A. Brockhaus, 1843</institution>
          <idno type="signatur">BSB-ID 991123990369707356</idno>
        </msIdentifier>
        <physDesc>
          <objectDesc>
            <supportDesc>
            </supportDesc>
          </objectDesc>
        </physDesc>
      </msDesc>
    </sourceDesc>
  </fileDesc>
</teiHeader>
"""


for xml_file in Path(INPUT_FOLDER).glob("*.xml"):
    print(f"[INFO] Verarbeite: {xml_file.name}")

    # (a) Alte Datei lesen
    old_content = xml_file.read_text(encoding="utf-8")

    # (b) <text> extrahieren
    parser = etree.XMLParser(remove_blank_text=False)
    root = etree.fromstring(old_content.encode("utf-8"), parser=parser)
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    text_elms = root.xpath("//tei:text", namespaces=ns)
    if text_elms:
        text_str = etree.tostring(text_elms[0], encoding="unicode")
    else:
        text_str = "<text/>"

    #  RegEx-Ersetzungen:
    #     <heading> -> <head>, <paragraph> -> <p>, <page-number> -> <pb n="..."/>,
    #     Timestamps in when="..." ersetzen, <lb/> behalten wir.
    text_str = re.sub(r"<heading>(.*?)</heading>", r"<head>\1</head>", text_str, flags=re.IGNORECASE|re.DOTALL)
    text_str = re.sub(r"<paragraph\s*/>", r"<p/>", text_str, flags=re.IGNORECASE)
    text_str = re.sub(r"<paragraph>(.*?)</paragraph>", r"<p>\1</p>", text_str, flags=re.IGNORECASE|re.DOTALL)

    def replace_page_number(m):
        content = m.group(1).strip()
        if content:
            return f'<pb n="{content}"/>'
        return "<pb/>"
    text_str = re.sub(r"<page-number>(.*?)</page-number>", replace_page_number, text_str, flags=re.IGNORECASE|re.DOTALL)

    text_str = re.sub(r'(when=")\d{9,}(")', r'\1 2025-02-11 \2', text_str)

    new_tei = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">\n'
        f'{FIXED_TEI_HEADER}\n'
        f'{text_str}\n'
        '</TEI>\n'
    )

    out_name = xml_file.name
    out_path = Path(OUTPUT_FOLDER) / out_name
    out_path.write_text(new_tei, encoding="utf-8")
    print(f"[OK] => {out_path}")
