def is_kanji(character):
    return any([ord(u"\u4e00") <= ord(character) <= ord(u"\u9faf")])


def is_cjk(character):
    """"
    Checks whether character is CJK.

        >>> is_cjk(u'\u33fe')
        True
        >>> is_cjk(u'\uFE5F')
        False

    :param character: The character that needs to be checked.
    :type character: char
    :return: bool
    """
    return any([start <= ord(character) <= end for start, end in
                [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215),
                 (63744, 64255), (65072, 65103), (65381, 65500),
                 (131072, 196607)]
                ])


class CJKChars(object):
    """
    An object that enumerates the code points of the CJK characters as listed on
    http://en.wikipedia.org/wiki/Basic_Multilingual_Plane#Basic_Multilingual_Plane

    This is a Python port of the CJK code point enumerations of Moses tokenizer:
    https://github.com/moses-smt/mosesdecoder/blob/master/scripts/tokenizer/detokenizer.perl#L309
    """
    # Hangul Jamo (1100–11FF)
    Hangul_Jamo = (4352, 4607) # (ord(u"\u1100"), ord(u"\u11ff"))

    # CJK Radicals Supplement (2E80–2EFF)
    # Kangxi Radicals (2F00–2FDF)
    # Ideographic Description Characters (2FF0–2FFF)
    # CJK Symbols and Punctuation (3000–303F)
    # Hiragana (3040–309F)
    # Katakana (30A0–30FF)
    # Bopomofo (3100–312F)
    # Hangul Compatibility Jamo (3130–318F)
    # Kanbun (3190–319F)
    # Bopomofo Extended (31A0–31BF)
    # CJK Strokes (31C0–31EF)
    # Katakana Phonetic Extensions (31F0–31FF)
    # Enclosed CJK Letters and Months (3200–32FF)
    # CJK Compatibility (3300–33FF)
    # CJK Unified Ideographs Extension A (3400–4DBF)
    # Yijing Hexagram Symbols (4DC0–4DFF)
    # CJK Unified Ideographs (4E00–9FFF)
    # Yi Syllables (A000–A48F)
    # Yi Radicals (A490–A4CF)
    CJK_Radicals = (11904, 42191) # (ord(u"\u2e80"), ord(u"\ua4cf"))

    # Phags-pa (A840–A87F)
    Phags_Pa = (43072, 43135) # (ord(u"\ua840"), ord(u"\ua87f"))

    # Hangul Syllables (AC00–D7AF)
    Hangul_Syllables = (44032, 55215) # (ord(u"\uAC00"), ord(u"\uD7AF"))

    # CJK Compatibility Ideographs (F900–FAFF)
    CJK_Compatibility_Ideographs = (63744, 64255) # (ord(u"\uF900"), ord(u"\uFAFF"))

    # CJK Compatibility Forms (FE30–FE4F)
    CJK_Compatibility_Forms = (65072, 65103) # (ord(u"\uFE30"), ord(u"\uFE4F"))

    # Range U+FF65–FFDC encodes halfwidth forms, of Katakana and Hangul characters
    Katakana_Hangul_Halfwidth = (65381, 65500) # (ord(u"\uFF65"), ord(u"\uFFDC"))

    # Supplementary Ideographic Plane 20000–2FFFF
    Supplementary_Ideographic_Plane = (131072, 196607) # (ord(u"\U00020000"), ord(u"\U0002FFFF"))

    ranges = [Hangul_Jamo, CJK_Radicals, Phags_Pa, Hangul_Syllables,
              CJK_Compatibility_Ideographs, CJK_Compatibility_Forms,
              Katakana_Hangul_Halfwidth, Supplementary_Ideographic_Plane]
