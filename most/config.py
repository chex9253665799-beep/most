#!/usr/bin/env python3
"""Вшитые настройки «Моста» (тот же формат, что custom.txt RustDesk): печатает base64 JSON.
Сервер и ключ берутся из переменных окружения MOST_HOST / MOST_KEY (секреты репозитория)."""
import base64, json, os

host, key = os.environ["MOST_HOST"].strip(), os.environ["MOST_KEY"].strip()
cfg = {
    "app-name": "Мост",
    # default-settings: начальные значения, пользователь может поменять
    "default-settings": {
        "view-style": "adaptive",          # картинка подгоняется под размер окна и экрана
        "show-monitors-toolbar": "Y",      # переключатель мониторов, если у удалённого ПК их несколько
        "lang": "ru",
    },
    # override-settings: свой сервер (пользователь не может его поменять) и скрытые разделы настроек.
    # Ключи hide-*/disable-* попадают во встроенные настройки (BUILTIN_SETTINGS) RustDesk.
    "override-settings": {
        "custom-rendezvous-server": host,
        "relay-server": host,
        "key": key,
        "api-server": "",
        "hide-server-settings": "Y",
        "hide-network-settings": "Y",
        "hide-proxy-settings": "Y",
        "hide-websocket-settings": "Y",
        "hide-security-settings": "Y",
        "hide-stop-service": "Y",
        "hide-help-cards": "Y",
        "hide-powered-by-me": "Y",
        "disable-change-id": "Y",
    },
}
print(base64.b64encode(json.dumps(cfg, ensure_ascii=True).encode()).decode())
