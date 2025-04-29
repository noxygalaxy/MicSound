<div align="center">
  <div>
    <img src="https://github.com/noxygalaxy/for-projects/raw/refs/heads/main/MicSoundAssets/iconbgrounded.png" width="150" alt="MicSound Logo"/>  
  </div>
  <h1>MicSound</h1>
  <img src="https://img.shields.io/github/downloads/noxygalaxy/micsound/total?style=for-the-badge"></img>  
  <img src="https://img.shields.io/github/created-at/noxygalaxy/micsound?style=for-the-badge"></img>
  <h2><a href="https://github.com/noxygalaxy/micsound/blob/main/README.md">Русский</a> | English</h2>  
</div>

**MicSound** is an application written in Python, designed to play sound effects when toggling the microphone in RP (Role-Play) projects. The application supports various servers like GTA5RP and Majestic RP, and allows easy adjustment of the volume, as well as enabling or disabling debug logs (if the application is opened through a console).

## Features
- **Microphone Toggle Sound:** Plays a sound when the microphone is turned on or off.
- **Server Selection:** Ability to choose a server between "GTA5RP" and "Majestic RP."
- **Volume Control:** Adjust the sound volume directly within the application.
- **Debug Logs:** Enable or disable debug logs to monitor events (only if the application is launched through the console).
- **System Tray Integration:** Minimize the application to the system tray with easy access via the tray icon.

## Libraries Used
- **pygame:** For playing sounds.
- **keyboard:** For tracking key presses.
- **PySide6:** For creating the graphical user interface.
- **PySide6 Fluent Widgets:** For a Windows 11-style Fluent design.
- **Pillow:** For image processing.

## Installation + Launch
1. Download the .exe file from [Releases](https://github.com/noxygalaxy/micsound/releases/latest/download/MicSound.exe).
2. Move the .exe file to any folder convenient for you.
3. Launch the application.

## Installation via Git + Python
1. Clone the repository:
   ```bash
   git clone https://github.com/noxygalaxy/MicSound.git
   cd MicSound
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   python main.py
   ```

## Configuration
You can adjust settings such as volume, server selection, and debug logs through the settings page in the application. Configuration is automatically saved to the `config.json` file in the folder where you opened the application.