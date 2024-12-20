import pathlib
from ipa.ipa import BanglaIPATranslator

path = pathlib.Path(__file__).absolute().parents[1] / "model/ipa_model.pth"


def ipa_checker(word):
    """
    Performs IPA checking with the model.

    Params:
        word (str): Bengali word for IPA checking.

    Returns:
        None
    """
    ipa = BanglaIPATranslator(path)
    ipa_translated = ipa.translate(word)
    print(ipa_translated)

#
# ipa = ipa_checker("চাষাবাদ")
# ipa2 = ipa_checker("মহারাজ\n")
# ipa3 = ipa_checker("সম্প্রতি\n")
# ipa4 = ipa_checker("ভারকেন্দ্র\n")
# ipa5 = ipa_checker("কথায়\n")
# print(ipa2)
# print(ipa, ipa2, ipa3, ipa4, ipa5)
