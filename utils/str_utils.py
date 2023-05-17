from fuzzywuzzy import fuzz


def remove_turkish_chars(word):
    return (
        word
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

    return (similarity_ratio + partial_ratio + token_sort_ratio + token_set_ratio) / 4
