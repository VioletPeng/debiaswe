#!/usr/bin/python

import sys
import codecs
import json

def extract_words_json(infile):
    words = []
    parsed_json = []
    with open(infile) as inf:
        for line in inf:
            parsed_line = json.loads(line)
            parsed_json.append(parsed_line)
            for elem in parsed_line:
                words.append(elem[0])
        return parsed_json, words

def load_words(infile):
    words = []
    with codecs.open(infile, encoding='utf-8') as inf:
        for line in inf:
            words.append(line.strip())
    return words

def compose_new_json(full_info, words):
    count = 0
    for elem in full_info:
        for info in elem:
            info[0] = words[count]
            count += 1
    print(json.dumps(full_info, ensure_ascii=False).encode('utf8'))

if __name__ == '__main__':
    parsed_json, words = extract_words_json(sys.argv[1])
    new_words = load_words(sys.argv[2])
    compose_new_json(parsed_json, new_words)
