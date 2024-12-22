phoneme_map = {
    # Vowels
    'అ': 'a', 'ఆ': 'aa', 'ఇ': 'i', 'ఈ': 'ee', 'ఉ': 'u', 'ఊ': 'oo',
    'ఋ': 'ru', 'ౠ': 'ruu', 'ఎ': 'e', 'ఏ': 'ee', 'ఐ': 'ai', 'ఒ': 'o', 'ఓ': 'oo', 'ఔ': 'au',

    # Consonants
    'క': 'ka', 'ఖ': 'kha', 'గ': 'ga', 'ఘ': 'gha', 'ఙ': 'nga',
    'చ': 'cha', 'ఛ': 'chha', 'జ': 'ja', 'ఝ': 'jha', 'ఞ': 'nya',
    'ట': 'ṭa', 'ఠ': 'ṭha', 'డ': 'ḍa', 'ఢ': 'ḍha', 'ణ': 'ṇa',
    'త': 'ta', 'థ': 'tha', 'ద': 'dha', 'ధ': 'dhha', 'న': 'na',
    'ప': 'pa', 'ఫ': 'pha', 'బ': 'ba', 'భ': 'bha', 'మ': 'ma',
    'య': 'ya', 'ర': 'ra', 'ల': 'la', 'వ': 'va', 'శ': 'sha',
    'ష': 'ssa', 'స': 'sa', 'హ': 'ha', 'ళ': 'lla', 'ం': 'm', 'ః': 'h',

    # Vowel diacritics
    'ా': 'aa', 'ి': 'i', 'ీ': 'ee', 'ు': 'u', 'ూ': 'oo', 'ృ': 'ru', 'ౄ': 'ruu',
    'ె': 'e', 'ే': 'ee', 'ై': 'ai', 'ొ': 'o', 'ో': 'oo', 'ౌ': 'au',

    # Virama (indicates the absence of a vowel)
    '్': '',

    # Additional mappings for consonants and their combinations can be added here
}

def text_to_phonemes(text):
    """
    Convert Telugu text to phonemes based on the phoneme_map.

    Parameters:
    text (str): The input text in Telugu.

    Returns:
    list: A list containing phonetic representations of each word.
    """
    result = []
    word = []
    i = 0
    while i < len(text):
        # Check if two characters together form a valid phoneme combination
        if i + 1 < len(text) and text[i:i+2] in phoneme_map:
            phoneme = phoneme_map[text[i:i+2]]
            word.append(phoneme)
            i += 2
        else:
            char = text[i]
            # Map individual characters, skipping characters not in the map
            if char in phoneme_map:
                phoneme = phoneme_map[char]
                word.append(phoneme)
            i += 1
        # Check for word boundary or end of text
        if i == len(text) or text[i] == ' ':
            if word:
                result.append(''.join(word))
                word = []
            if i < len(text) and text[i] == ' ':
                result.append(' ')
                i += 1

    return result

def process_text(text):
    """
    Process input text (single line or paragraph) and convert to phonemes.

    Parameters:
    text (str): The input text in Telugu.

    Returns:
    str: Phonetic representation of the entire text.
    """
    words = text.split(' ')
    phonetic_words = []

    for word in words:
        phonetic_word = text_to_phonemes(word)
        phonetic_words.append(''.join(phonetic_word))

    return ' '.join(phonetic_words)