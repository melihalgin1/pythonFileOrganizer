# 📂 Python File Organizer (Automation Service)

**A high-performance, background automation tool that keeps your Downloads folder clean.**

This is not just a script—it's a resilient **System Service** that runs in the background, monitoring your directories in real-time. It automatically detects new files, categorizes them based on your rules, and moves them to their designated folders instantly.

## 🚀 Key Features

* **⚡ Event-Driven (Zero Latency):** Uses the `watchdog` library to detect file creation instantly. No CPU-wasting "sleep loops."
* **🛡️ Data Safety First:** Never overwrites files. If `report.pdf` exists, it auto-renames the new one to `report_16345.pdf` (timestamped).
* **⚙️ Smart Configuration:** Fully customizable via `config.json`. Change folders or extensions without touching the code.
* **🐛 Robust Architecture:**
    * **Large File Protection:** Waits for large downloads (movies, ISOs) to finish writing before attempting to move them.
    * **Professional Logging:** Tracks all actions to `organizer.log` instead of crashing console output.
* **💻 Cross-Platform:** runs on macOS (launchd), Linux (systemd), and Windows.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/file-organizer.git](https://github.com/yourusername/file-organizer.git)
cd file-organizer
```

### 2. Install Dependencies
```bash
pip install watchdog
```

### 3. Configure Your Rules
1.  Locate `config.example.json`.
2.  Rename it to **`config.json`**.
3.  Open it and set your **Source Folder** (e.g., Downloads) and **Target Paths**.
    * *Note: Use double backslashes `\\` for Windows paths.*

---

## 🖥️ Running in the Background

### 🍎 macOS (using `launchd`)

1.  **Edit the Plist:**
    Open `com.yourname.organizer.plist.example`.
    * Replace `/PATH/TO/YOUR/PROJECT_FOLDER` with your actual path.
    * Replace `/usr/bin/python3` with your Python path (run `which python3` to find it).
2.  **Install:**
    Rename the file to `com.yourname.organizer.plist` and move it:
    ```bash
    mv com.yourname.organizer.plist ~/Library/LaunchAgents/
    ```
3.  **Start Service:**
    ```bash
    launchctl load ~/Library/LaunchAgents/com.yourname.organizer.plist
    ```
4.  **Verify:**
    Check the log file in your project folder: `tail -f organizer.log`

### 🐧 Linux / Ubuntu (using `systemd`)

1.  **Create Service File:**
    ```bash
    nano ~/.config/systemd/user/organizer.service
    ```
    *(If the folder doesn't exist, create it: `mkdir -p ~/.config/systemd/user/`)*

2.  **Paste Configuration:**
    ```ini
    [Unit]
    Description=Python File Organizer
    After=network.target

    [Service]
    # IMPORTANT: Use quotes around the path if it contains spaces
    ExecStart=/usr/bin/python3 "/home/YOUR_USER/path/to/organizer.py"
    Restart=always

    [Install]
    WantedBy=default.target
    ```
3.  **Enable & Start:**
    ```bash
    systemctl --user enable organizer
    systemctl --user start organizer
    ```
4.  **Check Status:**
    ```bash
    systemctl --user status organizer
    ```

### 🪟 Windows

1.  Open **Task Scheduler**.
2.  Create a Basic Task -> "Start a Program".
3.  **Program/script:** `pythonw.exe` (This runs Python without a window).
4.  **Arguments:** `C:\Path\To\organizer.py`
5.  Set the trigger to **"At log on"**.

---

## 📝 Configuration Reference (`config.json`)

Your `config.json` should look like this:

```json
{
  "source_folder": "/Users/name/Downloads",
  "rules": {
    "Images": {
      "target_path": "/Users/name/Pictures",
      "extensions": [".jpg", ".png", ".svg"]
    },
    "Documents": {
      "target_path": "/Users/name/Documents/Sorted",
      "extensions": [".pdf", ".docx", ".txt"]
    }
  }
}
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
