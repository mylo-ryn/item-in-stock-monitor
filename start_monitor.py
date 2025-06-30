#!/usr/bin/env python3
"""
Setup script for running the ASP Handcuffs Monitor continuously
"""

import os
import subprocess
import sys

def run_background():
    """Run monitor in background using nohup."""
    print("🔄 Starting monitor in background...")
    cmd = "nohup python simple_handcuffs_monitor.py > handcuffs_monitor.log 2>&1 &"
    subprocess.run(cmd, shell=True)
    print("✅ Monitor started in background!")
    print("📋 Log file: handcuffs_monitor.log")
    print("🛑 To stop: pkill -f simple_handcuffs_monitor.py")

def setup_launchagent():
    """Set up LaunchAgent for automatic startup."""
    print("🚀 Setting up LaunchAgent for automatic startup...")
    
    # Copy plist to LaunchAgents directory
    plist_source = "com.handcuffs.monitor.plist"
    plist_dest = os.path.expanduser("~/Library/LaunchAgents/com.handcuffs.monitor.plist")
    
    try:
        # Copy the plist file
        subprocess.run(f"cp {plist_source} {plist_dest}", shell=True, check=True)
        print(f"✅ Copied plist to {plist_dest}")
        
        # Load the LaunchAgent
        subprocess.run(f"launchctl load {plist_dest}", shell=True, check=True)
        print("✅ LaunchAgent loaded successfully!")
        
        print("\n🎉 Monitor will now:")
        print("   - Start automatically when you log in")
        print("   - Restart automatically if it crashes")
        print("   - Run in the background")
        print("   - Log to handcuffs_monitor.log")
        
        print("\n🛑 To stop automatic startup:")
        print(f"   launchctl unload {plist_dest}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up LaunchAgent: {e}")
        return False
    
    return True

def show_status():
    """Show current monitor status."""
    print("📊 Checking monitor status...")
    
    # Check if process is running
    result = subprocess.run("pgrep -f simple_handcuffs_monitor.py", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✅ Monitor is currently running")
        pids = result.stdout.decode().strip().split('\n')
        for pid in pids:
            if pid:
                print(f"   Process ID: {pid}")
    else:
        print("❌ Monitor is not currently running")
    
    # Check log file
    if os.path.exists("handcuffs_monitor.log"):
        print("📋 Log file exists: handcuffs_monitor.log")
        # Show last few lines
        try:
            with open("handcuffs_monitor.log", "r") as f:
                lines = f.readlines()
                if lines:
                    print("📝 Last log entries:")
                    for line in lines[-5:]:
                        print(f"   {line.strip()}")
        except:
            pass
    else:
        print("📋 No log file found")

def main():
    """Main setup function."""
    print("🔗 ASP Handcuffs Monitor - Continuous Setup")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Run in background (nohup)")
        print("2. Set up automatic startup (LaunchAgent)")
        print("3. Check current status")
        print("4. Stop monitor")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            run_background()
        elif choice == "2":
            setup_launchagent()
        elif choice == "3":
            show_status()
        elif choice == "4":
            print("🛑 Stopping monitor...")
            subprocess.run("pkill -f simple_handcuffs_monitor.py", shell=True)
            print("✅ Monitor stopped")
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main() 