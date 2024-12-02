# BRandom - Banát Random

Open-source generátor náhodných čísel pro výběr účastníků na expedici do Banátu.

## Spuštení

### Python interpreter

Pro spuštění je potřeba Python 3.11 a knihovna [Tkinter](https://docs.python.org/3/library/tkinter.html).

```bash
python3 main.py
```

### Executable

Lze stáhnout z releases, poté se spouští jako klasický `.exe` soubor. Aplikace se buildí pomocí `pyinstaller`:

```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py 
```

## Generování náhodného pořadí

Probíhá ve funkci `generate_and_shuffle_numbers`, která všechna čísla vygeneruje a promíchá najednou. Postupné zobrazování v GUI nemá na generování pořadí žádný vliv.

Funkce ještě před vrácením pořadí uloží do textového souboru se zaznamenaným časem, kdy k generování došlo.

