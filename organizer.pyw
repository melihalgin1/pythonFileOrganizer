import os
import sys
import time
import json
import logging
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- 1. SETUP LOGGING ---
# This saves a log file in the same folder as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "organizer.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- 2. LOAD CONFIGURATION ---
config_path = os.path.join(script_dir, 'config.json')

try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    SOURCE_DIR = config['source_folder']
    RULES = config['rules']
    logging.info("Configuration loaded successfully.")

except Exception as e:
    logging.error(f"Failed to load config: {e}")
    sys.exit(1)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # We scan the directory to handle files that might have been pasted
        # or created quickly.
        with os.scandir(SOURCE_DIR) as entries:
            for entry in entries:
                if entry.is_file():
                    self.check_and_move(entry)

    def check_and_move(self, entry):
        filename = entry.name
        # Skip hidden files (like .DS_Store)
        if filename.startswith('.'):
            return

        # Get extension (lowercase for consistent matching)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Check against our Config Rules
        for category, data in RULES.items():
            if ext in data['extensions']:
                target_folder = data['target_path']
                self.move_file(entry.path, filename, target_folder)
                return  # Stop checking other categories once matched

    def make_unique(self, destination, filename):
        """
        If file exists, adds a timestamp to the name to prevent overwriting.
        Example: report.pdf -> report_16345023.pdf
        """
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        full_dest_path = os.path.join(destination, new_filename)

        while os.path.exists(full_dest_path):
            # Add timestamp for uniqueness
            timestamp = int(time.time())
            new_filename = f"{base}_{timestamp}{extension}"
            full_dest_path = os.path.join(destination, new_filename)
        
        return full_dest_path

    def move_file(self, src_path, filename, target_folder):
        try:
            # 1. Ensure target folder exists
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # 2. Generate a unique destination path
            dest_path = self.make_unique(target_folder, filename)

            # 3. Wait for file to be free (Basic Stability Check)
            # This prevents moving a file while it is still downloading
            initial_size = -1
            while initial_size != os.path.getsize(src_path):
                initial_size = os.path.getsize(src_path)
                time.sleep(1) # Wait 1 second and check size again

            # 4. Move
            shutil.move(src_path, dest_path)
            logging.info(f"Moved: {filename} -> {target_folder}")

        except Exception as e:
            logging.error(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    # Startup Check
    if not os.path.exists(SOURCE_DIR):
        logging.error(f"Source folder does not exist: {SOURCE_DIR}")
        sys.exit(1)

    logging.info(f"Organizer Service Started. Watching: {SOURCE_DIR}")
    
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()