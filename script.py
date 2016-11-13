#!/usr/bin/env python3.5
import xml.parsers.expat
from textprocessing import get_sections_text
from sqlitedict import create_db, insert_values, create_index, close_db, commit
import zlib

inside_page = False
inside_title = False
inside_text = False
inside_sha1 = False

title_text = None
page_data = None
sha1_text = None

page_count = 0


def extract_definitions(lines):
    return get_sections_text(lines)

def start_element(element_name, attrs):
    global page_data, inside_page, page_count, inside_title, \
        inside_text, inside_sha1, title_text, sha1_text
    if element_name == 'page' and not inside_page:
        page_count += 1
        inside_page = True
    if element_name == 'text' and inside_page:
        page_data = [] # reset page_data
        inside_text = True
    if element_name == 'title' and inside_page:
        title_text = ''
        inside_title = True
    if element_name == 'sha1' and inside_page:
        sha1_text = ''
        inside_sha1 = True

def char_data(data):
    global page_data, inside_page, page_count, inside_title, \
        inside_text, inside_sha1, title_text, sha1_text
    if inside_page and inside_text:
        page_data.append(data)
    if inside_page and inside_title:
        title_text += data
    if inside_page and inside_sha1:
        sha1_text += data

def get_compressed_data(data):
    ba = bytearray(data, 'utf8')
    return zlib.compress(ba)

def create_record(checksum, title, data):
    ltitle = title.lower()
    char_sort = sorted(ltitle)
    char_sort = ''.join(char_sort)
    weight = 0
    for s in ltitle:
        weight+= ord(s)
    data = get_compressed_data(data)
    t = (checksum, title, data, weight, char_sort)
    return t

def end_element(element_name):
    global page_data, inside_page, page_count, inside_title, \
        inside_text, inside_sha1, title_text, sha1_text
    if element_name == 'page' and inside_page:
        inside_page = False
        # print('Title: ', str(title_text), '\n')
        # print('Text: ', extract_definitions(page_data), '\n')
        # print('sha1', str(sha1_text), '\n')
        t = create_record(sha1_text, title_text, extract_definitions(page_data))
        insert_values(t)
    if element_name == 'title' and inside_page:
        inside_title = False
    if element_name == 'text' and inside_page:
        inside_text = False
    if element_name == 'sha1' and inside_page:
        inside_sha1 = False

def create_sqlite_db():
    create_db()
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = start_element
    p.CharacterDataHandler = char_data
    p.EndElementHandler = end_element
    with open('/home/muqsith/Development/datasets/en-wiktionary/enwiktionary-latest-pages-articles.xml','rb') as f:
        p.ParseFile(f)
    commit()
    create_index()
    close_db()

if __name__ == "__main__":
    create_sqlite_db()
