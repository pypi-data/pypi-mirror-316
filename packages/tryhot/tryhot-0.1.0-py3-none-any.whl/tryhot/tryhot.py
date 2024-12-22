# /// script
# requires-python = ">=3.8.10"
# dependencies = [
#     "watchdog>=3.0.0",
# ]
# ///

"""
A minimal hot-reload implementation that watches for file changes and automatically
restarts the target function. It uses a parent-child process model where the parent
watches for changes and spawns child processes to run the actual code.

Features:
- Watches specified directories for file changes
- Automatically restarts on detected changes
- Supports recursive directory watching
- Handles keyboard interrupts gracefully
"""

import os
import sys
import time
import subprocess
import inspect
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, EVENT_TYPE_MODIFIED


def hotreload(func, watch_path=".", extensions=(".py",), recursive=True):
    """
    Minimal single-file hot-reload:
      - If HOTRELOAD_RUN is set in env, we are the *child* process -> just run `func()`.
      - Otherwise, we are the *parent/watcher* process:
          1. Spawn a child process with HOTRELOAD_RUN=1
          2. Watch for file changes
          3. If a *.py file changes, kill and restart the child
    """
    if os.environ.get("HOTRELOAD_RUN"):
        # We are in the child process -> just run the main function and exit
        return func()

    # We are the parent (watcher) process: set up environment for child
    new_env = dict(os.environ)
    new_env["HOTRELOAD_RUN"] = "1"

    # Figure out how to invoke `func` in the child process
    mod = inspect.getmodule(func)
    if not mod or func.__name__ == '<lambda>':
        raise RuntimeError("Could not determine the module of the given function or lambda functions are not supported.")
    module_name = mod.__name__
    func_name = func.__name__

    # If func is in __main__, then just re-run *this* file
    # Otherwise, import the module and call the function
    if module_name == "__main__":
        command = [sys.executable, sys.argv[0]]
    else:
        command = [
            sys.executable,
            "-c",
            f"import {module_name}; {module_name}.{func_name}()",
        ]

    # Start child process
    process = subprocess.Popen(command, env=new_env)

    # Setup filesystem watcher
    observer = Observer()

    class _ReloadHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.event_type == EVENT_TYPE_MODIFIED and any(
                event.src_path.endswith(ext) for ext in extensions
            ):
                nonlocal process
                print(
                    f"[hotreload] Detected change in {event.src_path}. Restarting child process..."
                )
                process.terminate()
                process.wait()
                process = subprocess.Popen(command, env=new_env)

    observer.schedule(_ReloadHandler(), watch_path, recursive=recursive)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[hotreload] Stopping...")
    finally:
        observer.stop()
        observer.join()
        # Terminate child if still running
        if process.poll() is None:
            process.terminate()
            process.wait()
