#! /usr/bin/python

import sys

def usage(command) -> None:
    print(f'Usage: {command} english_data polish_translation output')
    print('english_data - path to english dataset with sentences')
    print('polish_translation - path to polish dataset with translations')
    print('output - path to output file')

def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])
        exit(1)
    
    
    with open(sys.argv[1], 'r') as eng:
        with open(sys.argv[2], 'r') as pol:
            #Wczytaj po jednej linijce z danych wejsciowych
            engLine = eng.readline()
            polLine = pol.readline()

            while engLine != "" and polLine != "":
                #Zlicz wystąpienie polskich słów

                #Zlicz wystapienie tlumaczenia
                #Jezeli zdania maja rozne dlugosci słów,
                #to wykonaj dla kazdego możliwego offsetu

                engLine = eng.readline()
                polLine = pol.readline()

    #Na końcu zapisz wyniki do CSV

if __name__ == '__main__':
    main()