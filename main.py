import sys
import os
import json
import threading
import time
import keyboard
import pygame
from pygame import mixer
from PIL import Image
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition, MessageBox, setTheme, Theme
from qfluentwidgets import NavigationPushButton, FluentIcon
from qfluentwidgets import ComboBox, Slider, ToggleButton, BodyLabel, PrimaryPushButton
import urllib.request
import tempfile

pygame.mixer.init()

class MicSoundApp(FluentWindow):
    def __init__(self):
        super().__init__()
        self.config = {"debug_logs": False, "volume": 50, "selected_server": None}
        self.load_config()
        
        self.setWindowTitle("MicSound | github.com/noxygalaxy")
        self.resize(600, 400)
        self.setMinimumSize(400, 300)
        setTheme(Theme.DARK)
        self.apply_theme()

        self.config = {"debug_logs": False, "volume": 50, "selected_server": None}
        self.load_config()
        self.running = True
        self.key_thread = None
        self.tray_icon = None

        self.download_assets()

        self.initNavigation()
        self.setup_tray_icon()

        self.start_key_listener()
       
    def download_assets(self):
        asset_urls = {
            "icon.png": "https://github.com/noxygalaxy/for-projects/raw/refs/heads/main/MicSoundAssets/icon.png",
            "hold_start.ogg": "https://github.com/noxygalaxy/for-projects/raw/refs/heads/main/MicSoundAssets/hold_start.ogg",
            "hold_end.ogg": "https://github.com/noxygalaxy/for-projects/raw/refs/heads/main/MicSoundAssets/hold_end.ogg"
        }
        temp_dir = os.path.join(tempfile.gettempdir(), "MicSound", "Assets")
        os.makedirs(temp_dir, exist_ok=True)

        for file_name, url in asset_urls.items():
            file_path = os.path.join(temp_dir, file_name)
            if not os.path.exists(file_path):
                try:
                    urllib.request.urlretrieve(url, file_path)
                except Exception as e:
                    print(f"Ошибка загрузки {file_name}: {e}")

    def initNavigation(self):
        self.addSubInterface(self.create_server_page(), FluentIcon.GAME, "Выбор сервера")
        self.addSubInterface(self.create_settings_page(), FluentIcon.SETTING, "Настройки")
        self.addSubInterface(self.create_about_page(), FluentIcon.INFO, "О программе", NavigationItemPosition.BOTTOM)

    def create_server_page(self):
        from PySide6.QtWidgets import QWidget, QVBoxLayout
        widget = QWidget()
        widget.setObjectName("serverPage")
        layout = QVBoxLayout(widget)

        label = BodyLabel("Выберите RP сервер")
        label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        self.server_combo = ComboBox()
        self.server_combo.addItems(["GTA5RP", "Majestic RP"])
        if self.config["selected_server"]:
            self.server_combo.setCurrentText(self.config["selected_server"])
        self.server_combo.currentTextChanged.connect(self.on_server_changed)

        layout.addWidget(label)
        layout.addWidget(self.server_combo)
        layout.addStretch()
        return widget

    def create_settings_page(self):
        from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
        widget = QWidget()
        widget.setObjectName("settingsPage")
        layout = QVBoxLayout(widget)

        debug_layout = QHBoxLayout()
        debug_label = BodyLabel("Включить логи отладки")
        self.debug_toggle = ToggleButton()
        self.debug_toggle.setChecked(self.config["debug_logs"])
        self.debug_toggle.toggled.connect(self.on_debug_toggled)
        debug_layout.addWidget(debug_label)
        debug_layout.addWidget(self.debug_toggle)

        volume_layout = QHBoxLayout()
        volume_label = BodyLabel("Громкость")
        self.volume_slider = Slider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.config["volume"])
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)

        save_button = PrimaryPushButton("Сохранить конфигурацию")
        save_button.clicked.connect(self.save_config)

        layout.addLayout(debug_layout)
        layout.addLayout(volume_layout)
        layout.addWidget(save_button)
        layout.addStretch()
        return widget

    def create_about_page(self):
        from PySide6.QtWidgets import QWidget, QVBoxLayout
        widget = QWidget()
        widget.setObjectName("aboutPage")
        layout = QVBoxLayout(widget)

        about_text = BodyLabel(
            "MicSound by @noxygalaxy\n"
            "                     Версия 1.4.2\n\n"
            "Приложение для того чтобы включать звук при\nнажатии на кнопку вкл / выкл микрофона на РП проектах.\n\n\n\n"
            "Разработано на Python, с помощью библиотек\n- pygame\n- keyboard\n- PySide6\n- Pillow"
        )
        about_text.setStyleSheet("font-size: 14px;")

        layout.addWidget(about_text)
        layout.addStretch()
        return widget

    def on_server_changed(self, server):
        self.config["selected_server"] = server
        self.debug_log(f"Выбран сервер: {server}")
        self.save_config()
        self.restart_key_listener()
        
    def on_debug_toggled(self, checked):
        self.config["debug_logs"] = checked
        self.debug_log(f"Логи отладки {'включены' if checked else 'выключены'}")
        self.save_config()

    def on_volume_changed(self, value):
        self.config["volume"] = value
        self.debug_log(f"Громкость установлена на {value}%")

    def debug_log(self, message):
        if self.config["debug_logs"]:
            print(f"[DEBUG] {message}")

    def load_config(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    self.config.update(json.load(f))
                self.debug_log(f"Загружена конфигурация: {self.config}")
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")

    def save_config(self):
        try:
            with open("config.json", "w") as f:
                json.dump(self.config, f)
            self.debug_log("Конфигурация сохранена")
            MessageBox("Успех", "Конфигурация успешно сохранена!", self).exec()
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            MessageBox("Ошибка", f"Не удалось сохранить конфигурацию: {e}", self).exec()

    def play_sound(self, sound_file):
        try:
            sound_file = os.path.join(tempfile.gettempdir(), "MicSound", "Assets", os.path.basename(sound_file))
            sound = pygame.mixer.Sound(sound_file)
            sound.set_volume(self.config["volume"] / 100.0)
            sound.play()
            self.debug_log(f"Воспроизведение звука: {sound_file} при громкости {self.config['volume']}%")
        except Exception as e:
            print(f"Ошибка воспроизведения звука: {e}")

    def key_listener(self):
        key_to_monitor = 'b' if self.config["selected_server"] == "GTA5RP" else 'n'
        self.debug_log(f"Слушатель клавиш запущен. Отслеживаемая клавиша: {key_to_monitor}")

        while self.running:
            if keyboard.is_pressed(key_to_monitor):
                self.debug_log(f"Клавиша {key_to_monitor} нажата")
                self.play_sound("assets/hold_start.ogg")

                while keyboard.is_pressed(key_to_monitor) and self.running:
                    time.sleep(0.1)

                if self.running:
                    self.debug_log(f"Клавиша {key_to_monitor} отпущена")
                    self.play_sound("assets/hold_end.ogg")

            time.sleep(0.1)

    def start_key_listener(self):
        if not self.config["selected_server"]:
            self.config["selected_server"] = "GTA5RP"
            self.server_combo.setCurrentText("GTA5RP")
        self.key_thread = threading.Thread(target=self.key_listener, daemon=True)
        self.key_thread.start()
        self.debug_log("Поток слушателя клавиш запущен")

    def restart_key_listener(self):
        self.running = False
        if self.key_thread:
            self.key_thread.join(timeout=1.0)
        self.running = True
        self.start_key_listener()
        
    def load_config(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    self.config.update(json.load(f))
                self.debug_log(f"Загружена конфигурация: {self.config}")
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")

    def save_config(self):
        try:
            with open("config.json", "w") as f:
                json.dump(self.config, f)
            self.debug_log("Конфигурация сохранена")
            MessageBox("Успех", "Конфигурация успешно сохранена!", self).exec()
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            MessageBox("Ошибка", f"Не удалось сохранить конфигурацию: {e}", self).exec()

    def setup_tray_icon(self):
        icon_path = os.path.join(tempfile.gettempdir(), "MicSound", "Assets", "icon.png")
        try:
            if os.path.exists(icon_path):
                icon_image = Image.open(icon_path)
                self.debug_log(f"Загружен значок трея из {icon_path}")
            else:
                print(f"Предупреждение: Файл значка не найден по пути {icon_path}. Используется стандартный.")
                icon_image = Image.new('RGB', (64, 64))
        except Exception as e:
            print(f"Ошибка загрузки значка трея: {e}. Используется стандартный.")
            icon_image = Image.new('RGB', (64, 64))

        self.qt_tray = QSystemTrayIcon(QIcon(icon_path if os.path.exists(icon_path) else ""), self)
        tray_menu = QMenu()
        tray_menu.addAction("Открыть", self.restore_window)
        tray_menu.addAction("Выход", self.exit_application)
        self.qt_tray.setContextMenu(tray_menu)
        self.qt_tray.activated.connect(self.tray_activated)
        self.qt_tray.show()

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.restore_window()

    def restore_window(self):
        self.show()
        self.activateWindow()

    def exit_application(self):
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.qt_tray.showMessage(
            "MicSound",
            "Приложение свернуто в системный трей. Щелкните правой кнопкой мыши на значке, чтобы открыть или выйти.",
            QSystemTrayIcon.Information,
            2000
        )

def check_assets():
    temp_dir = os.path.join(tempfile.gettempdir(), "MicSound", "Assets")
    os.makedirs(temp_dir, exist_ok=True)
    missing_files = []
    for file in ["icon.png", "hold_start.ogg", "hold_end.ogg"]:
        if not os.path.exists(os.path.join(temp_dir, file)):
            missing_files.append(file)
    if missing_files:
        print("Предупреждение: Отсутствуют файлы:")
        for file in missing_files:
            print(f"- {file}")

if __name__ == "__main__":
    check_assets()
    app = QApplication(sys.argv)
    window = MicSoundApp()
    window.show()
    sys.exit(app.exec())