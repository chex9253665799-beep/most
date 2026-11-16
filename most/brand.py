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

# не предлагать обновление до RustDesk
sub("flutter/lib/desktop/pages/desktop_home_page.dart", "updateUrl.isNotEmpty", "false", required=False)

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("Брендинг применён")
