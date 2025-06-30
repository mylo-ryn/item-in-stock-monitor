#!/bin/bash
# Quick stop script for ASP Handcuffs Monitor
# Run this when you want to stop everything quickly

echo "🔗 ASP Handcuffs Monitor - Quick Stop"
echo "======================================"

# Stop the monitor process
echo "🛑 Stopping monitor process..."
pkill -f simple_handcuffs_monitor.py

# Unload LaunchAgent
echo "🛑 Unloading LaunchAgent..."
launchctl unload ~/Library/LaunchAgents/com.handcuffs.monitor.plist 2>/dev/null

# Remove LaunchAgent file
echo "🗑️ Removing LaunchAgent file..."
rm -f ~/Library/LaunchAgents/com.handcuffs.monitor.plist

# Clean up log files
echo "🧹 Cleaning up log files..."
rm -f handcuffs_monitor.log handcuffs_monitor_error.log previous_status.json

echo "✅ Quick stop complete!"
echo "📄 Monitor files remain (delete manually if desired):"
echo "   - simple_handcuffs_monitor.py"
echo "   - config.json"
echo "   - requirements.txt"
echo "   - start_monitor.py"
echo "   - stop_monitor.py"
echo "   - README.md" 