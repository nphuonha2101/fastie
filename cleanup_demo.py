#!/usr/bin/env python3
"""
Cleanup script để xóa các files được tạo bởi demo
"""

import os
import shutil
from pathlib import Path

def remove_path(path, description):
    """Remove a file or directory"""
    path_obj = Path(path)
    try:
        if path_obj.exists():
            if path_obj.is_dir():
                shutil.rmtree(path_obj)
                print(f"✅ Removed directory: {path}")
            else:
                path_obj.unlink()
                print(f"✅ Removed file: {path}")
        else:
            print(f"⚠️  Path not found: {path}")
    except Exception as e:
        print(f"❌ Error removing {path}: {e}")

def main():
    """Main cleanup function"""
    print("🧹 FASTIE CLI DEMO CLEANUP")
    print("==========================")
    print("Xóa các files được tạo bởi demo...")
    
    # List of demo files and directories to remove
    cleanup_paths = [
        "app/models/blog.py",
        "app/schemas/requests/blog",
        "app/schemas/responses/blog", 
        "app/repositories/interfaces/blog",
        "app/repositories/implements/blog",
        "app/services/interfaces/blog",
        "app/services/implements/blog",
        "app/api/v1/controllers/blog",
    ]
    
    for path in cleanup_paths:
        remove_path(path, f"Removing {path}")
    
    # Also remove empty parent directories if they exist
    empty_dirs = [
        "app/schemas/requests",
        "app/schemas/responses",
    ]
    
    for dir_path in empty_dirs:
        path_obj = Path(dir_path)
        try:
            if path_obj.exists() and path_obj.is_dir():
                # Only remove if empty
                if not any(path_obj.iterdir()):
                    path_obj.rmdir()
                    print(f"✅ Removed empty directory: {dir_path}")
        except Exception as e:
            # Ignore errors for non-empty directories
            pass
    
    print("\n✅ CLEANUP COMPLETED!")
    print("======================")
    print("Tất cả demo files đã được xóa.")

if __name__ == "__main__":
    main() 