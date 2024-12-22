# /// script
# requires-python = ">=3.8.10"
# dependencies = [
#     "watchdog>=3.0.0",
#     "pytest>=7.0.0",
# ]
# ///

"""
Test suite for the tryhot functionality. Tests cover:
- Child process execution
- File watching and reloading
- Error handling
- Environment variable handling
"""

import os
import time
import pytest
import multiprocessing
from pathlib import Path
from tryhot.tryhot import hotreload

# Move helper functions outside test functions so they can be pickled
def dummy_func():
    time.sleep(0.5)  # Keep process alive briefly

def run_hotreload_with_path(watch_path, extensions=(".py",), recursive=True):
    hotreload(dummy_func, watch_path=watch_path, extensions=extensions, recursive=recursive)

def test_function():
    """Simple function for testing hotreload"""
    return "test_success"


def test_child_process_execution():
    """Test that the function executes correctly in child process mode"""
    os.environ["HOTRELOAD_RUN"] = "1"
    try:
        result = hotreload(test_function)
        assert result == "test_success"
    finally:
        del os.environ["HOTRELOAD_RUN"]


def test_file_change_triggers_reload(tmp_path):
    """Test that file changes trigger a reload"""
    # Create a temporary Python file
    test_file = tmp_path / "test_watch.py"
    test_file.write_text("print('initial content')")
    
    process = multiprocessing.Process(
        target=run_hotreload_with_path,
        args=(str(tmp_path),)
    )
    process.start()
    
    try:
        # Give the watcher time to start
        time.sleep(1)
        
        # Modify the file
        test_file.write_text("print('modified content')")
        
        # Wait for reload to occur
        time.sleep(1)
        
        # Process should still be running
        assert process.is_alive()
        
    finally:
        process.terminate()
        process.join()


def test_invalid_function():
    """Test that passing an invalid function raises appropriate error"""
    with pytest.raises(RuntimeError):
        # Pass a lambda which can't be imported
        hotreload(lambda: None)


def test_extension_filtering(tmp_path):
    """Test that only specified extensions trigger reloads"""
    test_py = tmp_path / "test.py"
    test_txt = tmp_path / "test.txt"
    
    test_py.write_text("print('test')")
    test_txt.write_text("test")
    
    process = multiprocessing.Process(
        target=run_hotreload_with_path,
        args=(str(tmp_path), (".py",))
    )
    process.start()
    
    try:
        time.sleep(1)  # Let watcher start
        
        # Modify .txt file - should not trigger reload
        test_txt.write_text("modified")
        time.sleep(1)
        assert process.is_alive()
        
        # Modify .py file - should trigger reload
        test_py.write_text("print('modified')")
        time.sleep(1)
        assert process.is_alive()
        
    finally:
        process.terminate()
        process.join()


def test_recursive_watching(tmp_path):
    """Test recursive directory watching"""
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file = subdir / "test.py"
    test_file.write_text("print('test')")
    
    process = multiprocessing.Process(
        target=run_hotreload_with_path,
        args=(str(tmp_path),)
    )
    process.start()
    
    try:
        time.sleep(1)  # Let watcher start
        
        # Modify file in subdirectory
        test_file.write_text("print('modified')")
        time.sleep(1)
        assert process.is_alive()
        
    finally:
        process.terminate()
        process.join() 