import telebot
import spacy
import random


nlp = spacy.load("ru_core_news_sm")

TOKEN = ""

bot = telebot.TeleBot(TOKEN)


last_request = {}

# Функция для лемматизации существительных и добавления их в скобки в предложении
def bracket_nouns(text):
    doc = nlp(text)
    result = []

    for sent in doc.sents:
        nouns = [token for token in sent if token.pos_ == "NOUN"]

        if len(nouns) == 1:
            result.append(sent.text.replace(nouns[0].text, f"({nouns[0].lemma_})"))
        elif len(nouns) >= 2:
            lemmatized_nouns = [token.lemma_ for token in nouns[:2]]
            replaced_sent = sent.text.replace(nouns[0].text, f"({lemmatized_nouns[0]})")
            replaced_sent = replaced_sent.replace(nouns[1].text, f"({lemmatized_nouns[1]})")
            result.append(replaced_sent)

    return result


# Функция для получения 10 случайных предложений
def get_random_sentences(sentences):
    random_sentences = random.sample(sentences, min(len(sentences), 10))
    numbered_sentences = [(i + 1, sentence) for i, sentence in enumerate(random_sentences)]
    return numbered_sentences


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton('Упражнение на все падежи')
    itembtn2 = telebot.types.KeyboardButton('Упражнение на родительный падеж')
    itembtn3 = telebot.types.KeyboardButton('Упражнение на предложный падеж')
    itembtn4 = telebot.types.KeyboardButton('Упражнение на дательный падеж')
    itembtn5 = telebot.types.KeyboardButton('Упражнение на винительный падеж')
    itembtn6 = telebot.types.KeyboardButton('Упражнение на творительный падеж')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    bot.send_message(message.chat.id,
                     "Привет! Я бот, который делает упражнения типа 'раскройте скобки'.",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Упражнение на все падежи')
def ask_for_text(message):
    bot.send_message(message.chat.id, "Отправьте мне текст для анализа:")
    last_request[message.chat.id] = 'Упражнение на все падежи'


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Упражнение на родительный падеж':
        last_request[message.chat.id] = 'exercise_with_genitive'
        bot.send_message(message.chat.id, "Отправьте мне текст для анализа:")
    elif message.text == 'Упражнение на предложный падеж':
        last_request[message.chat.id] = 'exercise_with_locative'
        bot.send_message(message.chat.id, "Отправьте мне текст для анализа:")
    elif message.text == 'Упражнение на дательный падеж':
        last_request[message.chat.id] = 'exercise_with_dative'
        bot.send_message(message.chat.id, "Отправьте мне текст для анализа:")
    elif message.text == 'Упражнение на винительный падеж':
        last_request[message.chat.id] = 'exercise_with_accusative'
        bot.send_message(message.chat.id, "Отправьте мне текст для анализа:")
    elif message.text == 'Упражнение на творительный падеж':
        last_request[message.chat.id] = 'exercise_with_instrumental'
        bot.send_message(message.chat.id, "Отправьте мне текст для анализа:")
    elif message.chat.id in last_request and last_request[message.chat.id] == 'Упражнение на все падежи':

        lemmatized_sentences = bracket_nouns(message.text)

        # Получение и отправка 10 случайных предложений
        random_sentences = get_random_sentences(lemmatized_sentences)
        bot.send_message(message.chat.id, "10 случайных предложений:")
        for number, sentence in random_sentences:
            bot.send_message(message.chat.id, f"{number}. {sentence}")
        del last_request[message.chat.id]
    elif message.chat.id in last_request and last_request[message.chat.id] == 'exercise_with_genitive':
        del last_request[message.chat.id]
        exercise_with_genitive(message.text, message.chat.id)
    elif message.chat.id in last_request and last_request[message.chat.id] == 'exercise_with_locative':
        del last_request[message.chat.id]
        exercise_with_locative(message.text, message.chat.id)
    elif message.chat.id in last_request and last_request[message.chat.id] == 'exercise_with_dative':
        del last_request[message.chat.id]
        exercise_with_dative(message.text, message.chat.id)
    elif message.chat.id in last_request and last_request[message.chat.id] == 'exercise_with_accusative':
        del last_request[message.chat.id]
        exercise_with_accusative(message.text, message.chat.id)
    elif message.chat.id in last_request and last_request[message.chat.id] == 'exercise_with_instrumental':
        del last_request[message.chat.id]
        exercise_with_instrumental(message.text, message.chat.id)


# Функция для выполнения упражнения на родительный падеж
def exercise_with_genitive(text, chat_id):
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

    # Отправка результата обработки
    bot.send_message(chat_id, transformed_text)

# Функция для выполнения упражнения на предложный падеж

def exercise_with_locative(text, chat_id):
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ != 'PUNCT':
            cases[token.text] = token.morph.get('Case')

    loc_words = [word for word, cases in cases.items() if 'Loc' in cases]

    transformed_text = ""
    for token in doc:
        if token.pos_ == "NOUN" and token.text in loc_words:
            transformed_text += f"({token.lemma_}) "
        else:
            transformed_text += token.text_with_ws

    # Отправка результата обработки
    bot.send_message(chat_id, transformed_text)

def exercise_with_dative(text, chat_id):
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ != 'PUNCT':
            cases[token.text] = token.morph.get('Case')

    dat_words = [word for word, cases in cases.items() if 'Dat' in cases]

    transfor_text = ""
    for token in doc:
        if token.pos_ == "NOUN" and token.text in dat_words:
            transfor_text += f"({token.lemma_}) "
        else:
            transfor_text += token.text_with_ws

    # Отправка результата обработки
    bot.send_message(chat_id, transfor_text)


def exercise_with_accusative(text, chat_id):
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ != 'PUNCT':
            cases[token.text] = token.morph.get('Case')

    acc_words = [word for word, cases in cases.items() if 'Acc' in cases]

    transformed_text = ""
    for token in doc:
        if token.pos_ == "NOUN" and token.text in acc_words:
            transformed_text += f"({token.lemma_}) "
        else:
            transformed_text += token.text_with_ws

    # Отправка результата обработки
    bot.send_message(chat_id, transformed_text)

def exercise_with_instrumental(text, chat_id):
    doc = nlp(text)
    cases = {}
    for token in doc:
        if token.pos_ != 'PUNCT':
            cases[token.text] = token.morph.get('Case')

    ins_words = [word for word, cases in cases.items() if 'Ins' in cases]

    transformed_text = ""
    for token in doc:
        if token.pos_ == "NOUN" and token.text in ins_words:
            transformed_text += f"({token.lemma_}) "
        else:
            transformed_text += token.text_with_ws

    # Отправка результата обработки
    bot.send_message(chat_id, transformed_text)



# Запуск бота
bot.polling()
