#! /usr/bin/python

import sys
import csv

def usage(command) -> None:
    print(f'Usage: {command} word_dictionary_path')
    print('Reads words from STDIN until encounters EOL.')

def init_dictionary(dict_path) -> dict:
    result = dict()

    with open(dict_path) as dictionary:
        dict_reader = csv.reader(dictionary)
        for record in dict_reader:
            result[record[0]] = record[1]

    return result

def brutal_translate(line, words) -> str:
    result = ''

    #Obranie wejścia ze spacji
    line.strip()

    for word in line.split():
        stripped = word.lower().strip('".,?!')

        if stripped in words:
            result = result + f'{words[stripped]} '
        else:
            result = result + f'{stripped} '
        
    
    return result

def main() -> None:
    if len(sys.argv) < 2:
        usage(sys.argv[0])
        exit(1)

    #Wczytaj słownik
    words = init_dictionary(sys.argv[1])
    print(f'Dictionary initialized with {len(words)} words.')

    #Czytaj linie z STDIN
    for line in sys.stdin:
        translation = brutal_translate(line, words)
        print(translation)

if __name__ == '__main__':
    main()