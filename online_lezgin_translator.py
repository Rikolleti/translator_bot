def load_vocabulary(file_path):
    vocab = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            russian, lezgin = line.strip().split(':')
            vocab[russian] = lezgin
    return vocab

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
            if original_word.lower() not in ('в', 'на'):  # Exclude the letter "в", "на"
                translated_words.append(vocab.get(original_word.lower(), original_word))
            i += 1
    translated_phrase = ' '.join(translated_words)
    return translated_phrase

# Пример использования
while True:
    input_text = input("Введите текст для перевода: ")
    if input_text.lower() in ('stop', 'стоп'):
        print("Программа завершена.")
        break
    lezgin_translation = translate_russian_to_lezgin(input_text)
    print(f"Перевод: {lezgin_translation}")
