"""Zoglin lexer plugin"""

from pygments.lexer import RegexLexer, words, include
from pygments.token import Keyword, Text, Comment, Name,\
  Punctuation, Operator, Number, String

class ZoglinLexer(RegexLexer):
    name = "Zoglin Datapack Language"
    url = "https://zoglin.dev/"
    aliases = ["zoglin", "zog"]
    filenames = ["*.zog"]
    mimetypes = ["text/zoglin"]

    tokens = {
        'root': [
            # Resource location
            (r'#.+', Comment),
            (
              words(("namespace", "module", "fn",
                "if", "else", "while"),
                suffix = r'\b'
              ),
              Keyword
            ),
            include("literals"),
            (r'(?<=namespace) *\w+', Name.Namespace),
            (r'(?<=module) *\w+', Name.Class),
            (r'[$&@]?(\w+:|:|~)?[\w\/\-]+:?', Name.Variable),
            (r'[{}()\[\]]', Punctuation),
        ],
        "literals": [
            (r"(true|false)", Keyword.Constant),
            (r"-?\d+[eE]-?\d+", Number.Float),
            (r"-?\d*\.\d+[fFdD]?", Number.Float),
            (r"-?\d+[bBsSlLfFdD]?", Number.Integer),

            # Separate states for both types of strings so they don't entangle
            (r'"', String.Double, "literals.string_double"),
            (r"'", String.Single, "literals.string_single"),
        ],
        "literals.string_double": [
            (r"\\.", String.Escape),
            (r'[^\\"\n]+', String.Double),
            (r'"', String.Double, "#pop"),
        ],
        "literals.string_single": [
            (r"\\.", String.Escape),
            (r"[^\\'\n]+", String.Single),
            (r"'", String.Single, "#pop"),
        ],
    }
