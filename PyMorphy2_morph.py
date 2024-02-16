import os
import re, collections
import string
import pandas as pd
import pymorphy2
import json
from openpyxl import Workbook
from csv import excel


from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)



morph = pymorphy2.MorphAnalyzer()

with open('Texts_A0_without_stress.txt', 'r', encoding = 'utf-8') as f:
  text = f.read()

  text_words = []
  for word in [''.join([letter for letter in word if letter.isalpha()]) for word in text.split()]:
      word_info = morph.parse(word)[0]
      text_words.append(
          {
              'word': word,
              'case': word_info.tag.case,
              'POS': word_info.tag.POS
          })

  for word in text_words:
      print(word)


#файл в эксель
filename = 'morphy.xlsx'
pd.DataFrame(text_words).to_excel(filename, sheet_name='Sheet1', index=False)


# Находим слова в необходимом падеже
for word in text_words:
    for iter in word:
        if 'case' == iter and word ['case'] == 'gent':
            print(word['word'])

print(text_words)


# Лемматизируем слова в определенном падеже и кладём их в скобки
def lemmatize_genitive(text):
    morph = pymorphy2.MorphAnalyzer()
    tokens = text.split()
    lemmatized_text = []
    for token in tokens:
        parsed_token = morph.parse(token)[0]
        if 'NOUN' in parsed_token.tag and 'gent'in parsed_token.tag:
            lemmatized_text.append(f"({parsed_token.normal_form})")
        else:
            lemmatized_text.append(token)
    return ' '.join(lemmatized_text)

text = 'Я люблю Ивана. У меня нет сестры. У Анны нет брата. У моей сестры любовь.'
lemmatized_text = lemmatize_genitive(text)
print(lemmatized_text)


