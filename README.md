# Smart Calculator

An advanced, bilingual (Arabic / English) desktop calculator built with Python and wxPython. It is designed to be accessible to screen-reader users and includes light, dark and high-contrast themes plus colour-blind safe colour schemes.

## Features

- Bilingual interface (Arabic and English), with right-to-left layout for Arabic.
- Basic and scientific operations: +, −, ×, ÷, %, parentheses, sin, cos, tan (degrees), sqrt, square, reciprocal, log and ln.
- Memory functions: MC, MR, M+, M−.
- Keyboard shortcuts: Enter / Ctrl+Enter to calculate, Ctrl+E for the input box, Ctrl+R for the result box, Esc to clear, Backspace, Ctrl+L to clear, Ctrl+B for backspace and F1 or ? for help.
- Themes: Light, Dark and High Contrast.
- Colour schemes: Standard and colour-blind friendly (orange / blue).
- Font sizes: Normal, Large and Extra Large.
- Settings are saved to `calculator_settings.json`.
- Accessible controls: custom `wx.Accessible` objects for every button and text box.
- Self-drawn buttons so themes and colours render consistently on Windows.
- Safe expression evaluator using a recursive-descent parser; `eval()` is never used.

## Requirements

- Python 3.8 or newer.
- wxPython 4.2 or newer.

Install wxPython with:

```bash
python -m pip install wxPython
```

## Run

```bash
python calculator.py
```

## Tests

```bash
python -m unittest -v test_calculator.py
```

## Project files

- `calculator.py` — application source code.
- `calculator_settings.json` — saved language, theme, colour scheme and font size.
- `test_calculator.py` — unit tests for the expression evaluator.
- `LICENSE` — MIT license.
- `.gitignore` — files that should not be committed.

## License

Released under the MIT License. See `LICENSE` for details.

## Author

Hanan
