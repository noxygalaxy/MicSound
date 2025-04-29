<div align="center">
  <div>
    <img src="https://github.com/noxygalaxy/for-projects/raw/refs/heads/main/MicSoundAssets/iconbgrounded.png" width="150" alt="MicSound Logo"/>  
  </div>
  <h1>MicSound</h1>
  <img src="https://img.shields.io/github/downloads/noxygalaxy/micsound/total?style=for-the-badge"></img>  
  <img src="https://img.shields.io/github/created-at/noxygalaxy/micsound?style=for-the-badge"></img>
  <h2>Русский | <a href="https://github.com/noxygalaxy/micsound/blob/main/README_en.md">English</a></h2>  
</div>

**MicSound** — это приложение, написанное на Python, предназначенное для воспроизведения звуковых эффектов при переключении микрофона на РП проектах. Приложение поддерживает различные серверы, такие как GTA5RP и Majestic RP, и позволяет легко настраивать громкость, а также включать или выключать логи отладки ( если приложение открыто через консоль ).

## Возможности
- **Звук при переключении микрофона:** Воспроизводит звук при включении/выключении микрофона.
- **Выбор сервера:** Возможность выбрать сервер между "GTA5RP" и "Majestic RP".
- **Управление громкостью:** Настройка громкости звука непосредственно в приложении.
- **Логи отладки:** Включение или отключение логов отладки для мониторинга событий ( только если приложение открыто через консоль ).
- **Интеграция с системным трей:** Минимизация приложения в системный трей с легким доступом через иконку в трее.

## Используемые библиотеки
- **pygame:** Для воспроизведения звуков.
- **keyboard:** Для отслеживания нажатий клавиш.
- **PySide6:** Для создания графического интерфейса.
- **PySide6 Fluent Widgets:** Для Fluent дизайна по типу Windows 11
- **Pillow:** Для обработки изображений.

## Установка + Запуск
1. Установите .exe файл с [Releases](https://github.com/noxygalaxy/micsound/releases/latest/download/MicSound.exe).
2. Перекиньте .exe файл в любую папку удобную для вас.
3. Запустите приложение

## Установка через git + python
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/noxygalaxy/MicSound.git
   cd MicSound
   ```

2. Установите необходимые библиотеки:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите приложение:
   ```bash
   python main.py
   ```

## Конфигурация
Вы можете настроить параметры, такие как громкость, выбор сервера и логи отладки, через страницу настроек в приложении. Конфигурация сохраняется автоматически в файл `config.json` в папке в которой вы откроете приложение.