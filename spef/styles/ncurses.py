from pygments.style import Style
from pygments.token import (
    Keyword,
    Name,
    Comment,
    String,
    Error,
    Text,
    Number,
    Operator,
    Generic,
    Whitespace,
    Punctuation,
    Other,
    Literal,
)


"""
* style for ncurses (similar to visual code colors)
* color is represented by number of curses.color_pair defined in utils/coloring.py
"""


class NcursesStyle(Style):

    """mapping to ncurses colors defined in coloring.py file"""

    HL_PURPLE = "#000040"
    HL_BLUE = "#000041"
    HL_LIGHT_BLUE = "#000042"
    HL_YELLOW = "#000043"
    HL_CYAN = "#000044"
    HL_GREEN = "#000045"
    HL_PASTEL_GREEN = "#000046"
    HL_ORANGE = "#000047"
    HL_RED = "#000048"
    HL_OLIVE = "#000049"
    HL_PINK = "#000050"

    HL_NORMAL = "#000055"

    default_style = HL_NORMAL

    # https://svn.python.org/projects/external/Pygments-1.3.1/docs/build/tokens.html
    # fmt: off
    styles = {
        Comment: HL_GREEN,
        Comment.Preproc: HL_PURPLE,
        Comment.Special: HL_NORMAL,
        Keyword: HL_BLUE,
        # Keyword.Constant:          "",
        # Keyword.Declaration:       "", # var
        Keyword.Namespace: HL_PURPLE,  # import, package
        # Keyword.Pseudo:            "",
        # Keyword.Reserved:          "",
        # Keyword.Type:              "", # int, char
        Name: HL_NORMAL,
        Name.Attribute: HL_YELLOW,
        Name.Builtin: HL_LIGHT_BLUE,  # self, this
        # Name.Builtin.Pseudo:       "",
        Name.Class: HL_CYAN,
        Name.Constant: HL_BLUE,  # const
        Name.Decorator: HL_YELLOW,
        # Name.Entity:               HL_LIGHT_BLUE,
        Name.Exception: HL_CYAN,
        Name.Function: HL_YELLOW,
        # Name.Label:                "",
        # Name.Namespace:            HL_LIGHT_BLUE, # import path or name folowing the module/namespace keyword
        Name.Other: HL_YELLOW,
        Name.Tag: HL_PURPLE,
        Name.Variable: HL_LIGHT_BLUE,
        Number: HL_PASTEL_GREEN,  # HL_PINK
        Literal: HL_PASTEL_GREEN,  # HL_PINK
        Literal.Date: HL_ORANGE,
        String: HL_ORANGE,
        String.Escape: HL_PASTEL_GREEN,  # HL_PINK
        String.Interpol: HL_BLUE,
        Text: HL_NORMAL,
        Operator: HL_NORMAL,
        Operator.Word: HL_BLUE,
        Punctuation: HL_NORMAL,
        Error: HL_RED,
        Generic.Deleted: HL_PURPLE,
        Generic.Inserted: HL_YELLOW,
        Generic.Output: HL_BLUE,
        Generic.Prompt: HL_PURPLE,
        Generic.Subheading: HL_PURPLE,
    }
