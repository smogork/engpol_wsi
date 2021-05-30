#! /usr/bin/python

import sys

class TranslationRecord:
    def __init__(self, translation):
        self.translation = translation
        self.original_words = dict()
        self.total_original_words = 0

    def add_word(self, word):
        if self.original_words.get(word) is None:
            self.original_words[word] = 1
        else:
            self.original_words[word] += 1
        self.total_original_words += 1

    def __repr__(self):
        ret = ""
        
        for word in self.original_words:
            ret += f'{self.translation} -> {word}[{self.original_words[word]}]\n'
        
        return ret


def usage(command) -> None:
    print(f'Usage: {command} english_data polish_translation output')
    print('english_data - path to english dataset with sentences')
    print('polish_translation - path to polish dataset with translations')
    print('output - path to output file')

def count_words(line, word_dictionary) -> int:
    word_in_line = 0

    line.strip()
    for word in line.split():
        stripped = word.lower().strip('".,?!')

        if word_dictionary.get(word) is None:
            word_dictionary[word] = 1
        else:
            word_dictionary[word] += 1
        word_in_line += 1

    return word_in_line

def count_translations(translationLine, originalLine, translationDictionary):
    translationLine.strip()
    originalLine.strip()
    translationWords = translationLine.split()
    originalWords = originalLine.split()

    #Jezeli nie istnieje dane tlumaczenie, to dodaj element do slownika
    for translation in translationWords:
        correctTranslation = translation.lower().strip('".,?!')
        if translationDictionary.get(correctTranslation) is None:
            translationDictionary[correctTranslation] = TranslationRecord(correctTranslation)

    #Przypdaek oryginału krótszego lub równego od tłumaczenia
    if len(translationWords) >= len(originalWords):
        offset = 0
        while offset + len(originalWords) <= len(translationWords):
            for original_it in range(0, len(originalWords)):
                correct_translation = translationWords[original_it + offset].lower().strip('".,?!')
                correct_original = originalWords[original_it].lower().strip('".,?!')
                translationDictionary[correct_translation].add_word(correct_original)
            offset += 1
    #Przypdaek tłumaczenia dluższego od oryginalu
    else:
        offset = 0
        while offset + len(translationWords) <= len(originalWords):
            for translation_it in range(0, len(translationWords)):
                correct_translation = translationWords[translation_it].lower().strip('".,?!')
                correct_original = originalWords[translation_it + offset].lower().strip('".,?!')
                translationDictionary[correct_translation].add_word(correct_original)
            offset += 1


def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])
        exit(1)
    
    pol_count = dict()
    pol_words_total = 0

    translation_count = dict()
    
    with open(sys.argv[1], 'r') as eng:
        with open(sys.argv[2], 'r') as pol:
            #Wczytaj po jednej linijce z danych wejsciowych
            engLine = eng.readline()
            polLine = pol.readline()

            while engLine != "" and polLine != "":
                #Zlicz wystąpienie polskich słów
                pol_words_total += count_words(polLine, pol_count)

                #Zlicz wystapienie tlumaczenia
                #Jezeli zdania maja rozne dlugosci słów,
                #to wykonaj dla kazdego możliwego offsetu
                count_translations(polLine, engLine, translation_count)

                engLine = eng.readline()
                polLine = pol.readline()

    #Na końcu zapisz wyniki do CSV

if __name__ == '__main__':
    main()