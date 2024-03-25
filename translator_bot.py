import telebot

# Initialize your Telegram bot token
bot_token = "TOKEN"
bot = telebot.TeleBot(bot_token)

# Load vocabulary for translation
def load_vocabulary(file_path):
    vocab = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            russian, lezgin = line.strip().split(':')
            vocab[russian] = lezgin
    return vocab

# Translate Russian to Lezgin
def translate_russian_to_lezgin(input_text, vocab_file='lezgin_translate.txt'):
    vocab = load_vocabulary(vocab_file)
    input_text = input_text.replace(',', ' ')
    words = input_text.split()
    translated_words = []
    i = 0
    while i < len(words):
        # Check for one, two, and three-word phrases
        for phrase_length in range(4, 0, -1):
            phrase = ' '.join(words[i:i+phrase_length])
            if phrase.lower() in vocab:
                translated_words.append(vocab[phrase.lower()])
                i += phrase_length  # Skip the next words
                break
        else:
            # Use original word if not found
            original_word = words[i]
            if original_word.lower() not in ('в', 'на'):  # Exclude the letter "в"
                translated_words.append(vocab.get(original_word.lower(), original_word))
            i += 1
    translated_phrase = ' '.join(translated_words)
    return translated_phrase

def translate_russian_to_avar(input_text, vocab_file='avar_translate.txt'):
    vocab = load_vocabulary(vocab_file)
    input_text = input_text.replace(',', ' ')
    words = input_text.split()
    translated_words = []
    i = 0
    while i < len(words):
        # Check for one, two, and three-word phrases
        for phrase_length in range(4, 0, -1):
            phrase = ' '.join(words[i:i+phrase_length])
            if phrase.lower() in vocab:
                translated_words.append(vocab[phrase.lower()])
                i += phrase_length  # Skip the next words
                break
        else:
            # Use original word if not found
            original_word = words[i]
            if original_word.lower() not in ('в', 'на'):  # Exclude the letter "в"
                translated_words.append(vocab.get(original_word.lower(), original_word))
            i += 1
    translated_phrase = ' '.join(translated_words)
    return translated_phrase

# Dictionary to store user states
user_states = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_states[message.chat.id] = "start"
    user_first_name = message.from_user.first_name
    welcome_message = f"Добрый день, {user_first_name}!\nВас приветствует бот ДагоЛинго-Переводчик. 📚\n\nВыберите язык на который вы хотите перевести русский текст:"
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Лезгинский", "Аварский", "Кумыкский (в разработке)", "Даргинский (в разработке)", "Лакский (в разработке)")
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Лезгинский", "Аварский", "Кумыкский (в разработке)", "Даргинский (в разработке)", "Лакский (в разработке)"])
def handle_language_selection(message):
    selected_language = message.text
    user_states[message.chat.id] = selected_language
    if selected_language == "Лезгинский":
        bot.send_message(message.chat.id, f"Вы выбрали {selected_language}.\nТеперь введите текст для перевода:")
    elif selected_language == "Аварский":
        bot.send_message(message.chat.id, f"Вы выбрали {selected_language}.\nТеперь введите текст для перевода:")
    else:
        bot.send_message(message.chat.id, "В разработке")  # Output "В разработке" for unsupported languages
        user_states[message.chat.id] = "start"  # Reset user state to start

# Handle user input for translation
@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id] != "start")
def handle_translation_input(message):
    input_text = message.text.lower()  # Convert input to lowercase for case-insensitivity
    selected_language = user_states[message.chat.id]
    
    if input_text in ["стоп", "stop"]:
        # Exit the loop if 'стоп' or 'stop' is entered
        bot.send_message(message.chat.id, "Перевод остановлен. До свидания!")
        user_states[message.chat.id] = "start"  # Reset user state to start
        return

    if selected_language == "Лезгинский":
        lezgin_translation = translate_russian_to_lezgin(input_text)
        bot.send_message(message.chat.id, f"Перевод: {lezgin_translation}")

    if selected_language == "Аварский":
        avar_translation = translate_russian_to_avar(input_text)
        bot.send_message(message.chat.id, f"Перевод: {avar_translation}")

# Start the bot
bot.polling()