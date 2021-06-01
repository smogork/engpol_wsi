#! /usr/bin/python

from string import punctuation, whitespace
from math import sqrt

meaningless_characters = punctuation + whitespace + "”"
meaningless_english_words = ["a", "the"]


def split_sentence_to_words(sentence: str) -> list[str]:
    words = sentence.lower().split()
    stripped_words = list(map(lambda word: word.strip(meaningless_characters), words))
    stripped_words = list(filter(lambda word: len(word) > 0, stripped_words))
    return stripped_words


def filter_out_meaningless_words(words: list[str], meaningless_words: list[str]) -> list[str]:
    return list(filter(lambda word: word not in meaningless_words, words))


class TranslationSet:

    source_word: str
    target_word_counts: dict[str, int]

    def __init__(self, source_word: str):
        self.source_word = source_word
        self.target_word_counts = {}

    def __repr__(self):
        r = "( "
        for target_word, occurence_count in self.target_word_counts.items():
            r += f"{occurence_count}x'{target_word}' "
        return r + ")"

    def add_translation(self, target_word: str, count: int = 1):
        if target_word in self.target_word_counts:
            self.target_word_counts[target_word] += count
        else:
            self.target_word_counts[target_word] = count


class TranslationAggregator:

    translations: dict[str, TranslationSet]
    target_words: dict[str, int]

    def __init__(self):
        self.translations = {}
        self.target_words = {}

    def _correlate_words(self, source_words: list[str], target_words: list[str]) -> list[tuple[str, str]]:
        source_words = filter_out_meaningless_words(source_words, meaningless_english_words)
        min_len = min(len(source_words), len(target_words))
        source_words, target_words = source_words[:min_len], target_words[:min_len]
        return list(zip(source_words, target_words))

    def learn_from_corresponding_words(self, source_word: str, target_word: str):
        if source_word not in self.translations:
            self.translations[source_word] = TranslationSet(source_word)
            self.target_words[source_word] = 0
        self.translations[source_word].add_translation(target_word)
        self.target_words[source_word] += 1

    def learn_from_corresponding_sentence(self, source_sentence: str, target_sentence: str):
        source_words = split_sentence_to_words(source_sentence)
        target_words = split_sentence_to_words(target_sentence)
        corresponding_words = self._correlate_words(source_words, target_words)
        for source_word, target_word in corresponding_words:
            self.learn_from_corresponding_words(source_word, target_word)

    def learn_from_corresponding_sentences(self, source_sentences: list[str], target_sentence: list[str]):
        for source_sentence, target_sentence in zip(source_sentences, target_sentence):
            self.learn_from_corresponding_sentence(source_sentence, target_sentence)


class StatisticalTranslator:

    mappings: dict[str, str]

    def __init__(self, aggregator: TranslationAggregator):
        self.mappings = {}
        for translation_set in aggregator.translations.values():
            translations = []
            for target_word, occurrences in translation_set.target_word_counts.items():
                total_occurences = aggregator.target_words.get(target_word, 0)
                weight = occurrences
                translations.append((target_word, weight))

            if translations:
                #print(translation_set.source_word, sorted(translations, key=lambda word_weight: word_weight[1]))
                best_translation = max(translations, key=lambda word_weight: word_weight[1])[0]
                self.mappings[translation_set.source_word] = best_translation

    def __call__(self, string) -> str:
        words = split_sentence_to_words(string)
        return " ".join(map(lambda word: self.mappings.get(word, "["+word+"]"), words))


if __name__ == '__main__':
    source_file = "trainingData/sentences/sentences1.txt"
    target_file = "trainingData/translatedSentences/sentences1.en.pl.txt"

    source_sentences: list[str]
    with open(source_file, "r") as f:
        source_sentences = f.readlines()

    target_sentences: list[str]
    with open(target_file, "r") as f:
        target_sentences = f.readlines()

    aggregator = TranslationAggregator()
    aggregator.learn_from_corresponding_sentences(source_sentences, target_sentences)

    translator = StatisticalTranslator(aggregator)

    test_strings = """Ala has cat.
I am sorry but your going abroad is out of the question.
The policeman appeared out of the blue and ordered us to leave the house.
You can get these books for nothing if you ask my brother.
I will be right back.
In the meantime, you can watch TV.
Mike tried to repair his old TV many times, but without success.
I’ve heard that David was arrested yesterday.
I think somebody’s trying to frame him.
Your sister says that you have a brain lesion.
It was getting dark so I switched on the light and drew the blinds.
Kate immersed herself in the book.
How shall I put it?
I think we’re done.
Please make sure that we leave on time.
I tried very hard but we didn’t manage to find common ground.
Her spoilt children were always crying for the moon.
If I were you, I would have gone on that trip.
Long time no see.
What have you been up to lately?
Working here is seen by many as a career dead end.
""".splitlines(keepends=False)

    for string in test_strings:
        print(string)
        print(translator(string))
        print()
