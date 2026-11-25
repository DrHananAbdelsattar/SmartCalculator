# -*- coding: utf-8 -*-
"""
Smart Calculator: advanced bilingual calculator (Arabic / English)
- wxPython GUI
- Two text boxes: input and output (result)
- Shortcuts: Ctrl+E -> input box, Ctrl+R -> result box, Enter -> calculate,
             Ctrl+Enter -> calculate, Ctrl+L -> clear, Ctrl+B -> backspace,
             F1 or '?' -> help
- Accessibility: custom wx.Accessible for every control (screen readers)
- Settings: language, light/dark/high-contrast themes, colourblind-safe
  colours, font size -- all saved to a JSON config file.
"""
import wx
import math
import os
import json

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_CONFIG = {
    'lang': 'en',          # 'en' | 'ar'
    'theme': 'light',      # 'light' | 'dark' | 'highcontrast'
    'colorscheme': 'default',   # 'default' | 'colorblind'
    'fontsize': 'normal',  # 'normal' | 'large' | 'xlarge'
}

CFG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "calculator_settings.json")


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    try:
        with open(CFG_PATH, 'r', encoding='utf-8') as f:
            cfg.update(json.load(f))
    except Exception:
        pass
    return cfg


def save_config(cfg):
    try:
        with open(CFG_PATH, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------
I18N = {
    'en': {
        'app.about': "Smart Calculator - Python + wxPython",
        'title': "Smart Calculator",
        'status': ("Input box: type digits and operators.\n"
                   "Enter = calculate, Esc = clear, Ctrl+E = input, "
                   "Ctrl+R = result, F1 = help."),
        'in_name': "Input box",
        'in_desc': "Type numbers and operators here. Press Enter to calculate.",
        'out_name': "Result box",
        'out_desc': "Shows the calculation result.",
        'menu.file': "&File",
        'menu.exit': "E&xit",
        'menu.settings': "&Settings",
        'menu.language': "&Language",
        'menu.lang.en': "English",
        'menu.lang.ar': "Arabic (\u0627\u0644\u0639\u0631\u0628\u064a\u0629)",
        'menu.theme': "&Theme",
        'menu.theme.light': "Light",
        'menu.theme.dark': "Dark",
        'menu.theme.high': "High Contrast",
        'menu.colors': "&Colours",
        'menu.colors.std': "Standard",
        'menu.colors.cb': "Colour-blind friendly",
        'menu.font': "&Font Size",
        'menu.font.normal': "Normal",
        'menu.font.large': "Large",
        'menu.font.xlarge': "Extra Large",
        'menu.help_menu': "&Help",
        'menu.help': "&Help\tF1",
        'menu.about': "&About",
        'names': {
            'C': "Clear",
            'BSPC': "Backspace",
            'PCT': "Percent",
            'DIV': "Divide",
            'MUL': "Multiply",
            'SUB': "Subtract",
            'ADD': "Add",
            'EQUALS': "Equals",
            'DOT': "Decimal point",
            'SIGN': "Toggle sign",
            'SIN': "Sine",
            'COS': "Cosine",
            'TAN': "Tangent",
            'SQRT': "Square root",
            'SQUARE': "Square",
            'INV': "Reciprocal",
            'LPAREN': "Open parenthesis",
            'RPAREN': "Close parenthesis",
            'MC': "Memory clear",
            'MR': "Memory recall",
            'MP': "Memory add",
            'MS': "Memory subtract",
        },
        'descs': {
            'C': "Clear the input and the result",
            'BSPC': "Delete the last character",
            'PCT': "Percent, divide by one hundred",
            'DIV': "Division",
            'MUL': "Multiplication",
            'SUB': "Subtraction",
            'ADD': "Addition",
            'EQUALS': "Calculate the result",
            'DOT': "Decimal point",
            'SIGN': "Toggle the sign of the value",
            'SIN': "Sine, in degrees",
            'COS': "Cosine, in degrees",
            'TAN': "Tangent, in degrees",
            'SQRT': "Square root",
            'SQUARE': "Square the current value",
            'INV': "Reciprocal, one divided by the value",
            'LPAREN': "Opening parenthesis",
            'RPAREN': "Closing parenthesis",
            'MC': "Clear memory",
            'MR': "Recall memory into the input",
            'MP': "Add the value to memory",
            'MS': "Subtract the value from memory",
        },
        'errors': {
            'char': "Invalid character",
            'zero': "Division by zero",
            'expr': "Invalid expression",
            'func': "Unknown function",
            'paren': "Missing closing parenthesis",
        },
        'help': (
            "How to use the calculator:\n\n"
            "- Input box: type digits and operators.\n"
            "- Result box: shows the answer.\n"
            "- 2+3*4 = 14  (multiplication before addition)\n"
            "- % divides by one hundred: 50% = 0.5\n"
            "- sin/cos/tan use degrees: sin(30) = 0.5\n"
            "- x\u00b2, \u221a, and 1/x act on the current value.\n\n"
            "Shortcuts:\n"
            "  Enter / Ctrl+Enter ... Calculate (Result box)\n"
            "  Ctrl+E ................ go to Input box\n"
            "  Ctrl+R ................ go to Result box\n"
            "  Backspace ............. delete one character\n"
            "  Esc ................... clear everything\n"
            "  Ctrl+L ................ clear\n"
            "  Ctrl+B ................ backspace\n"
            "  F1 or ? ............... this help\n\n"
            "Settings menu: language, theme, colours, font size."
        ),
        'about': (
            "Smart Calculator\n\n"
            "Built with Python and wxPython.\n"
            "Accessible for screen readers, with light / dark /\n"
            "high-contrast themes and colour-blind safe colours.\n\n"
            "Version 2.0"
        ),
        'press': "Press",
    },
    'ar': {
        'app.about': "\u062d\u0627\u0633\u0628\u0629 \u0630\u0643\u064a\u0629 - Python \u0648 wxPython",
        'title': "\u062d\u0627\u0633\u0628\u0629 \u0630\u0643\u064a\u0629",
        'status': ("\u0645\u0631\u0628\u0639 \u0627\u0644\u0625\u062f\u062e\u0627\u0644: \u0627\u0643\u062a\u0628 \u0627\u0644\u0623\u0631\u0642\u0627\u0645 \u0648\u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a.\n"
                   "Enter = \u0627\u0644\u062d\u0633\u0627\u0628\u060c Esc = \u0627\u0644\u0645\u0633\u062d\u060c "
                   "Ctrl+E = \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a\u060c Ctrl+R = \u0627\u0644\u0646\u062a\u064a\u062c\u0629\u060c F1 = \u0645\u0633\u0627\u0639\u062f\u0629."),
        'in_name': "\u0645\u0631\u0628\u0639 \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a",
        'in_desc': "\u0627\u0643\u062a\u0628 \u0627\u0644\u0623\u0631\u0642\u0627\u0645 \u0648\u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a \u0647\u0646\u0627\u060c \u062b\u0645 \u0627\u0636\u063a\u0637 Enter \u0644\u0644\u062d\u0633\u0627\u0628.",
        'out_name': "\u0645\u0631\u0628\u0639 \u0627\u0644\u0646\u062a\u064a\u062c\u0629",
        'out_desc': "\u062a\u0638\u0647\u0631 \u0646\u062a\u064a\u062c\u0629 \u0627\u0644\u062d\u0633\u0627\u0628 \u0647\u0646\u0627.",
        'menu.file': "\u0645\u0644\u0641",
        'menu.exit': "\u062e\u0631\u0648\u062c",
        'menu.settings': "\u0627\u0644\u0625\u0639\u062f\u0627\u062f\u0627\u062a",
        'menu.language': "\u0627\u0644\u0644\u063a\u0629",
        'menu.lang.en': "\u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629",
        'menu.lang.ar': "\u0627\u0644\u0639\u0631\u0628\u064a\u0629",
        'menu.theme': "\u0646\u0645\u0637 \u0627\u0644\u0639\u0631\u0636",
        'menu.theme.light': "\u0641\u0627\u062a\u062d",
        'menu.theme.dark': "\u0645\u0638\u0644\u0645",
        'menu.theme.high': "\u062a\u0628\u0627\u064a\u0646 \u0639\u0627\u0644",
        'menu.colors': "\u0627\u0644\u0623\u0644\u0648\u0627\u0646",
        'menu.colors.std': "\u0627\u0644\u0623\u0633\u0627\u0633\u064a",
        'menu.colors.cb': "\u0645\u0646\u0627\u0633\u0628 \u0644\u0636\u0639\u0641 \u062a\u0645\u064a\u064a\u0632 \u0627\u0644\u0623\u0644\u0648\u0627\u0646",
        'menu.font': "\u062d\u062c\u0645 \u0627\u0644\u062e\u0637",
        'menu.font.normal': "\u0639\u0627\u062f\u064a",
        'menu.font.large': "\u0643\u0628\u064a\u0631",
        'menu.font.xlarge': "\u0643\u0628\u064a\u0631 \u062c\u062f\u0627",
        'menu.help_menu': "\u0645\u0633\u0627\u0639\u062f\u0629",
        'menu.help': "\u0645\u0633\u0627\u0639\u062f\u0629",
        'menu.about': "\u062d\u0648\u0644",
        'names': {
            'C': "\u0645\u0633\u062d \u0627\u0644\u0643\u0644",
            'BSPC': "\u0645\u0633\u062d \u0622\u062e\u0631 \u062d\u0631\u0641",
            'PCT': "\u0627\u0644\u0646\u0633\u0628\u0629 \u0627\u0644\u0645\u0626\u0648\u064a\u0629",
            'DIV': "\u0627\u0644\u0642\u0633\u0645\u0629",
            'MUL': "\u0627\u0644\u0636\u0631\u0628",
            'SUB': "\u0627\u0644\u0637\u0631\u062d",
            'ADD': "\u0627\u0644\u062c\u0645\u0639",
            'EQUALS': "\u0627\u0644\u062d\u0633\u0627\u0628",
            'DOT': "\u0627\u0644\u0641\u0627\u0635\u0644\u0629 \u0627\u0644\u0639\u0634\u0631\u064a\u0629",
            'SIGN': "\u0639\u0643\u0633 \u0627\u0644\u0625\u0634\u0627\u0631\u0629",
            'SIN': "\u0627\u0644\u062c\u064a\u0628",
            'COS': "\u062c\u064a\u0628 \u0627\u0644\u062a\u0645\u0627\u0645",
            'TAN': "\u0627\u0644\u0638\u0644",
            'SQRT': "\u0627\u0644\u062c\u0630\u0631 \u0627\u0644\u062a\u0631\u0628\u064a\u0639\u064a",
            'SQUARE': "\u0627\u0644\u062a\u0631\u0628\u064a\u0639",
            'INV': "\u0627\u0644\u0645\u0642\u0644\u0648\u0628",
            'LPAREN': "\u0642\u0648\u0633 \u0641\u062a\u062d",
            'RPAREN': "\u0642\u0648\u0633 \u0625\u063a\u0644\u0627\u0642",
            'MC': "\u0645\u0633\u062d \u0627\u0644\u0630\u0627\u0643\u0631\u0629",
            'MR': "\u0627\u0633\u062a\u0631\u062c\u0627\u0639 \u0627\u0644\u0630\u0627\u0643\u0631\u0629",
            'MP': "\u0625\u0636\u0627\u0641\u0629 \u0644\u0644\u0630\u0627\u0643\u0631\u0629",
            'MS': "\u0637\u0631\u062d \u0645\u0646 \u0627\u0644\u0630\u0627\u0643\u0631\u0629",
        },
        'descs': {
            'C': "\u0645\u0633\u062d \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a \u0648\u0627\u0644\u0646\u062a\u064a\u062c\u0629",
            'BSPC': "\u062d\u0630\u0641 \u0622\u062e\u0631 \u062d\u0631\u0641",
            'PCT': "\u0627\u0644\u0646\u0633\u0628\u0629 \u0627\u0644\u0645\u0626\u0648\u064a\u0629\u060c \u0627\u0644\u0642\u0633\u0645\u0629 \u0639\u0644\u0649 \u0645\u0627\u0626\u0629",
            'DIV': "\u0627\u0644\u0642\u0633\u0645\u0629",
            'MUL': "\u0627\u0644\u0636\u0631\u0628",
            'SUB': "\u0627\u0644\u0637\u0631\u062d",
            'ADD': "\u0627\u0644\u062c\u0645\u0639",
            'EQUALS': "\u0627\u062d\u0633\u0628 \u0627\u0644\u0646\u062a\u064a\u062c\u0629",
            'DOT': "\u0627\u0644\u0641\u0627\u0635\u0644\u0629 \u0627\u0644\u0639\u0634\u0631\u064a\u0629",
            'SIGN': "\u0639\u0643\u0633 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0642\u064a\u0645\u0629",
            'SIN': "\u0627\u0644\u062c\u064a\u0628 \u0628\u0627\u0644\u062f\u0631\u062c\u0627\u062a",
            'COS': "\u062c\u064a\u0628 \u0627\u0644\u062a\u0645\u0627\u0645 \u0628\u0627\u0644\u062f\u0631\u062c\u0627\u062a",
            'TAN': "\u0627\u0644\u0638\u0644 \u0628\u0627\u0644\u062f\u0631\u062c\u0627\u062a",
            'SQRT': "\u0627\u0644\u062c\u0630\u0631 \u0627\u0644\u062a\u0631\u0628\u064a\u0639\u064a",
            'SQUARE': "\u062a\u0631\u0628\u064a\u0639 \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u062d\u0627\u0644\u064a\u0629",
            'INV': "\u0627\u0644\u0645\u0642\u0644\u0648\u0628\u060c \u0648\u0627\u062d\u062f \u0639\u0644\u0649 \u0627\u0644\u0642\u064a\u0645\u0629",
            'LPAREN': "\u0642\u0648\u0633 \u0641\u062a\u062d",
            'RPAREN': "\u0642\u0648\u0633 \u0625\u063a\u0644\u0627\u0642",
            'MC': "\u0645\u0633\u062d \u0627\u0644\u0630\u0627\u0643\u0631\u0629",
            'MR': "\u0627\u0633\u062a\u0631\u062c\u0627\u0639 \u0627\u0644\u0630\u0627\u0643\u0631\u0629 \u0641\u064a \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a",
            'MP': "\u0625\u0636\u0627\u0641\u0629 \u0627\u0644\u0642\u064a\u0645\u0629 \u0625\u0644\u0649 \u0627\u0644\u0630\u0627\u0643\u0631\u0629",
            'MS': "\u0637\u0631\u062d \u0627\u0644\u0642\u064a\u0645\u0629 \u0645\u0646 \u0627\u0644\u0630\u0627\u0643\u0631\u0629",
        },
        'errors': {
            'char': "\u062d\u0631\u0641 \u063a\u064a\u0631 \u0635\u0627\u0644\u062d",
            'zero': "\u0627\u0644\u0642\u0633\u0645\u0629 \u0639\u0644\u0649 \u0635\u0641\u0631",
            'expr': "\u062a\u0639\u0628\u064a\u0631 \u063a\u064a\u0631 \u0635\u0627\u0644\u062d",
            'func': "\u062f\u0627\u0644\u0629 \u063a\u064a\u0631 \u0645\u0639\u0631\u0648\u0641\u0629",
            'paren': "\u0642\u0648\u0633 \u0625\u063a\u0644\u0627\u0642 \u0646\u0627\u0642\u0635",
        },
        'help': (
            "\u0643\u064a\u0641 \u062a\u0633\u062a\u062e\u062f\u0645 \u0627\u0644\u062d\u0627\u0633\u0628\u0629:\n\n"
            "- \u0645\u0631\u0628\u0639 \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a: \u0627\u0643\u062a\u0628 \u0627\u0644\u0623\u0631\u0642\u0627\u0645 \u0648\u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a.\n"
            "- \u0645\u0631\u0628\u0639 \u0627\u0644\u0646\u062a\u064a\u062c\u0629: \u064a\u0638\u0647\u0631 \u0641\u064a\u0647 \u0627\u0644\u0646\u0627\u062a\u062c.\n"
            "- 2+3*4 = 14  (\u0627\u0644\u0636\u0631\u0628 \u0642\u0628\u0644 \u0627\u0644\u062c\u0645\u0639)\n"
            "- % \u064a\u0642\u0633\u0645 \u0639\u0644\u0649 \u0645\u0627\u0626\u0629: 50% = 0.5\n"
            "- \u0627\u0644\u062f\u0648\u0627\u0644 \u0628\u0627\u0644\u062f\u0631\u062c\u0627\u062a: sin(30) = 0.5\n"
            "- x\u00b2 \u0648 \u221a \u0648 1/x \u062a\u0639\u0645\u0644 \u0639\u0644\u0649 \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u062d\u0627\u0644\u064a\u0629.\n\n"
            "\u0627\u0644\u0627\u062e\u062a\u0635\u0627\u0631\u0627\u062a:\n"
            "  Enter \u0623\u0648 Ctrl+Enter ... \u0627\u0644\u062d\u0633\u0627\u0628 (\u0645\u0631\u0628\u0639 \u0627\u0644\u0646\u062a\u064a\u062c\u0629)\n"
            "  Ctrl+E ................ \u0627\u0644\u0627\u0646\u062a\u0642\u0627\u0644 \u0625\u0644\u0649 \u0645\u0631\u0628\u0639 \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a\n"
            "  Ctrl+R ................ \u0627\u0644\u0627\u0646\u062a\u0642\u0627\u0644 \u0625\u0644\u0649 \u0645\u0631\u0628\u0639 \u0627\u0644\u0646\u062a\u064a\u062c\u0629\n"
            "  Backspace ............. \u062d\u0630\u0641 \u062d\u0631\u0641\n"
            "  Esc ................... \u0645\u0633\u062d \u0627\u0644\u0643\u0644\n"
            "  Ctrl+L ................ \u0645\u0633\u062d\n"
            "  Ctrl+B ................ \u0645\u0633\u062d \u062d\u0631\u0641\n"
            "  F1 \u0623\u0648 ? ............... \u0647\u0630\u0647 \u0627\u0644\u0645\u0633\u0627\u0639\u062f\u0629\n\n"
            "\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u0625\u0639\u062f\u0627\u062f\u0627\u062a: \u0627\u0644\u0644\u063a\u0629 \u0648\u0627\u0644\u0646\u0645\u0637 \u0648\u0627\u0644\u0623\u0644\u0648\u0627\u0646 \u0648\u062d\u062c\u0645 \u0627\u0644\u062e\u0637."
        ),
        'about': (
            "\u062d\u0627\u0633\u0628\u0629 \u0630\u0643\u064a\u0629\n\n"
            "\u0628\u0646\u064a\u062a \u0628\u0640 Python \u0648 wxPython.\n"
            "\u0645\u062a\u0648\u0627\u0641\u0642\u0629 \u0645\u0639 \u0642\u0627\u0631\u0626\u0627\u062a \u0627\u0644\u0634\u0627\u0634\u0629\u060c \u0628\u0623\u0648\u0636\u0627\u0639\n"
            "\u0641\u0627\u062a\u062d \u0648\u0645\u0638\u0644\u0645 \u0648\u062a\u0628\u0627\u064a\u0646 \u0639\u0627\u0644\u060c \u0648\u0623\u0644\u0648\u0627\u0646\n"
            "\u0645\u0646\u0627\u0633\u0628\u0629 \u0644\u0636\u0639\u0627\u0641 \u062a\u0645\u064a\u064a\u0632 \u0627\u0644\u0623\u0644\u0648\u0627\u0646.\n\n"
            "\u0627\u0644\u0625\u0635\u062f\u0627\u0631 2.0"
        ),
        'press': "\u0627\u0636\u063a\u0637",
    },
}

# ---------------------------------------------------------------------------
# Themes and colour schemes (chosen to be safe for colour-blind users:
# no red/green pairs; high contrast)
# ---------------------------------------------------------------------------
THEMES = {
    'light': {
        'bg': '#e9edf2', 'fg': '#101418',
        'in_bg': '#ffffff', 'in_fg': '#101418',
        'out_bg': '#ffffff', 'out_fg': '#101418',
        'btn': '#f4f6f9', 'btnfg': '#101418',
        'op_btn': '#c9d4e0', 'op_fg': '#101418',
        'sb_bg': '#e9edf2', 'sb_fg': '#101418',
    },
    'dark': {
        'bg': '#18181c', 'fg': '#e8e8ea',
        'in_bg': '#212126', 'in_fg': '#e8e8ea',
        'out_bg': '#212126', 'out_fg': '#e8e8ea',
        'btn': '#2a2a30', 'btnfg': '#e8e8ea',
        'op_btn': '#3c3c46', 'op_fg': '#ffffff',
        'sb_bg': '#18181c', 'sb_fg': '#e8e8ea',
    },
    'highcontrast': {
        'bg': '#000000', 'fg': '#ffffff',
        'in_bg': '#000000', 'in_fg': '#ffffff',
        'out_bg': '#000000', 'out_fg': '#ffffff',
        'btn': '#000000', 'btnfg': '#ffffff',
        'op_btn': '#ffffff', 'op_fg': '#000000',
        'sb_bg': '#000000', 'sb_fg': '#ffffff',
    },
}

# Accent colours per (theme, colour-scheme). 'colorblind' uses an orange/blue
# palette that is distinguishable by people with deuteranopia/protanopia.
ACCENTS = {
    ('default', 'light'): '#0057b8',
    ('default', 'dark'): '#8ab4ff',
    ('default', 'highcontrast'): '#ffff00',
    ('colorblind', 'light'): '#e87722',
    ('colorblind', 'dark'): '#ffb454',
    ('colorblind', 'highcontrast'): '#ffff00',
}

FONT_SCALES = {
    'normal': 1.0,
    'large': 1.35,
    'xlarge': 1.8,
}

# Button visual kinds
DIGIT_TOKENS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
OP_TOKENS = {'DIV', 'MUL', 'SUB', 'ADD', 'EQUALS', 'PCT', 'SIGN'}
FUNC_TOKENS = {'SIN', 'COS', 'TAN', 'SQRT', 'SQUARE', 'INV',
               'LPAREN', 'RPAREN', 'MC', 'MR', 'MP', 'MS'}

BUTTON_LABELS = {
    'en': {'C': 'C', 'BSPC': '\u232b', 'PCT': '%', 'DIV': '\u00f7',
           'MUL': '\u00d7', 'SUB': '\u2212', 'ADD': '+', 'EQUALS': '=',
           'DOT': '.', 'SIGN': '\u00b1', 'SIN': 'sin', 'COS': 'cos',
           'TAN': 'tan', 'SQRT': '\u221a', 'SQUARE': 'x\u00b2',
           'INV': '1/x', 'LPAREN': '(', 'RPAREN': ')',
           'MC': 'MC', 'MR': 'MR', 'MP': 'M+', 'MS': 'M-\u200e'},
    'ar': {'C': '\u0645\u0633\u062d', 'BSPC': '\u232b', 'PCT': '%',
           'DIV': '\u00f7', 'MUL': '\u00d7', 'SUB': '\u2212', 'ADD': '+',
           'EQUALS': '=', 'DOT': '.', 'SIGN': '\u00b1', 'SIN': '\u062c\u064a\u0628',
           'COS': '\u062c\u062a\u0627', 'TAN': '\u0638\u0627', 'SQRT': '\u221a',
           'SQUARE': 'x\u00b2', 'INV': '1/x', 'LPAREN': '(', 'RPAREN': ')',
           'MC': 'MC', 'MR': 'MR', 'MP': 'M+', 'MS': 'M-'},
}

BUTTON_LAYOUT = [
    ['C', 'BSPC', 'PCT', 'DIV'],
    ['MC', 'MR', 'MP', 'MS'],
    ['LPAREN', 'RPAREN', 'SQRT', 'SQUARE'],
    ['SIN', 'COS', 'TAN', 'INV'],
    ['7', '8', '9', 'MUL'],
    ['4', '5', '6', 'SUB'],
    ['1', '2', '3', 'ADD'],
    ['SIGN', '0', 'DOT', 'EQUALS'],
]

# ---------------------------------------------------------------------------
# Safe expression evaluator (recursive descent parser).
# Error codes are translated through I18N.
# ---------------------------------------------------------------------------
class CalcError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _tokenize(s):
    i, n, toks = 0, len(s), []
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or c == '.':
            j = i
            while j < n and (s[j].isdigit() or s[j] == '.'):
                j += 1
            toks.append(('num', float(s[i:j])))
            i = j
        elif c.isalpha():
            j = i
            while j < n and s[j].isalpha():
                j += 1
            toks.append(('func', s[i:j].lower()))
            i = j
        elif c in '+-*/%()':
            toks.append((c, c))
            i += 1
        else:
            raise CalcError('char')
    toks.append(('end', ''))
    return toks


class _Parser:
    def __init__(self, s):
        self.toks = _tokenize(s)
        self.pos = 0

    def _peek(self):
        return self.toks[self.pos]

    def _next(self):
        t = self.toks[self.pos]
        self.pos += 1
        return t

    def _expect(self, ty, err):
        t = self._next()
        if t[0] != ty:
            raise CalcError(err)
        return t

    def evaluate(self):
        v = self._expr()
        if self._peek()[0] != 'end':
            raise CalcError('expr')
        return v

    def _expr(self):
        v = self._term()
        while self._peek()[0] in ('+', '-'):
            op = self._next()[0]
            r = self._term()
            v = v + r if op == '+' else v - r
        return v

    def _term(self):
        v = self._unary()
        while self._peek()[0] in ('*', '/', '%'):
            op = self._next()[0]
            if op == '%':
                v = v / 100.0
            elif op == '*':
                v *= self._unary()
            else:
                d = self._unary()
                if d == 0:
                    raise CalcError('zero')
                v /= d
        return v

    def _unary(self):
        if self._peek()[0] == '-':
            self._next()
            return -self._unary()
        return self._atom()

    def _atom(self):
        t = self._peek()
        if t[0] == 'num':
            self._next()
            return t[1]
        if t[0] == '(':
            self._next()
            v = self._expr()
            self._expect(')', 'paren')
            return v
        if t[0] == 'func':
            f = self._next()[1]
            self._expect('(', 'expr')
            arg = self._expr()
            self._expect(')', 'paren')
            funcs = {
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                'sqrt': math.sqrt,
                'log': math.log10,
                'ln': math.log,
            }
            if f not in funcs:
                raise CalcError('func')
            try:
                return funcs[f](arg)
            except (ValueError, ZeroDivisionError, OverflowError):
                raise CalcError('expr')
        raise CalcError('expr')


def evaluate(text):
    return _Parser(text).evaluate()


def format_number(v):
    if math.isnan(v) or math.isinf(v):
        return "Error"
    if v == int(v):
        return str(int(v))
    return format(v, '.10g')


# ---------------------------------------------------------------------------
# Accessibility
# ---------------------------------------------------------------------------
class NamedAccessible(wx.Accessible):
    def __init__(self, name, description, role=None, action=None,
                 click_cb=None):
        super().__init__()
        self._name = name
        self._description = description
        self._role = role
        self._action = action
        self._click_cb = click_cb

    def GetName(self, childId):
        if childId == wx.ACC_SELF:
            return (wx.ACC_OK, self._name)
        return (wx.ACC_NOT_IMPLEMENTED, "")

    def GetDescription(self, childId):
        if childId == wx.ACC_SELF:
            return (wx.ACC_OK, self._description)
        return (wx.ACC_NOT_IMPLEMENTED, "")

    def GetHelpText(self, childId):
        if childId == wx.ACC_SELF:
            return (wx.ACC_OK, self._description)
        return (wx.ACC_NOT_IMPLEMENTED, "")

    def GetRole(self, childId):
        if childId == wx.ACC_SELF and self._role is not None:
            return (wx.ACC_OK, self._role)
        return (wx.ACC_NOT_IMPLEMENTED, 0)

    def GetDefaultAction(self, childId):
        if childId == wx.ACC_SELF and self._action is not None:
            return (wx.ACC_OK, self._action)
        return (wx.ACC_NOT_IMPLEMENTED, "")

    def DoDefaultAction(self, childId):
        if childId == wx.ACC_SELF and self._click_cb is not None:
            self._click_cb()
            return wx.ACC_OK
        return wx.ACC_NOT_SUPPORTED


class ThemeButton(wx.Control):
    """Self-drawn button so themes/colours render on every platform
    (native wx.Button ignores colours on MSW). Fully keyboard accessible."""

    def __init__(self, parent, token, on_click, id=wx.ID_ANY):
        super().__init__(parent, id=id, size=wx.Size(-1, 46))
        self.token = token
        self._on_click = on_click
        self._label = ""
        self._name = ""
        self._desc = ""
        self._action_label = "Press"
        self._kind = 'digit'  # digit | op | func | equals
        self._fp = None      # (bg, fg, idle_border, focus_border)
        self._font = None
        self._hover = False
        self._pressed = False
        self._accessible = None

        self.SetMinSize(wx.Size(64, 46))

        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_down)
        self.Bind(wx.EVT_LEFT_UP, self._on_up)
        self.Bind(wx.EVT_ENTER_WINDOW, lambda e: self._set_hover(True))
        self.Bind(wx.EVT_LEAVE_WINDOW, lambda e: self._set_hover(False))
        self.Bind(wx.EVT_KILL_FOCUS, lambda e: self.Refresh())
        self.Bind(wx.EVT_SET_FOCUS, lambda e: self.Refresh())
        self.Bind(wx.EVT_CHAR, self._on_char)

    # ---------------------------------------------------------- public API
    def configure(self, label, name, desc, fp, font, action_label):
        self._label = label
        self._name = name
        self._desc = desc
        self._fp = fp
        self._font = font
        self._action_label = action_label
        self._accessible = NamedAccessible(
            name, desc, role=wx.ROLE_SYSTEM_PUSHBUTTON,
            action=action_label, click_cb=self._trigger)
        self.SetAccessible(self._accessible)
        self.SetToolTip(wx.ToolTip(desc))
        self.Refresh()

    def set_kind(self, kind):
        self._kind = kind

    def _trigger(self):
        if self._on_click:
            self._on_click(self.token)

    # ------------------------------------------------------------ internal
    def _set_hover(self, on):
        self._hover = on
        self.Refresh()

    def _on_down(self, evt):
        self._pressed = True
        self.CaptureMouse()
        self.Refresh()

    def _on_up(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        was = self._pressed
        self._pressed = False
        self.Refresh()
        pt = evt.GetPosition()
        if was and (0 <= pt.x <= self.GetSize().GetWidth()
                    and 0 <= pt.y <= self.GetSize().GetHeight()):
            self._trigger()

    def _on_char(self, evt):
        k = evt.GetKeyCode()
        if k in (wx.WXK_SPACE, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._trigger()
        else:
            evt.Skip()

    def _on_paint(self, evt):
        dc = wx.PaintDC(self)
        w, h = self.GetClientSize()

        if self._fp:
            base_bg, base_fg = self._fp[0], self._fp[1]
        else:
            base_bg, base_fg = wx.BLACK, wx.WHITE

        bg, fg = base_bg, base_fg

        if self._pressed:
            bg, fg = base_fg, base_bg

        pen = self._fp[2] if self._fp else bg
        if self.HasFocus():
            pen = self._fp[3] if self._fp else wx.WHITE

        dc.SetBrush(wx.Brush(bg))
        dc.SetPen(wx.Pen(pen, 2))
        dc.DrawRoundedRectangle(1, 1, max(0, w - 2), max(0, h - 2), 7)

        if self._font:
            dc.SetFont(self._font)
        dc.SetTextForeground(fg)
        tw, th = dc.GetTextExtent(self._label)
        dc.DrawText(self._label, max(1, (w - tw) // 2), max(1, (h - th) // 2))


class CalculatorFrame(wx.Frame):
    # --- menu / shortcut ids --------------------------------------------
    ID_EXIT = wx.ID_HIGHEST + 1
    ID_FOCUS_IN = ID_EXIT + 1
    ID_FOCUS_OUT = ID_EXIT + 2
    ID_EQUALS = ID_EXIT + 3
    ID_CLEAR = ID_EXIT + 4
    ID_BACKSPACE = ID_EXIT + 5
    ID_HELP = ID_EXIT + 6
    ID_ABOUT = ID_EXIT + 7

    ID_LANG_EN = ID_EXIT + 20
    ID_LANG_AR = ID_EXIT + 21

    ID_THEME_LIGHT = ID_EXIT + 30
    ID_THEME_DARK = ID_EXIT + 31
    ID_THEME_HIGH = ID_EXIT + 32

    ID_COLOR_STD = ID_EXIT + 40
    ID_COLOR_CB = ID_EXIT + 41

    ID_FONT_NORMAL = ID_EXIT + 50
    ID_FONT_LARGE = ID_EXIT + 51
    ID_FONT_XLARGE = ID_EXIT + 52

    def __init__(self):
        self.config = load_config()
        self.lang = self.config['lang']
        self._buttons = {}
        self._accessibles = []
        self._mem_value = 0.0
        super().__init__(None, title="", size=(360, 560))

        self.panel = wx.Panel(self)
        self._build_widgets()

        self._setup_shortcuts()
        self._bind_menu_handlers()
        self.CreateStatusBar()
        self._apply_config()

        self.Centre()
        wx.CallAfter(self.input.SetFocus)

    # ---------------------------------------------------------------- i18n
    def tr(self, key):
        return I18N[self.lang].get(key, key)

    def tr_names(self, token):
        return I18N[self.lang]['names'].get(token, token)

    def tr_descs(self, token):
        return I18N[self.lang]['descs'].get(token, "")

    def tr_err(self, code):
        return I18N[self.lang]['errors'].get(code, code)

    # -------------------------------------------------------------- build
    def _build_widgets(self):
        # Input and output boxes
        self.input = wx.TextCtrl(self.panel, style=wx.TE_RIGHT | wx.TE_PROCESS_ENTER)
        self.output = wx.TextCtrl(self.panel, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.input.Bind(wx.EVT_TEXT, self._on_input_text)
        self.input.Bind(wx.EVT_KEY_DOWN, lambda e: self._on_edit_key(e, is_input=True))
        self.output.Bind(wx.EVT_KEY_DOWN, lambda e: self._on_edit_key(e, is_input=False))

        grid = wx.GridSizer(rows=8, cols=4, vgap=5, hgap=5)
        for row in BUTTON_LAYOUT:
            for token in row:
                btn = ThemeButton(self.panel, token,
                                  on_click=self._on_button)
                kind = ('op' if token in OP_TOKENS else
                        'func' if token in FUNC_TOKENS else 'digit')
                btn.set_kind(kind)
                self._buttons[token] = btn
                grid.Add(btn, 1, wx.EXPAND)

        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(self.input, 0, wx.EXPAND | wx.ALL, 6)
        main.Add(self.output, 0, wx.EXPAND | wx.ALL, 6)
        main.Add(grid, 1, wx.EXPAND | wx.ALL, 6)
        self.panel.SetSizer(main)

    # ----------------------------------------------------------- shortcuts
    def _setup_shortcuts(self):
        accel = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('E'), self.ID_FOCUS_IN),
            (wx.ACCEL_CTRL, ord('R'), self.ID_FOCUS_OUT),
            (wx.ACCEL_CTRL, wx.WXK_RETURN, self.ID_EQUALS),
            (wx.ACCEL_CTRL, ord('L'), self.ID_CLEAR),
            (wx.ACCEL_CTRL, ord('B'), self.ID_BACKSPACE),
            (wx.ACCEL_NORMAL, wx.WXK_F1, self.ID_HELP),
            (wx.ACCEL_NORMAL, ord('?'), self.ID_HELP),
        ])
        self.SetAcceleratorTable(accel)

    # --------------------------------------------------------------- menus
    def _bind_menu_handlers(self):
        self.Bind(wx.EVT_MENU, self._on_focus_input, id=self.ID_FOCUS_IN)
        self.Bind(wx.EVT_MENU, self._on_focus_output, id=self.ID_FOCUS_OUT)
        self.Bind(wx.EVT_MENU, lambda e: self._action("="), id=self.ID_EQUALS)
        self.Bind(wx.EVT_MENU, lambda e: self._action("C"), id=self.ID_CLEAR)
        self.Bind(wx.EVT_MENU, lambda e: self._action("BSPC"), id=self.ID_BACKSPACE)
        self.Bind(wx.EVT_MENU, self._show_help, id=self.ID_HELP)
        self.Bind(wx.EVT_MENU, self._show_about, id=self.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self._on_exit, id=self.ID_EXIT)

        self.Bind(wx.EVT_MENU, lambda e, v='en': self._on_setting(e, lang=v), id=self.ID_LANG_EN)
        self.Bind(wx.EVT_MENU, lambda e, v='ar': self._on_setting(e, lang=v), id=self.ID_LANG_AR)
        self.Bind(wx.EVT_MENU, lambda e, v='light': self._on_setting(e, theme=v), id=self.ID_THEME_LIGHT)
        self.Bind(wx.EVT_MENU, lambda e, v='dark': self._on_setting(e, theme=v), id=self.ID_THEME_DARK)
        self.Bind(wx.EVT_MENU, lambda e, v='highcontrast': self._on_setting(e, theme=v), id=self.ID_THEME_HIGH)
        self.Bind(wx.EVT_MENU, lambda e, v='default': self._on_setting(e, colorscheme=v), id=self.ID_COLOR_STD)
        self.Bind(wx.EVT_MENU, lambda e, v='colorblind': self._on_setting(e, colorscheme=v), id=self.ID_COLOR_CB)
        self.Bind(wx.EVT_MENU, lambda e, v='normal': self._on_setting(e, fontsize=v), id=self.ID_FONT_NORMAL)
        self.Bind(wx.EVT_MENU, lambda e, v='large': self._on_setting(e, fontsize=v), id=self.ID_FONT_LARGE)
        self.Bind(wx.EVT_MENU, lambda e, v='xlarge': self._on_setting(e, fontsize=v), id=self.ID_FONT_XLARGE)

    def _rebuild_menus(self):
        t = self.tr
        mb = wx.MenuBar()
        mfile = wx.Menu()
        mfile.Append(self.ID_EXIT, t("menu.exit"))
        mb.Append(mfile, t("menu.file"))

        mset = wx.Menu()

        mlang = wx.Menu()
        mlang.AppendRadioItem(self.ID_LANG_EN, t("menu.lang.en"))
        mlang.AppendRadioItem(self.ID_LANG_AR, t("menu.lang.ar"))
        mlang.Check(self.ID_LANG_AR if self.lang == 'ar' else self.ID_LANG_EN, True)
        mset.AppendSubMenu(mlang, t("menu.language"))

        mtheme = wx.Menu()
        mtheme.AppendRadioItem(self.ID_THEME_LIGHT, t("menu.theme.light"))
        mtheme.AppendRadioItem(self.ID_THEME_DARK, t("menu.theme.dark"))
        mtheme.AppendRadioItem(self.ID_THEME_HIGH, t("menu.theme.high"))
        mtheme.Check({'light': self.ID_THEME_LIGHT,
                      'dark': self.ID_THEME_DARK,
                      'highcontrast': self.ID_THEME_HIGH}[self.config['theme']],
                     True)
        mset.AppendSubMenu(mtheme, t("menu.theme"))

        mcolor = wx.Menu()
        mcolor.AppendRadioItem(self.ID_COLOR_STD, t("menu.colors.std"))
        mcolor.AppendRadioItem(self.ID_COLOR_CB, t("menu.colors.cb"))
        mcolor.Check(self.ID_COLOR_CB if self.config['colorscheme'] == 'colorblind'
                     else self.ID_COLOR_STD, True)
        mset.AppendSubMenu(mcolor, t("menu.colors"))

        mfont = wx.Menu()
        mfont.AppendRadioItem(self.ID_FONT_NORMAL, t("menu.font.normal"))
        mfont.AppendRadioItem(self.ID_FONT_LARGE, t("menu.font.large"))
        mfont.AppendRadioItem(self.ID_FONT_XLARGE, t("menu.font.xlarge"))
        mfont.Check({'normal': self.ID_FONT_NORMAL,
                     'large': self.ID_FONT_LARGE,
                     'xlarge': self.ID_FONT_XLARGE}[self.config['fontsize']],
                    True)
        mset.AppendSubMenu(mfont, t("menu.font"))

        mb.Append(mset, t("menu.settings"))

        mhelp = wx.Menu()
        mhelp.Append(self.ID_HELP, t("menu.help"))
        mhelp.Append(self.ID_ABOUT, t("menu.about"))
        mb.Append(mhelp, t("menu.help_menu"))

        self.SetMenuBar(mb)

    # ---------------------------------------------------------------- apply
    def _make_palette(self):
        pal = dict(THEMES[self.config['theme']])
        pal['accent'] = ACCENTS[(self.config['colorscheme'], self.config['theme'])]
        pal['font_scale'] = FONT_SCALES[self.config['fontsize']]
        return pal

    def _dup_font(self, f):
        return wx.Font(f.GetPointSize(), f.GetFamily(), f.GetStyle(),
                       f.GetWeight(), f.GetUnderlined(), f.GetFaceName(),
                       f.GetEncoding())

    def _make_fonts(self, pal):
        base = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        s = max(1.0, pal['font_scale'])
        f_btn = self._dup_font(base)
        f_btn.SetPointSize(max(9, int(base.GetPointSize() * s)))
        f_in = self._dup_font(base)
        f_in.SetPointSize(max(11, int(base.GetPointSize() * s * 1.4)))
        f_out = self._dup_font(base)
        f_out.SetPointSize(max(11, int(base.GetPointSize() * s * 1.4)))
        f_out.SetWeight(wx.FONTWEIGHT_BOLD)
        return f_btn, f_in, f_out

    def _apply_config(self):
        self._apply_language()
        self._apply_theme()
        self._rebuild_menus()
        self.Layout()
        save_config(self.config)

    def _apply_language(self):
        t = self.tr
        self.SetTitle(t("title"))

        # layout direction (available on MSW)
        if self.lang == 'ar':
            try:
                self.SetLayoutDirection(wx.Layout_RightToLeft)
            except Exception:
                pass
        else:
            try:
                self.SetLayoutDirection(wx.Layout_LeftToRight)
            except Exception:
                pass

        ci = self._set_acc_wrap
        ci(self.input, t("in_name"), t("in_desc"))
        ci(self.output, t("out_name"), t("out_desc"))

    def _set_acc_wrap(self, win, name, desc):
        acc = NamedAccessible(name, desc, role=wx.ROLE_SYSTEM_TEXT)
        win.SetAccessible(acc)
        self._accessibles.append(acc)

    def _apply_theme(self):
        pal = self._make_palette()
        f_btn, f_in, f_out = self._make_fonts(pal)

        self.panel.SetBackgroundColour(pal['bg'])
        self.panel.SetForegroundColour(pal['fg'])

        self.input.SetBackgroundColour(pal['in_bg'])
        self.input.SetForegroundColour(pal['in_fg'])
        self.input.SetFont(f_in)
        self.output.SetBackgroundColour(pal['out_bg'])
        self.output.SetForegroundColour(pal['out_fg'])
        self.output.SetFont(f_out)

        sb = self.GetStatusBar()
        if sb:
            sb.SetBackgroundColour(pal['sb_bg'])
            sb.SetForegroundColour(pal['sb_fg'])

        accent = pal['accent']
        press = I18N[self.lang]['press']
        for token, btn in self._buttons.items():
            if token in DIGIT_TOKENS:
                fp = (pal['btn'], pal['btnfg'], pal['btn'], accent)
            elif token == 'EQUALS':
                fp = (accent, '#ffffff', accent, accent)
            elif token in OP_TOKENS or token in FUNC_TOKENS:
                fp = (pal['op_btn'], pal['op_fg'], pal['op_btn'], accent)
            else:
                fp = (pal['btn'], pal['btnfg'], pal['btn'], accent)

            label = BUTTON_LABELS[self.lang].get(token, token)
            btn.configure(label,
                          self.tr_names(token),
                          self.tr_descs(token),
                          fp, f_btn, press)

        self.GetStatusBar().SetStatusText(self.tr("status"))

    # --------------------------------------------------------------- events
    def _on_setting(self, evt, lang=None, theme=None, colorscheme=None,
                    fontsize=None):
        onChange = False
        if lang is not None and lang in ('en', 'ar') and self.lang != lang:
            self.lang = lang
            self.config['lang'] = lang
            onChange = True
        if theme is not None and self.config['theme'] != theme:
            self.config['theme'] = theme
            onChange = True
        if colorscheme is not None and self.config['colorscheme'] != colorscheme:
            self.config['colorscheme'] = colorscheme
            onChange = True
        if fontsize is not None and self.config['fontsize'] != fontsize:
            self.config['fontsize'] = fontsize
            onChange = True
        if onChange:
            self._apply_config()

    def _on_exit(self, evt):
        self.Close()

    def _on_focus_input(self, evt):
        self.input.SetFocus()

    def _on_focus_output(self, evt):
        self.output.SetFocus()

    def _show_help(self, evt):
        wx.MessageBox(self.tr("help"), self.tr("menu.help"),
                      wx.OK | wx.ICON_INFORMATION)

    def _show_about(self, evt):
        wx.MessageBox(self.tr("about"), self.tr("app.about"),
                      wx.OK | wx.ICON_INFORMATION)

    # --------------------------------------------------------- input events
    def _on_input_text(self, evt):
        # Typing into the input invalidates a stale result.
        self.output.SetValue("")

    def _on_edit_key(self, evt, is_input):
        k = evt.GetKeyCode()
        if k in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._calculate()
            return
        if k == wx.WXK_ESCAPE:
            self._action("C")
            return
        if k == wx.WXK_BACK:
            if not is_input:
                self.input.SetValue(self.input.GetValue()[:-1])
                self.input.SetFocus()
            else:
                evt.Skip()
            return
        if not is_input:
            uc = evt.GetUnicodeKey()
            if uc and chr(uc) in '0123456789+-*/%.()':
                self.input.SetValue(self.input.GetValue() + chr(uc))
                self.input.SetInsertionPointEnd()
                self.input.SetFocus()
                return
        evt.Skip()

    # ------------------------------------------------------------ calculator
    def _to_ascii(self, token):
        return {'DIV': '/', 'MUL': '*', 'SUB': '-', 'ADD': '+',
                'PCT': '%'}.get(token, token)

    def _action(self, token):
        if token in DIGIT_TOKENS:
            self._append(token)
            self.input.SetFocus()
        elif token in ('DIV', 'MUL', 'SUB', 'ADD', 'PCT'):
            self._append(self._to_ascii(token))
            self.input.SetFocus()
        elif token in ('LPAREN', 'RPAREN'):
            self._append('(' if token == 'LPAREN' else ')')
            self.input.SetFocus()
        elif token == 'DOT':
            self._append('.')
            self.input.SetFocus()
        elif token == 'EQUALS':
            self._calculate()  # moves focus to result box
        elif token == 'C':
            self.input.SetValue("")
            self.output.SetValue("")
            self.input.SetFocus()
        elif token == 'BSPC':
            self.input.SetValue(self.input.GetValue()[:-1])
            self.input.SetFocus()
        elif token == 'SIGN':
            self._compute(lambda v: -v)
        elif token in ('SIN', 'COS', 'TAN', 'SQRT', 'SQUARE', 'INV'):
            self._function(token)
        elif token in ('MC', 'MR', 'MP', 'MS'):
            self._memory(token)

    def _append(self, text):
        self.input.SetValue(self.input.GetValue() + text)
        self.input.SetInsertionPointEnd()

    def _input_value(self):
        text = self.input.GetValue()
        try:
            return evaluate(text)
        except Exception:
            return None

    def _calculate(self):
        text = self.input.GetValue()
        try:
            result = evaluate(text)
            self.output.SetValue(format_number(result))
        except CalcError as e:
            self.output.SetValue(self.tr_err(e.code))
        except Exception:
            self.output.SetValue(self.tr_err('expr'))
        self.output.SetFocus()

    def _compute(self, fn):
        v = self._input_value()
        if v is not None:
            self.output.SetValue(format_number(fn(v)))
            self.output.SetFocus()

    def _function(self, token):
        v = self._input_value()
        if v is None:
            return
        try:
            if token == 'SQRT':
                r = math.sqrt(v)
            elif token == 'SQUARE':
                r = v * v
            elif token == 'INV':
                r = 1.0 / v
            elif token == 'SIN':
                r = math.sin(math.radians(v))
            elif token == 'COS':
                r = math.cos(math.radians(v))
            elif token == 'TAN':
                r = math.tan(math.radians(v))
            else:
                r = v
            self.output.SetValue(format_number(r))
            self.output.SetFocus()
        except Exception:
            self.output.SetValue(self.tr_err('expr'))
            self.output.SetFocus()

    def _memory(self, token):
        if token == 'MC':
            self._mem_value = 0.0
            return
        if token == 'MR':
            self._append(format_number(self._mem_value))
            self.input.SetFocus()
            return
        try:
            v = evaluate(self.input.GetValue())
        except Exception:
            return
        if token == 'MP':
            self._mem_value += v
        elif token == 'MS':
            self._mem_value -= v

    def _on_button(self, token):
        self._action(token)


# ---------------------------------------------------------------------------
app_instance = None


def main():
    global app_instance
    app_instance = wx.App(False)
    frame = CalculatorFrame()
    frame.Show()
    app_instance.MainLoop()


if __name__ == "__main__":
    main()