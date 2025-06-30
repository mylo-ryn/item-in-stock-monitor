# ASP Handcuffs Monitor 🔗

A Python-based web scraping tool that continuously monitors the availability of ASP Identifier Ultra Plus Chain Handcuffs color variants and sends email notifications when they come back in stock.

June 2025

## 🔒 **Security Notice**

⚠️ **IMPORTANT**: This project contains sensitive email credentials. Before sharing or publishing:

1. **NEVER commit `config.json`** - It contains your email password
2. **Use `config.example.json`** as a template
3. **Set up your own credentials** before running

### **Safe Setup:**
```bash
# 1. Copy the template
cp config.example.json config.json

# 2. Edit with your credentials
nano config.json

# 3. Verify config.json is in .gitignore
git status  # Should NOT show config.json
```

## 🎯 **What It Monitors**

- **Product**: ASP Identifier Ultra Plus Chain Handcuffs
- **URL**: https://www.handcuffwarehouse.com/asp-identifier-ultra-plus-chain-handcuffs/
- **Colors**: Blue, Gray, Pink, Yellow
- **Price**: $65.60
- **SKU**: ASP5606X

## 🚀 **Quick Start**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings
Edit `config.json` with your email credentials:
```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "your-email@gmail.com"
  }
}
```

### 3. Start the Monitor
```bash
python start_monitor.py
```

## 🔧 **How to Manage the Monitor**

### **Check if Monitor is Running**
```bash
ps aux | grep simple_handcuffs_monitor
```
**Expected Output:**
```
mouse  45116  0.0  0.2  411133632  44576   ??  S    11:11PM   0:00.55 /opt/homebrew/Caskroom/miniconda/base/bin/python /Users/mouse/src/playground/simple_handcuffs_monitor.py
```

### **View Real-time Logs**
```bash
# View main log
tail -f handcuffs_monitor.log

# View error log
tail -f handcuffs_monitor_error.log

# View last 20 lines
tail -20 handcuffs_monitor.log
```

### **Check LaunchAgent Status**
```bash
# List all LaunchAgents
launchctl list | grep handcuffs

# Expected output:
# -       1       com.handcuffs.monitor
```

### **Stop the Monitor**
```bash
# Stop the process
pkill -f simple_handcuffs_monitor.py

# Stop auto-startup (LaunchAgent)
launchctl unload ~/Library/LaunchAgents/com.handcuffs.monitor.plist
```

### **Start the Monitor**
```bash
# Start manually
python simple_handcuffs_monitor.py

# Start with auto-restart (LaunchAgent)
launchctl load ~/Library/LaunchAgents/com.handcuffs.monitor.plist
```

### **Restart the Monitor**
```bash
# Restart LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.handcuffs.monitor.plist
launchctl load ~/Library/LaunchAgents/com.handcuffs.monitor.plist
```

## 🛑 **How to Stop the Monitor**

### **When You're Done Monitoring**
Use these commands when you no longer need the monitor (e.g., after getting your handcuffs).

### **Option 1: Interactive Cleanup (Recommended)**
```bash
python stop_monitor.py
```
This will:
- ✅ Check what's currently running
- ✅ Ask for confirmation before stopping
- ✅ Stop the monitor process
- ✅ Remove the LaunchAgent (auto-startup)
- ✅ Clean up log files
- ✅ Show you what files remain
- ✅ Verify everything is stopped

### **Option 2: Quick Stop**
```bash
./quick_stop.sh
```
This will:
- ✅ Stop everything immediately
- ✅ Remove LaunchAgent and log files
- ✅ No confirmation prompts (fast)

### **Manual Stop Commands**
```bash
# Stop the process only
pkill -f simple_handcuffs_monitor.py

# Stop auto-startup (LaunchAgent)
launchctl unload ~/Library/LaunchAgents/com.handcuffs.monitor.plist

# Remove LaunchAgent file
rm ~/Library/LaunchAgents/com.handcuffs.monitor.plist

# Clean up log files
rm handcuffs_monitor.log handcuffs_monitor_error.log previous_status.json
```

### **What Gets Removed During Cleanup**

**Stopped:**
- Monitor process
- LaunchAgent (auto-startup)

**Deleted:**
- `handcuffs_monitor.log`
- `handcuffs_monitor_error.log`
- `previous_status.json`
- `com.handcuffs.monitor.plist`

**Remains (can delete manually):**
- `simple_handcuffs_monitor.py`
- `config.json`
- `requirements.txt`
- `start_monitor.py`
- `stop_monitor.py`
- `README.md`

### **Complete Removal**
To remove everything including the source files:
```bash
# After running stop_monitor.py or quick_stop.sh
rm simple_handcuffs_monitor.py config.json requirements.txt start_monitor.py stop_monitor.py README.md quick_stop.sh
```

## 📊 **Monitor Configuration**

### **Check Interval**
- **Default**: Every 168 hours (1 week)
- **Configurable**: Edit `config.json` → `schedule.interval_hours`

### **Email Notifications**
- **Trigger**: When ANY color variant becomes available
- **Content**: Product URL, status, timestamp
- **Recipient**: Configured in `config.json`

### **Log Files**
- **Main Log**: `handcuffs_monitor.log` - All activity
- **Error Log**: `handcuffs_monitor_error.log` - Errors only

## 🔍 **Troubleshooting**

### **Monitor Not Starting**
```bash
# Check error log
cat handcuffs_monitor_error.log

# Common issues:
# 1. Missing dependencies - run: pip install -r requirements.txt
# 2. Wrong Python path - check: which python
# 3. Email config issues - verify config.json
```

### **No Email Notifications**
1. **Check Gmail App Password**: Make sure you're using an App Password, not your regular password
2. **Enable 2FA**: Two-factor authentication must be enabled on your Google Account
3. **Test Email**: Run `python setup_handcuffs.py` and test email configuration

### **Monitor Stops Unexpectedly**
```bash
# Check if LaunchAgent is still loaded
launchctl list | grep handcuffs

# Restart if needed
launchctl unload ~/Library/LaunchAgents/com.handcuffs.monitor.plist
launchctl load ~/Library/LaunchAgents/com.handcuffs.monitor.plist
```

### **Check Website Status Manually**
```bash
# Test the monitor logic
python simple_handcuffs_monitor.py
```

## 📁 **File Structure**

```
playground/
├── simple_handcuffs_monitor.py    # Main monitor script
├── config.json                    # Configuration file
├── requirements.txt               # Python dependencies
├── start_monitor.py               # Setup/management script
├── com.handcuffs.monitor.plist    # LaunchAgent configuration
├── handcuffs_monitor.log          # Main activity log
├── handcuffs_monitor_error.log    # Error log
└── previous_status.json           # Stock status history
```

## 🔄 **How It Works**

1. **Web Scraping**: Uses `requests` and `BeautifulSoup` to check the product page
2. **Stock Detection**: Parses BigCommerce's `BCData` JavaScript object for `available_modifier_values`
3. **Status Tracking**: Compares current status with previous checks
4. **Email Alerts**: Sends notifications when stock status changes from unavailable to available
5. **Auto-restart**: LaunchAgent ensures the monitor keeps running

## 🛠 **Advanced Configuration**

### **Change Check Interval**
Edit `config.json`:
```json
{
  "schedule": {
    "interval_hours": 24,  // Check daily instead of weekly
    "check_time": "09:00"
  }
}
```

### **Add More Items**
Edit `config.json`:
```json
{
  "items": [
    {
      "name": "ASP Identifier Ultra Plus Chain Handcuffs - Pink",
      "url": "https://www.handcuffwarehouse.com/asp-identifier-ultra-plus-chain-handcuffs/",
      "selectors": {
        "out_of_stock": ".out-of-stock, .sold-out",
        "in_stock": ".add-to-cart, .buy-now"
      }
    }
    // Add more items here...
  ]
}
```

### **Custom Email Templates**
Edit the `send_notification` method in `simple_handcuffs_monitor.py` to customize email content.

## 🚨 **Security Notes**

- **App Passwords**: Use Gmail App Passwords, not your regular password
- **File Permissions**: Keep `config.json` secure (contains email credentials)
- **Log Files**: May contain sensitive information - secure appropriately

## 📞 **Support**

If you encounter issues:
1. Check the error log: `cat handcuffs_monitor_error.log`
2. Verify dependencies: `pip list | grep -E "(requests|beautifulsoup4|schedule)"`
3. Test manually: `python simple_handcuffs_monitor.py`

## 📝 **Changelog**

- **v1.0**: Initial release with BigCommerce parsing
- **v1.1**: Added LaunchAgent for auto-startup
- **v1.2**: Improved error handling and logging
- **v1.3**: Enhanced stock detection logic

---

**Happy Monitoring!** 🎉 