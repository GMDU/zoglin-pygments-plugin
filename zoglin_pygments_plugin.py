"""Zoglin lexer plugin"""

from pygments.lexer import RegexLexer, words, include, using
from pygments.lexers.minecraft import MCFunctionLexer
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
            (r'#.*', Comment),
            (
              words(
                ("namespace", "module", "fn", "res", "asset"),
                suffix = r'\b'
              ),
              Keyword.Declaration
            ),
            (
              words(
                ("include", "import", "as", "if", "else", "while", "return", "break", "continue"),
                suffix = r'\b'
              ),
              Keyword
            ),
            include("literals"),
            include("commands"),
            (r'(?<=namespace) *\w+', Name.Namespace),
            (r'(?<=module) *\w+', Name.Class),
            (r'[$&@%]?(\w+:|:|~)?[\w\/]+(?=\s*\()', Name.Function),
            (r'[$&@%]?(\w+:|:|~)?[\w\/]+:?', Name.Variable),
            (r'[{}()\[\]]', Punctuation),
        ],
        "commands": [
          (
            r'^\s*(advancement|attribute|bossbar|clear|clone|damage|data|datapack|difficulty|effect|enchant|execute|experience|fill|fillbiome|forceload|function|gamemode|gamerule|give|item|kill|loot|particle|place|playsound|random|recipe|reload|ride|say|schedule|scoreboard|setblock|setworldspawn|spawnpoint|spectate|spreadplayers|stopsound|summon|tag|team|teleport|tellraw|time|title|tp|trigger|weather|worldborder|xp)\b.+',
            using(MCFunctionLexer)
          ),
          (
            r'(?<=\/).+',
            using(MCFunctionLexer)
          )
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
