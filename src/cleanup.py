#!/usr/bin/env python3
"""
Cleanup script to remove redundant UI server files after merge
This script safely removes files that are no longer needed after merging UI and server functionality
"""

import os
import shutil
import sys

def cleanup_redundant_files():
    """Remove redundant files after UI/Server merge"""
    
    print("🧹 AI Voice Assistant - Cleanup Redundant Files")
    print("=" * 50)
    
    # Get the src directory path
    src_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Files and directories to remove
    redundant_items = [
        "ui/",  # Entire UI directory (functionality merged into server/server.py)
    ]
    
    removed_count = 0
    
    for item in redundant_items:
        item_path = os.path.join(src_dir, item)
        
        try:
            if os.path.isfile(item_path):
                print(f"🗑️  Removing redundant file: {item}")
                os.remove(item_path)
                removed_count += 1
            elif os.path.isdir(item_path):
                print(f"🗂️  Removing redundant directory: {item}")
                shutil.rmtree(item_path)
                removed_count += 1
            else:
                print(f"⏭️  Skipping (not found): {item}")
                
        except Exception as e:
            print(f"❌ Error removing {item}: {e}")
    
    print()
    print(f"✅ Cleanup completed! Removed {removed_count} redundant items.")
    print()
    print("📋 Current Architecture:")
    print("   • API Server (5001)    - For Flutter/mobile apps")
    print("   • Unified Server (5000) - Web UI + API functionality")
    print()
    print("🚀 To start the servers:")
    print("   python launcher.py")
    print("   or")
    print("   ./start_servers.ps1")

if __name__ == "__main__":
    try:
        cleanup_redundant_files()
    except KeyboardInterrupt:
        print("\n⚠️  Cleanup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
