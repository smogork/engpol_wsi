#! /usr/bin/python

import sys
import csv

class TranslationRecord:
    def __init__(self, translation):
        self.translation = translation
        self.original_words = dict()
        self.total_original_words = 0

    def add_word(self, word):
        self.add_word_count(word, 1)

    def add_word_count(self, word, count):
        if self.original_words.get(word) is None:
            self.original_words[word] = count
        else:
            self.original_words[word] += count
        self.total_original_words += count

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
        stripped = word.lower().strip('".,?!\n-')

        if word_dictionary.get(stripped) is None:
            word_dictionary[stripped] = 1
        else:
            word_dictionary[stripped] += 1
        word_in_line += 1

    return word_in_line

def count_translations(translationLine, originalLine, translationDictionary) -> None:
    translationLine.strip()
    originalLine.strip()
    translationWords = translationLine.split()
    originalWords = originalLine.split()

    #Jezeli nie istnieje dane tlumaczenie, to dodaj element do slownika
    for translation in translationWords:
        correctTranslation = translation.lower().strip('".,?!\n-')
        if translationDictionary.get(correctTranslation) is None:
            translationDictionary[correctTranslation] = TranslationRecord(correctTranslation)

    #walic roznice dlugosci -> slowo po slowie
    for it in range(0, min(len(originalWords), len(translationWords))):
        correct_translation = translationWords[it].lower().strip('".,?!\n-')
        correct_original = originalWords[it].lower().strip('".,?!\n-')
        translationDictionary[correct_translation].add_word(correct_original)

    '''#Przypdaek oryginału krótszego lub równego od tłumaczenia
    if len(translationWords) >= len(originalWords):
        offset = 0
        while offset + len(originalWords) <= len(translationWords):
            for original_it in range(0, len(originalWords)):
                correct_translation = translationWords[original_it + offset].lower().strip('".,?!\n-')
                correct_original = originalWords[original_it].lower().strip('".,?!\n-')
                translationDictionary[correct_translation].add_word(correct_original)
            offset += 1
    #Przypdaek tłumaczenia dluższego od oryginalu
    else:
        offset = 0
        while offset + len(translationWords) <= len(originalWords):
            for translation_it in range(0, len(translationWords)):
                correct_translation = translationWords[translation_it].lower().strip('".,?!\n-')
                correct_original = originalWords[translation_it + offset].lower().strip('".,?!\n-')
                translationDictionary[correct_translation].add_word(correct_original)
            offset += 1'''

def reverse_translation_dictionary(translation_dictionary) -> dict():
    ret = dict()

    for translationRecord in translation_dictionary:
        record = translation_dictionary[translationRecord]
        for original_word in record.original_words:
            if ret.get(original_word) is None:
                ret[original_word] = TranslationRecord(original_word)
            ret[original_word].add_word_count(record.translation, record.original_words[original_word])

    return ret

def select_best_translations(translation_dictionary, pol_count, pol_words_total) -> dict():
    ret = dict()

    for translationRecord in translation_dictionary:
        record = translation_dictionary[translationRecord]

        best_probability = 0
        best_pair = ("", "")

        for translation in record.original_words:
            target_probability = pol_count[translation] / pol_words_total
            translation_probability = record.original_words[translation] / record.total_original_words
            prob = target_probability * translation_probability
            if prob > best_probability:
                best_probability = prob
                best_pair = (record.translation, translation)

        ret[best_pair[0]] = best_pair[1]
    
    return ret

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

    #Zamień słownik do zliczenia tłumaczeń na słownik
    #z prawdopodobieństwami tłumaczeń dla oryginalnych słów
    reverse_dictionary = reverse_translation_dictionary(translation_count)

    #Przetwórz wyniki na podobne do danych wejściowych brutala
    brutal_data = select_best_translations(reverse_dictionary, pol_count, pol_words_total)

    #Na końcu zapisz wyniki do CSV
    with open(sys.argv[3], 'w') as csvFile:
        writer = csv.writer(csvFile)
        for row in brutal_data:
            writer.writerow([row, brutal_data[row]])


if __name__ == '__main__':
    main()