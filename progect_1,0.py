import logging
from telebot import TeleBot, types
import random

TOKEN = '7207116047:AAGAV3wzI9UV5VZoJR6nyhPU4Kd_F-xTs5M'

logging.basicConfig(level=logging.INFO)

bot = TeleBot(TOKEN)

skips = 3
current_level = 1
current_word = ''
solved_words = 0

@bot.message_handler(commands=['start'])
def start(message):
    global current_level, current_word, skips, hints
    current_level = 0
    current_word = ''
    hints = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('Старт')
    ciphers_button = types.KeyboardButton('Шифры')
    stats_button = types.InlineKeyboardButton('Статистика')#, callback_data='stats')
    markup.add(start_button, ciphers_button, stats_button)
    skips = 3

@bot.message_handler(func=lambda message: message.text == 'Шифры')
def show_ciphers(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    caesar_button = types.KeyboardButton('Шифр Цезаря')
    polybius_button = types.KeyboardButton('Квадрат Полибия')
    trisemus_button = types.KeyboardButton('Таблица Трисемуса')
    playfair_button = types.KeyboardButton('Биграммный шифр Плейфера')
    base32_button = types.KeyboardButton('32-ричная система счисления')
    exit_button = types.KeyboardButton('Выход')
    markup.add(caesar_button, polybius_button, trisemus_button, playfair_button, base32_button, exit_button)
    bot.send_message(message.chat.id, 'Выберите шифр:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Шифр Цезаря', 'Квадрат Полибия', 'Таблица Трисемуса', 'Биграммный шифр Плейфера', '32-ричная система счисления'])
def show_cipher_info(message):
    if message.text == 'Шифр Цезаря':
        bot.send_message(message.chat.id, 'Шифр Цезаря - это шифр замены, При шифровке все буквы смещаются на 2 вперёд. Пример: А -> В. При расшифрове все буквы смещаются на 2 назад. Пример: В -> А.')
    elif message.text == 'Квадрат Полибия':
        text = "Квадрат Полибия - это метод шифрования, основанный на замене каждой буквы алфавита на координаты ее положения в квадратной таблице. Ниже представлена таблица для расшифровки."
        photo = open('C:/Users/Пользователь/OneDrive/Рабочий стол/Проект Хакатон июнь 2024___/1-1.PNG', 'rb')
        bot.send_message(message.chat.id, text)
        bot.send_photo(message.chat.id, photo)
    elif message.text == 'Таблица Трисемуса':
        bot.send_message(message.chat.id, 'Таблица Трисемуса - это шифр замены, где каждый символ текста заменяется символом, стоящим на пересечении строк и столбцов таблицы(пока что не реализовано).')
    elif message.text == 'Биграммный шифр Плейфера':
        bot.send_message(message.chat.id, 'Биграммный шифр Плейфера - это шифр замены, где каждый символ текста заменяется символом, стоящим на пересечении строк и столбцов таблицы(пока что не реализовано).')
    elif message.text == '32-ричная система счисления':
        bot.send_message(message.chat.id, '32-ричная система счисления - это шифр замены, каждая буква в слове сопоставляется с кодировкой в 32 ричной системе счислениярусские буквы к символам из 32 ричной системы счисления А-0 Б-1 В-2 Г-3 Д-4 Е-5 Ж-6 З-7 И-8 Й-9 К-A Л-B М-C Н-D О-E П-F Р-G С-H Т-I У-J Ф-K Х-L Ц-M Ч-N Ш-O Щ-P Ъ-Q Ы-R Ь-S Э-T Ю-U Я-V и закодированное слово на русском будет преобразовываться в кодировку из символов в 32 ричной системе счисления, а уже кодировка из 32 ричной будет преобразовываться в число в привычной нам десятеричной системе счислениянапример слово РУБЛЬ в промежуточном состоянии (символах из 32 ричной системы счисления) будет выглядеть как GJ1BS а в конечном зашифрованные виде (в десятеричной системе счисления) будет выглядеть как 17401212.')

@bot.message_handler(func=lambda message: message.text == 'Выход')
def exit_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('Старт')
    ciphers_button = types.KeyboardButton('Шифры')
    markup.add(start_button, ciphers_button)
    bot.send_message(message.chat.id, 'Вы вернулись в главное меню.', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Старт')
def start_game(message):
    global current_level, current_word, skips, hints
    current_level = 1
    current_word = random.choice(words[f'level{current_level}'])
    cipher = random.choice(list(ciphers.keys()))
    encrypted_word = ciphers[cipher](current_word)
    markup = types.InlineKeyboardMarkup()
    tip_button = types.InlineKeyboardButton('Подсказка', callback_data='tip')
    exit_button = types.InlineKeyboardButton('Выход', callback_data='exit')
    skip_button = types.InlineKeyboardButton('Пропуск', callback_data='skip')
    markup.add(tip_button)
    markup.add(skip_button)
    markup.add(exit_button)
    bot.send_message(message.chat.id, f'Уровень {current_level}. Шифр: {cipher}. Зашифрованное слово: {encrypted_word}', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    global current_level, current_word, solved_words
    if message.text.lower() == current_word.lower():
        solved_words += 1
        bot.send_message(message.chat.id, 'Верно!')
        if solved_words == 1:
            current_level += 1
            solved_words = 0
            if current_level > 3:
                bot.send_message(message.chat.id, 'Поздравляем, вы выиграли! Игра окончена.')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                start_button = types.KeyboardButton('Старт')
                ciphers_button = types.KeyboardButton('Шифры')
                markup.add(start_button, ciphers_button)
                bot.send_message(message.chat.id, 'Вы вернулись в главное меню.', reply_markup=markup)
            else:
                current_word = random.choice(words[f'level{current_level}'])
                cipher = random.choice(list(ciphers.keys()))
                encrypted_word = ciphers[cipher](current_word)
                markup = types.InlineKeyboardMarkup()
                tip_button = types.InlineKeyboardButton('Подсказка', callback_data='tip')
                skip_button = types.InlineKeyboardButton('Пропуск', callback_data='skip')
                exit_button = types.InlineKeyboardButton('Выход', callback_data='exit')
                markup.add(tip_button)
                markup.add(skip_button)
                markup.add(exit_button)
                bot.send_message(message.chat.id, f'Уровень {current_level}. Шифр: {cipher}. Зашифрованное слово: {encrypted_word}', reply_markup=markup)
        else:
            current_word = random.choice(words[f'level{current_level}'])
            cipher = random.choice(list(ciphers.keys()))
            encrypted_word = ciphers[cipher](current_word)
            markup = types.InlineKeyboardMarkup()
            tip_button = types.InlineKeyboardButton('Подсказка', callback_data='tip')
            skip_button = types.InlineKeyboardButton('Пропуск', callback_data='skip')
            exit_button = types.InlineKeyboardButton('Выход', callback_data='exit')
            markup.add(tip_button)
            markup.add(skip_button)
            markup.add(exit_button)
            bot.send_message(message.chat.id, f'Уровень {current_level}. Шифр: {cipher}. Зашифрованное слово: {encrypted_word}', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неправильно. Попробуйте еще раз.')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global current_level, current_word , skips
    if call.data.startswith('next_level_'):
        level = int(call.data.split('_')[1])
        if level > current_level:
            current_level = level
            current_word = random.choice(words[f'level{current_level}'])
            cipher = random.choice(list(ciphers.keys()))
            encrypted_word = ciphers[cipher](current_word)
            markup = types.InlineKeyboardMarkup()
            tip_button = types.InlineKeyboardButton('Подсказка', callback_data='tip')
            markup.add(tip_button)
            bot.send_message(call.message.chat.id, f'Уровень {current_level}. Шифр: {cipher}. Зашифрованное слово: {encrypted_word}', reply_markup=markup)
    elif call.data == 'tip':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
        bot.send_message(call.message.chat.id, f'Правильный ответ: {current_word}')
    elif call.data == 'exit':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton('Старт')
        ciphers_button = types.KeyboardButton('Шифры')
        markup.add(start_button, ciphers_button)
        bot.send_message(call.message.chat.id, 'Вы вернулись в главное меню.', reply_markup=markup)
    elif call.data == 'skip':
        if skips > 0:
            skips -= 1
            bot.send_message(call.message.chat.id, f'У тебя осталось {skips} пропусков')
            current_word = random.choice(words[f'level{current_level}'])
            cipher = random.choice(list(ciphers.keys()))
            encrypted_word = ciphers[cipher](current_word)
            markup = types.InlineKeyboardMarkup()
            tip_button = types.InlineKeyboardButton('Подсказка', callback_data='tip')
            skip_button = types.InlineKeyboardButton('Пропуск', callback_data='skip')
            exit_button = types.InlineKeyboardButton('Выход', callback_data='exit')
            markup.add(tip_button)
            markup.add(skip_button)
            markup.add(exit_button)
            bot.send_message(call.message.chat.id, f'Уровень {current_level}. Шифр: {cipher}. Зашифрованное слово: {encrypted_word}', reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, 'У тебя больше не осталось пропусков')

def base32_encrypt(word):
    russian_alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    base32_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
    base32_code = ''

    for char in word.upper():
        index = russian_alphabet.index(char)
        base32_code += base32_alphabet[index]
    decimal_code = int(base32_code, 32)
    return decimal_code

def caesar_cipher(text, shift = 2):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 1040 if char.isupper() else 1072
            result += chr((ord(char) - ascii_offset + shift) % 33 + ascii_offset)
        else:
            result += char
    return result

polybius_table = [
    ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З'],
    ['И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П'],
    ['Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч'],
    ['Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
]

def polybius_square_cipher(text):
    result = ''
    for char in text:
        for i, row in enumerate(polybius_table):
            for j, cell in enumerate(row):
                if char == cell:
                    result += str(i+1) + str(j+1)
                    break
    return f'{result}'

ciphers = {
    'Шифр Цезаря': caesar_cipher,
    'Квадрат Полибия': polybius_square_cipher,
    #'Таблица Трисемуса': base32_encrypt,
    #'Полиабинский квадрат': polybius_square_cipher,
    '32 система исчисления': base32_encrypt,
    #'Биграммный шифр Плейфера': caesar_cipher
}

words = {
    'level1': ['РУБЛЬ', 'БАНАН', 'ЭФФЕКТИВНОСТЬ','МАТЬ','ПОТОЛОК','СТОЛЕШНИЦА','КОМПЬЮТЕР','СТЕНА','САМОЛЕТ','НЕВЕРОЯТНО','ТЕТРАДЬ'],  # слова для первого уровня
    'level2': ['КОРПУС', 'МИР', 'ОБНОВЛЕНИЕ','ФУТБОЛКА','ОПАЗДЫВАТЬ','ОБЛАКО','ЕДИНИЦА','ВРЕМЯ','СУФФИКС','ПРЕДЛОЖЕНИЕ','СИСТЕМА'],  # слова для второго уровня
    'level3': ['ГОРОСКОП', 'АБРИКОС', 'РЕГИСТРАЦИЯ','ТЕЛЕФОН','ОДИННАДЦАТИКЛАССНИК','НОУТБУК','МОНИТОР','СТАКАН','СОЕДИНЕНИЕ','МАНДАРИН','ЛОШАДЬ','ГИДРОКАРБОНАТ']  # слова для третьего уровня
}

bot.polling()

            