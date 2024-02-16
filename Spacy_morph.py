
import spacy
import pandas as pd


nlp = spacy.load("ru_core_news_sm")

with open('Texts_A0_without_stress.txt', 'r', encoding = 'utf-8') as f:
  text = f.read()

doc = nlp(text)

cases_info = []

for token in doc:
    case = token.morph.get('Case')
    cases_info.append((token.text, case))

# df = pd.DataFrame(cases_info, columns=['Токен', 'Падеж'])
# df.to_excel("Spacy.xlsx", index=False)


#Как лемматизировать по падежу:

cases = {}

for token in doc:
    if token.pos_ != 'PUNCT':
        cases[token.text] = token.morph.get('Case')

print(cases)

# Создание списка слов в родительном падеже
gen_words = [word for word, cases in cases.items() if 'Gen' in cases]

transformed_text = ""

for token in doc:
    if token.pos_ == "NOUN" and token.text in gen_words:
        transformed_text += f"({token.lemma_}) "
    else:
        transformed_text += token.text_with_ws

print(transformed_text)


#функция для поиска частотных существительных в Gen

def freq_nouns_genitive(text):
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ != 'PUNCT':
            cases[token.text] = token.morph.get('Case')

    gen_words = [word for word, cases in cases.items() if 'Gen' in cases]

    return gen_words[:60]

print(freq_nouns_genitive(text))


#функция для поиска редких существительных в Gen
def rare_nouns_genitive(text):
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ == 'NOUN' and token.morph.get('Case') == 'Gen':
            lemma = token.lemma_.lower()
            cases[lemma] = cases.get(lemma, 0) + 1  # Считаем количество каждого существительного

    # Выбираем существительные, которые встретились реже 2 раз
    rare_nouns = [word for word, count in cases.items() if count < 2]

    return rare_nouns

print(rare_nouns_genitive(text))


