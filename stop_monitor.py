#!/usr/bin/env python3
"""
Cleanup script for ASP Handcuffs Monitor
Use this when you no longer need the monitor (e.g., after getting your handcuffs)
"""

import os
import subprocess
import sys
import shutil

def check_monitor_status():
    """Check if the monitor is currently running."""
    print("🔍 Checking monitor status...")
    
    # Check if process is running
    result = subprocess.run("pgrep -f simple_handcuffs_monitor.py", shell=True, capture_output=True)
    if result.returncode == 0:
        pids = result.stdout.decode().strip().split('\n')
        print(f"✅ Monitor is running (PID: {', '.join(pids)})")
        return True
    else:
        print("❌ Monitor is not currently running")
        return False

def check_launchagent_status():
    """Check if LaunchAgent is loaded."""
    print("🔍 Checking LaunchAgent status...")
    
    result = subprocess.run("launchctl list | grep handcuffs", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✅ LaunchAgent is loaded")
        return True
    else:
        print("❌ LaunchAgent is not loaded")
        return False

def stop_monitor():
    """Stop the monitor process."""
    print("🛑 Stopping monitor process...")
    
    result = subprocess.run("pkill -f simple_handcuffs_monitor.py", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✅ Monitor process stopped")
    else:
        print("ℹ️ No monitor process was running")

def unload_launchagent():
    """Unload the LaunchAgent."""
    print("🛑 Unloading LaunchAgent...")
    
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.handcuffs.monitor.plist")
    
    try:
        subprocess.run(f"launchctl unload {plist_path}", shell=True, check=True)
        print("✅ LaunchAgent unloaded")
        return True
    except subprocess.CalledProcessError:
        print("ℹ️ LaunchAgent was not loaded")
        return False

def remove_launchagent_file():
    """Remove the LaunchAgent plist file."""
    print("🗑️ Removing LaunchAgent file...")
    
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.handcuffs.monitor.plist")
    
    if os.path.exists(plist_path):
        try:
            os.remove(plist_path)
            print("✅ LaunchAgent file removed")
            return True
        except Exception as e:
            print(f"❌ Error removing LaunchAgent file: {e}")
            return False
    else:
        print("ℹ️ LaunchAgent file not found")
        return False

def cleanup_files():
    """Remove monitor-related files."""
    print("🧹 Cleaning up monitor files...")
    
    files_to_remove = [
        "handcuffs_monitor.log",
        "handcuffs_monitor_error.log", 
        "previous_status.json",
        "com.handcuffs.monitor.plist"
    ]
    
    removed_count = 0
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removed {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file}: {e}")
        else:
            print(f"ℹ️ {file} not found")
    
    return removed_count

def show_remaining_files():
    """Show what files remain after cleanup."""
    print("\n📁 Remaining files in directory:")
    
    monitor_files = [
        "simple_handcuffs_monitor.py",
        "config.json",
        "requirements.txt",
        "start_monitor.py",
        "stop_monitor.py",
        "README.md"
    ]
    
    for file in monitor_files:
        if os.path.exists(file):
            print(f"   📄 {file}")
        else:
            print(f"   ❌ {file} (missing)")

def main():
    """Main cleanup function."""
    print("🔗 ASP Handcuffs Monitor - Cleanup Script")
    print("=" * 50)
    print("This script will completely remove the monitor and all its components.")
    print("Use this when you no longer need the monitor (e.g., after getting your handcuffs).")
    print("=" * 50)
    
    # Check current status
    monitor_running = check_monitor_status()
    launchagent_loaded = check_launchagent_status()
    
    if not monitor_running and not launchagent_loaded:
        print("\nℹ️ Monitor is already stopped and LaunchAgent is not loaded.")
        print("Would you like to clean up the files anyway?")
        choice = input("Clean up files? (y/n): ").strip().lower()
        if choice != 'y':
            print("👋 Cleanup cancelled.")
            return
    
    print("\n⚠️ This will:")
    print("   - Stop the monitor process")
    print("   - Remove the LaunchAgent (auto-startup)")
    print("   - Delete log files and status history")
    print("   - Remove the LaunchAgent configuration file")
    
    choice = input("\nContinue with cleanup? (y/n): ").strip().lower()
    if choice != 'y':
        print("👋 Cleanup cancelled.")
        return
    
    print("\n🔄 Starting cleanup...")
    
    # Stop everything
    stop_monitor()
    unload_launchagent()
    
    # Clean up files
    removed_count = cleanup_files()
    
    # Show results
    print(f"\n✅ Cleanup complete!")
    print(f"   - Removed {removed_count} files")
    
    # Verify cleanup
    print("\n🔍 Verifying cleanup...")
    monitor_running = check_monitor_status()
    launchagent_loaded = check_launchagent_status()
    
    if not monitor_running and not launchagent_loaded:
        print("✅ Cleanup successful! Monitor is completely stopped.")
    else:
        print("⚠️ Some components may still be running. Check manually.")
    
    # Show remaining files
    show_remaining_files()
    
    print("\n🎉 Monitor cleanup complete!")
    print("📄 The following files remain (you can delete them manually if desired):")
    print("   - simple_handcuffs_monitor.py (main script)")
    print("   - config.json (email configuration)")
    print("   - requirements.txt (dependencies)")
    print("   - start_monitor.py (setup script)")
    print("   - stop_monitor.py (this cleanup script)")
    print("   - README.md (documentation)")
    
    print("\n💡 To completely remove everything, you can:")
    print("   rm simple_handcuffs_monitor.py config.json requirements.txt start_monitor.py stop_monitor.py README.md")

if __name__ == "__main__":
    main() 