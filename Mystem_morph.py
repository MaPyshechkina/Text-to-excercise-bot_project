

#импортируем все, что нужно
import os
import re, collections
import string
import nltk  #для токенизации
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk import Text as nltk_text
import re #для регулярных выражений
from pymystem3 import Mystem #для лемматизации
from nltk.corpus import stopwords
stop_words = stopwords.words('russian')
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('russian')
russian_stopwords = stopwords.words('russian')
from collections import Counter # для подсчета существительных в тексте



#2. Открывем файл, чистим от ударений
with open('Texts_А1.txt', 'r', encoding = 'utf-8') as f:
  text = f.read()

result = re.sub('\u0301', '', text) #0. уберу ударения из текста -- обычно учебные тексты с ударениями


#_____________________________________________________
#ЗАДАЧА 1 -- СДЕЛАТЬ ГЕНЕРАТОР УПРАЖНЕНИЙ С 1 ПАДЕЖОМ С ЧАСТОТНЫМИ СУЩЕСТВИТЕЛЬНЫМИ И МЕНЕЕ ЧАСТОТНЫМИ
#______________________________________________________


#3.считаем количество частотных существительных винительного падежа в тексте
mystem = Mystem()
new_text = []

for word in mystem.analyze(result):
  if word.get('analysis') and word['analysis'][0]['gr'].split(',')[0] == 'S' and word['analysis'][0]['gr'].split(',')[2][-3:]=='вин':
      new_text.append(word['text'])
number = Counter(new_text).most_common(60)
print(number)


#4.лемматизируем предложения с частотными существительными

without_num = [] #убераем цифры из частотного списка
for k, v in number:
    without_num.append(k)


filtered_sentences = [] #ищем предложения, в которых встречаются частотные сущ в вин падеже

for sentence in result.split("."):
    sentence_words = sentence.split(" ")
    contains_word = False
    for word in without_num:
        if word in sentence_words:
            contains_word = True
            break
    if contains_word:
        filtered_sentences.append(sentence)

        print(filtered_sentences)


mystem = Mystem()

lemmatized = [] #лемматиризируем существительные (вин) в уже отобранных предложениях

for sent in filtered_sentences: # берем предложения по одному
    for word in mystem.analyze(sent): # передаем 1 предложение в mystem
      if word.get('analysis') and word['analysis'][0]['gr'].split(',')[0] == 'S' and word['analysis'][0]['gr'].split(',')[2][-3:]=='вин':
          lemmatized.append('(' + word['analysis'][0]['lex'] + ')')
      else:
          lemmatized.append(word['text'])

lemmas_text = ''.join(lemmatized)
print(lemmas_text)



#5. создаем генератор 10 случайных предложений в винительном падеже
sentences = []   #преобразуем результут лемматизации в список
for line in lemmas_text.split('\n'):
    sentences.append(line)

#print(sentences)

result_par = [s for s in sentences if s != ''] #убираем пустые " "
print(result_par)

from random import choices   #запускаем рандомайзер и выводим 10 предложений с лемматизированными сущ в П4
random_proposals = list(choices(result_par, k=10))
print(random_proposals)


#найдем "редкие" существительные в винительном падеже
mystem = Mystem()
second_new_text = []

for word in mystem.analyze(result):
  if word.get('analysis') and word['analysis'][0]['gr'].split(',')[0] == 'S' and word['analysis'][0]['gr'].split(',')[2][-3:]=='вин':
      second_new_text.append(word['text'])

rare = sorted(Counter(second_new_text).items(), key=lambda x: x[1]) #преобразуем список от редких элементов к частотным
print(rare)

elements_with_unit_value = []

elements_with_one = [x for x in rare if int(x[1]) == 1] #
print(elements_with_one)


#Проблема: Я говорю Марии -- [3][-3:]=='род': >> 'S,имя,жен,од=(пр,ед|дат,ед|род,ед|им,мн)'}]
