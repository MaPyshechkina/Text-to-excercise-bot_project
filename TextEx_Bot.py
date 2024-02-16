import telebot
from telebot import types
import spacy
import os


nlp = spacy.load("ru_core_news_sm")


bot = telebot.TeleBot("Token")
print(bot)



# Функция для нахождения частотных существительных в генитиве

def freq_nouns_genitive(message):
    text = message.text
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ != 'PUNCT':
            cases[token.text] = token.morph.get('Case')

    gen_words = [word for word, cases in cases.items() if 'Gen' in cases]

    return gen_words[:60]



# Функция для создания упражнения с частотными существительными в предложениях
def exercise_with_nouns(message):
    text = message.text
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ != 'PUNCT':
            cases[token.text] = token.morph.get('Case')

    gen_words = [word for word, cases in cases.items() if 'Gen' in cases]

    transformed_text = ""
    for token in doc:
        if token.pos_ == "NOUN" and token.text in gen_words:
            transformed_text += f"({token.lemma_}) "
        else:
            transformed_text += token.text_with_ws

    return transformed_text

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Частотные существительные в Gen')
    item2 = types.KeyboardButton('Упражнение с частотными существительными в Gen')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)




# Обработчик кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Частотные существительные в Gen':
        bot.send_message(message.chat.id, "Введите текст для анализа:")
        bot.register_next_step_handler(message, get_genitive_freq_nouns)
    elif message.text == 'Упражнение с частотными существительными в Gen':
        bot.send_message(message.chat.id, "Введите текст для анализа:")
        bot.register_next_step_handler(message, get_exercise_with_nouns)


        

# Обработчик текстовых сообщений для кнопки 1
def get_genitive_freq_nouns(message):
    gen_words = freq_nouns_genitive(message)
    bot.send_message(message.chat.id, "Частотные существительные в Gen:\n" + ", ".join(gen_words))




# Обработчик текстовых сообщений для кнопки 2
def get_exercise_with_nouns(message):
    transformed_text = exercise_with_nouns(message)
    with open("exercise.txt", "w") as file:
        file.write(transformed_text)
    bot.send_document(message.chat.id, open("exercise.txt", "rb"))
    os.remove("exercise.txt")


bot.polling()
