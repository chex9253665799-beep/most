#!/usr/bin/env python3
"""«Мост»: замена названия и производителя в исходниках перед сборкой (вызывается из CI).
Запускается один раз на чистых исходниках; падает, если ожидаемого текста нет (значит, исходники RustDesk поменялись)."""
import pathlib, re, sys

NAME = "Мост"          # видимое название
EXE = "most"           # имя файла программы (латиницей)
COMPANY = "Мост"
root = pathlib.Path(__file__).resolve().parent.parent
errors = []


def sub(path, pattern, repl, regex=False, required=True, count=0):
    p = root / path
    t = p.read_text(encoding="utf-8")
    n = len(re.findall(pattern, t)) if regex else t.count(pattern)
    if n == 0:
        if required:
            errors.append(f"{path}: не найдено {pattern!r}")
        return
    t = re.sub(pattern, repl, t, count=count) if regex else t.replace(pattern, repl)
    p.write_text(t, encoding="utf-8", newline="")
    print(f"{path}: {pattern!r} → {repl!r} ({n})")


# описание exe (Windows → Свойства → Подробно)
for f in ("Cargo.toml", "libs/portable/Cargo.toml"):
    sub(f, 'description = "RustDesk Remote Desktop"', f'description = "{NAME}"')
    sub(f, 'ProductName = "RustDesk"', f'ProductName = "{NAME}"')
    sub(f, 'FileDescription = "RustDesk Remote Desktop"', f'FileDescription = "{NAME} — удалённый доступ"')
    sub(f, 'OriginalFilename = "rustdesk.exe"', f'OriginalFilename = "{EXE}.exe"')
    sub(f, r"Copyright © \d+ Purslane Tech Pte\. Ltd\. All rights reserved\.", f"{COMPANY}", regex=True, required=False)
sub("libs/portable/src/main.rs", 'const APP_PREFIX: &str = "rustdesk";', f'const APP_PREFIX: &str = "{EXE}";')

rc = "flutter/windows/runner/Runner.rc"
sub(rc, '"RustDesk Remote Desktop"', f'"{NAME} — удалённый доступ"')
sub(rc, 'VALUE "InternalName", "rustdesk" "\\0"', f'VALUE "InternalName", "{EXE}" "\\0"')
sub(rc, '"rustdesk.exe"', f'"{EXE}.exe"')
sub(rc, '"RustDesk"', f'"{NAME}"')
sub(rc, r"Copyright © \d+ Purslane Tech Pte\. Ltd\. All rights reserved\.", COMPANY, regex=True, required=False)
sub(rc, "Purslane Tech Pte. Ltd.", COMPANY, required=False)

# тексты интерфейса не трогаем: translate() сам подставляет имя программы вместо «RustDesk»

# производитель в «О программе»
for f in ("flutter/lib/desktop/pages/desktop_setting_page.dart", "src/main.rs"):
    sub(f, "Purslane Tech Pte. Ltd.", COMPANY, required=False)
    sub(f, "Purslane Ltd", COMPANY, required=False)

# фирменные цвета «Моста» вместо синего и серого RustDesk: акценты, кнопки, тёмные фоны — как в панели
import glob
PALETTE = {
    # синие акценты → фиолетово-розовые
    "0071FF": "7C3AED", "2C8CFF": "8B5CF6", "2196F3": "8B5CF6", "0C6AF6": "7C3AED",
    "0697EA": "A855F7", "0583EA": "9333EA", "2F65BA": "6D28D9", "00B6F0": "E879F9",
    # тёмная тема: серые → глубокий фиолетовый, как фон панели
    "18191E": "0C0A16", "24252B": "1D1934", "212121": "151227", "3F3F3F": "2C2648",
    "555555": "3A3260", "121212": "0A0814", "202020": "151227",
}
for f in glob.glob(str(root / "flutter/lib/**/*.dart"), recursive=True):
    t = open(f, encoding="utf-8").read()
    n = t
    for old, new in PALETTE.items():
        n = re.sub(r"(?i)(0x[0-9a-f]{2})" + old, r"\g<1>" + new, n)
    n = n.replace("Color.fromARGB(255, 45, 46, 53)", "Color.fromARGB(255, 40, 34, 70)")
    if n != t:
        open(f, "w", encoding="utf-8", newline="").write(n)
        print(f"{f}: цвета «Моста»")
sub("flutter/lib/common.dart", "primary: Colors.blue,", "primary: const Color(0xFF7C3AED),")
sub("flutter/lib/common.dart", "primary: Colors.blue, secondary: accent", "primary: const Color(0xFF7C3AED), secondary: accent", required=False)

# не предлагать обновление до RustDesk
sub("flutter/lib/desktop/pages/desktop_home_page.dart", "updateUrl.isNotEmpty", "false", required=False)

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("Брендинг применён")
