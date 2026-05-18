import os, time, sys, json, sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Paths
POLICY_FILE = os.path.expanduser("~/Dev/sentinel/integrity.policy")
LOG_FILE = os.path.expanduser("~/Documents/obsidian/Null/Hermes-Flight-Log.md")

class SentinelHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            # Simple check: append log
            with open(LOG_FILE, "a") as f:
                f.write(f"\n- [SENTINEL ALERT] Modification detected: {event.src_path}\n")

if __name__ == "__main__":
    with open(POLICY_FILE, 'r') as f:
        policy = json.load(f)
    
    observer = Observer()
    handler = SentinelHandler()
    for path in policy['watch_paths']:
        observer.schedule(handler, os.path.expanduser(path), recursive=True)
    
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
