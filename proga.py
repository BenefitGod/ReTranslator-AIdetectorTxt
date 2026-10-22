import os

def decode_text(input_file_path, output_file_path=None):
    """
    Преобразует текст из специального формата в обычный.
    ПРОБЕЛ -> обычный пробел ( )
    """
    
    replacements = {
        'ПРОБЕЛ': ' ',
        'ТОЧКА': '.',
        'ЗАПЯТАЯ': ',',
        'АБЗАЦ': '\n',
        'ТИРЕ': '\u2013',
        'СКОБКАОТКРЫВАЕТСЯ': '(',
        'СКОБКАЗАКРЫВАЕТСЯ': ')',
        'ДВОЕТОЧИЕ': ':',
        'ТОЧКАСЗАПЯТОЙ': ';',
        'ВОПРОСИТЕЛЬНЫЙЗНАК': '?',
        'ВОСКЛИЦАТЕЛЬНЫЙЗНАК': '!',
        'КАВЫЧКИ': '"',
        'ПРОЦЕНТ': '%',
        'НОМЕР': '#',
        'АМПЕРСАНД': '&',
        'ЗВЕЗДОЧКА': '*',
        'ПЛЮС': '+',
        'МИНУС': '-',
        'РАВНО': '=',
        'СЛЭШ': '/',
        'ОБРАТНЫЙСЛЭШ': '\\',
        'ВЕРТИКАЛЬНАЯЧЕРТА': '|',
        'МЕНЬШЕ': '<',
        'БОЛЬШЕ': '>',
        'КВАДРАТНЫЕСКОБКИОТКРЫВАЮТСЯ': '[',
        'КВАДРАТНЫЕСКОБКИЗАКРЫВАЮТСЯ': ']',
        'ФИГУРНЫЕСКОБКИОТКРЫВАЮТСЯ': '{',
        'ФИГУРНЫЕСКОБКИЗАКРЫВАЮТСЯ': '}',
    }

    if output_file_path is None:
        base = os.path.splitext(input_file_path)[0]
        output_file_path = f"{base}_decoded.txt"

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        text = infile.read()

    for marker, symbol in replacements.items():
        text = text.replace(marker, symbol)

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(text)

    print(f"Готово: {output_file_path}")
    return output_file_path


def encode_text(input_file_path, output_file_path=None):
    """
    Преобразует обычный текст в специальный формат.
    """

    replacements = {
        ' ': 'ПРОБЕЛ',
        '.': 'ТОЧКА',
        ',': 'ЗАПЯТАЯ',
        '\n': 'АБЗАЦ',
        '\u2013': 'ТИРЕ',
        '(': 'СКОБКАОТКРЫВАЕТСЯ',
        ')': 'СКОБКАЗАКРЫВАЕТСЯ',
        ':': 'ДВОЕТОЧИЕ',
        ';': 'ТОЧКАСЗАПЯТОЙ',
        '?': 'ВОПРОСИТЕЛЬНЫЙЗНАК',
        '!': 'ВОСКЛИЦАТЕЛЬНЫЙЗНАК',
        '"': 'КАВЫЧКИ',
        '%': 'ПРОЦЕНТ',
        '#': 'НОМЕР',
        '&': 'АМПЕРСАНД',
        '*': 'ЗВЕЗДОЧКА',
        '+': 'ПЛЮС',
        '-': 'МИНУС',
        '=': 'РАВНО',
        '/': 'СЛЭШ',
        '\\': 'ОБРАТНЫЙСЛЭШ',
        '|': 'ВЕРТИКАЛЬНАЯЧЕРТА',
        '<': 'МЕНЬШЕ',
        '>': 'БОЛЬШЕ',
        '[': 'КВАДРАТНЫЕСКОБКИОТКРЫВАЮТСЯ',
        ']': 'КВАДРАТНЫЕСКОБКИЗАКРЫВАЮТСЯ',
        '{': 'ФИГУРНЫЕСКОБКИОТКРЫВАЮТСЯ',
        '}': 'ФИГУРНЫЕСКОБКИЗАКРЫВАЮТСЯ',
    }

    if output_file_path is None:
        base = os.path.splitext(input_file_path)[0]
        output_file_path = f"{base}_encoded.txt"

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        text = infile.read()

    for symbol, marker in replacements.items():
        text = text.replace(symbol, marker)

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(text)

    print(f"Готово: {output_file_path}")
    return output_file_path


# ============================================================
# НАСТРОЙКИ - укажи нужные пути здесь
# ============================================================

# Выбери режим: "decode" или "encode"
MODE = "decode"

# Укажи путь к входному файлу
INPUT_FILE = "d.txt"

# Укажи путь к выходному файлу (или None для автоматического имени)
OUTPUT_FILE = None

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    if MODE == "decode":
        decode_text(INPUT_FILE, OUTPUT_FILE)
    elif MODE == "encode":
        encode_text(INPUT_FILE, OUTPUT_FILE)
    else:
        print("Ошибка: MODE должен быть 'decode' или 'encode'")