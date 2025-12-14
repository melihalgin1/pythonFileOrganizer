# 📂 Python File Organizer Service

A cross-platform background automation tool that monitors directories in real-time and organizes files into subfolders based on their extensions. Designed to demonstrate system scripting, file I/O operations, and daemonized process management.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Key Features

* **Event-Driven Architecture:** Utilizes the `watchdog` library to react to file system events immediately (avoiding resource-heavy polling loops).
* **Cross-Platform Compatibility:** Implements `os.path` and `pathlib` for OS-agnostic path handling (works on macOS, Windows, and Linux).
* **Smart Collision Handling:** Automatically detects duplicate filenames and renames new files with a timestamp to prevent data overwrites (e.g., `image.jpg` -> `image_170258.jpg`).
* **Audit Logging:** Maintains a persistent `organizer_history.log` file to track every file movement and error for debugging purposes.
* **Background Execution:** Includes configuration for running as a headless service via macOS `launchd`.

## 🛠️ Technical Stack

* **Language:** Python 3
* **Libraries:** `watchdog`, `shutil`, `os`, `logging`, `time`
* **Concepts:** File Systems, Observer Pattern, Error Handling, Daemonization.

## ⚙️ Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone https://github.com/melihalgin1/file-organizer.git
    cd file-organizer
    ```

2.  **Install Dependencies:**
    ```bash
    pip install watchdog
    ```

## 🏃 Usage

### 1. Configuration
Open `organizer.py` and verify the `TRACKED_FOLDER` variable.
* By default, it uses `os.path.expanduser("~")` to automatically find your **Downloads** folder on any operating system.

### 2. Manual Execution (Testing)
Run the script in your terminal to see it working:
```bash
python organizer.py
```
**Press Ctrl + C to stop the script.**

### Running in the background
1. For macOS users (Your OS may ask for specific permissions to be able to run in the background)
   1. Open com.yourname.organizer.plist in a text editor of your choice and update the Python and Script paths to match your system.
   2. Move the file to the LaunchAgents folder with the following command (or using finder if you wish).
      cp com.yourname.organizer.plist ~/Library/LaunchAgents/
   3. Load the Service with the following command
      launchctl load ~/Library/LaunchAgents/com.yourname.organizer.plist
2. For Windows Users
   This project includes an optional organizer.pyw file to add to Windows startup folder
   **Option 1: Startup Folder (Simple)**
   1. Press `Win + R` and run `shell:startup`.
   2. Place a shortcut to the `.pyw` file in this folder.

   **Option 2: Task Scheduler (Recommended)**
   1. Open Windows Task Scheduler and select "Create Task".
   2. Set Trigger to **"At log on"**.
   3. Set Action to **"Start a program"**:
      * Program: `pythonw.exe`
      * Arguments: `"C:\Path\To\organizer.py"`
   4. In Settings, enable "Restart task if it fails" to ensure persistence.
3. For Linux Users
   1. Open organizer.service in a text editor of your choice and update the Python and Script paths to match your system.
   2. Copy organizer.service to /etc/systemd/system/organizer.service
   3. Reload systemd so it sees the new file: sudo systemctl daemon-reload
   4. Enable the Script
     ```bash
    sudo systemctl enable organizer.service
    ```
   5. Start the script
   ```bash
    sudo systemctl start organizer.service
    ```
   6. Optional: You can check service status with
    ```bash
    systemctl status organizer
    ```    

## 📄 License
Distributed under the MIT License. See LICENSE for more information.
