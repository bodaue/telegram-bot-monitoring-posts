import difflib

import pymorphy2


def replace_str_index(text: str,
                      index: int = 0,
                      replacement: str = '') -> str:
    return '%s%s%s' % (text[:index], replacement, text[index + 1:])


def check_difference(string_1: str,
                     string_2: str) -> tuple[str, str]:
    for i, s in reversed(list(enumerate([i for i in difflib.ndiff(string_1, string_2) if i[0] == '-' or i[0] == ' ']))):
        if s[0] == '-':
            string_1 = replace_str_index(text=string_1, index=i, replacement='<s>' + s[-1] + '</s>')

    for i, s in reversed(list(enumerate([i for i in difflib.ndiff(string_1, string_2) if i[0] == '+' or i[0] == ' ']))):
        if s[0] == '+':
            string_2 = replace_str_index(text=string_2, index=i, replacement='<u>' + s[-1] + '</u>')
    return string_1, string_2


morph = pymorphy2.MorphAnalyzer()
word_cases = {
    "nomn": "иминительный",
    "gent": "родительный",
    "datv": "дательный",
    "accs": "винительный",
    "ablt": "творительный",
    "loct": "предложный",
    "voct": "звательный",
    "gen2": "второй родительный",
    "acc2": "второй винительный",
    "loc2": "второй предложный"
}


def get_word_cases(word: str) -> list[str]:
    return_list = []
    try:
        form = morph.parse(word)[0]
        for case in word_cases:
            return_list.append(form.inflect({case})[0])
        return return_list
    except TypeError:
        return_list.append(word)
        return return_list


async def notify_users(chat_id: int,
                       message_id: int) -> None:
    pass
