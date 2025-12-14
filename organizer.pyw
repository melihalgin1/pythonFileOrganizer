import os
from pathlib import Path
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Detect the user's home directory automatically
# On Mac: /Users/YourName
# On Windows: C:\Users\YourName
# On Linux: /home/YourName
HOME_DIR = os.path.expanduser("~")

# Construct the Downloads path safely for ANY OS
TRACKED_FOLDER = os.path.join(HOME_DIR, "Downloads")

# Define the log file location dynamically
LOG_FILE = os.path.join(TRACKED_FOLDER, "organizer_history.log")

DESTINATIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav"],
    "Video": [".mp4", ".mov", ".avi"],
    "Installers": [".exe", ".dmg", ".pkg", ".msi"]
}

# --- LOGGING SETUP ---
# This tells Python: "Write to a file, include the time, and the message."
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- THE LOGIC ---
class SmartFileMover(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered when a file is pasted or dragged in."""
        if event.is_directory:
            return
        
        # Log and process
        # logging.info(f"Detected creation: {event.src_path}") # Optional verbose log
        self.move_file(event.src_path)

    def on_moved(self, event):
        """Triggered when a browser renames a download from .crdownload to .jpg"""
        if event.is_directory:
            return

        # For "moved" events, we care about where it ended up (dest_path),
        # not where it started (src_path).
        logging.info(f"Detected download completion (rename): {event.dest_path}")
        self.move_file(event.dest_path)

    def move_file(self, file_path):
        """Shared logic to check extension and move file."""
        # 1. Check if file still exists (browsers can be tricky)
        if not os.path.exists(file_path):
            return

        filename = os.path.basename(file_path)
        
        # Safety: Don't move the log file!
        if filename == "organizer_history.log":
            return
            
        # 2. Filter out temporary browser files explicitly
        if filename.endswith(".crdownload") or filename.endswith(".part") or filename.endswith(".tmp"):
            return

        # 3. Standard Logic
        extension = os.path.splitext(filename)[1].lower()

        for folder_name, extensions in DESTINATIONS.items():
            if extension in extensions:
                destination_folder = os.path.join(TRACKED_FOLDER, folder_name)
                
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                
                # Handle Duplicates
                destination_path = os.path.join(destination_folder, filename)
                if os.path.exists(destination_path):
                    name, ext = os.path.splitext(filename)
                    timestamp = int(time.time())
                    new_filename = f"{name}_{timestamp}{ext}"
                    destination_path = os.path.join(destination_folder, new_filename)

                # Move and Log
                try:
                    # Small buffer time for the filesystem to unlock the file after rename
                    time.sleep(1) 
                    shutil.move(file_path, destination_path)
                    logging.info(f"SUCCESS: Moved '{filename}' to {folder_name}")
                except Exception as e:
                    logging.error(f"ERROR moving {filename}: {e}")
                return

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if not os.path.exists(TRACKED_FOLDER):
        print(f"ERROR: Folder {TRACKED_FOLDER} not found.")
    else:
        event_handler = SmartFileMover()
        observer = Observer()
        observer.schedule(event_handler, TRACKED_FOLDER, recursive=False)
        
        # Log that the service started
        logging.info("--- Service Started: Monitoring Folder ---")
        
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logging.info("--- Service Stopped by User ---")
        observer.join()
