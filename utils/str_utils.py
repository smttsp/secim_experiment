from fuzzywuzzy import fuzz


def replace_turkish_chars(word):
    return (
        word.lower()
        .replace("ç", "c")
        .replace("ğ", "g")
        .replace("ö", "o")
        .replace("ş", "s")
        .replace("ü", "u")
        .replace("ı", "i")
    )


def string_matching(word, target):
    similarity_ratio = fuzz.ratio(word, target)
    partial_ratio = fuzz.partial_ratio(word, target)
    token_sort_ratio = fuzz.token_sort_ratio(word, target)
    token_set_ratio = fuzz.token_set_ratio(word, target)

    return (similarity_ratio + partial_ratio + token_sort_ratio + token_set_ratio) / 4 / 100.0


def get_number_from_digits(value):
    if value.replace(" ", "").isdigit():
        res = int(value)
    elif value == "":
        res = -1
    else:
        res = -2
    return res


from utils.turkish_numbers import NUMBERS, NUMBERS_wo_SPACE


def get_number_from_string(value, numbers=NUMBERS, numbers_wo_space=NUMBERS_wo_SPACE):
    prev_best = 0
    best_key = -1
    for k, v in numbers.items():
        max_corr = string_matching(value, v)
        # max(string_matching(value, v), string_matching(value, numbers_wo_space[k]))
        if max_corr > prev_best:
            prev_best = max_corr
            best_key = k
    if prev_best < 0.1:
        best_key = -1

    return best_key


def get_number(format, value):
    if format == "rakamla":
        res = get_number_from_digits(value)
    elif format == "yaziyla":
        res = get_number_from_string(value)
    else:
        res = -3
    return res
