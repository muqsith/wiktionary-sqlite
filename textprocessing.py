import re

section_pattern = re.compile(r'^=+.+=$')

def check_section_start(line):
    global section_pattern
    sections = ['NOUN', 'PRONOUN', 'ADJECTIVE', 'VERB', 'ADVERB', 'PREPOSITION', 'CONJUNCTION', 'INTERJECTION', 'ETYMOLOGY', 'PRONUNCIATION', 'USAGE']
    result = False
    if section_pattern.search(line):
        line = line.strip()
        line = line.upper()
        for part_of_speech in sections:
            pos_pattern = re.compile(r'[ =]+('+part_of_speech+'){1}[ =]+')
            if pos_pattern.search(line):
                result = True
    return result

def check_section_end(line):
    global section_pattern
    result = False
    if section_pattern.search(line) and not check_section_start(line):
        result = True
    return result

def get_sections(lines):
    sections_data = {}
    keep_reading = False
    current_section_title = 0
    for line in lines:
        if check_section_start(line):
            keep_reading = True
            current_section_title += 1
            sections_data[current_section_title] = line
            continue
        if check_section_end(line):
            keep_reading = False
            continue
        if keep_reading:
            try:
                if sections_data[current_section_title]:
                    sections_data[current_section_title] = sections_data[current_section_title] +'\n'+ line
            except:
                pass
    return sections_data

def get_sections_text(lines):
    text = ''
    sections_data = get_sections(lines)
    if sections_data:
        for key in sections_data:
            text += '\n'+sections_data[key]
    return text
