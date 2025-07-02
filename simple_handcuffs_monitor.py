#!/usr/bin/env python3
"""
Simple monitor for ASP Identifier Ultra Plus Chain Handcuffs - Pink variant
Uses requests instead of Selenium to avoid ChromeDriver issues
"""

import requests
import schedule
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleHandcuffsMonitor:
    def __init__(self, config_file="config.json"):
        """Initialize the simple handcuffs monitor."""
        self.config_file = config_file
        self.config = self.load_config()
        self.previous_status = {}
        self.load_previous_status()
        
    def load_config(self):
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            print("❌ config.json not found. Please run setup_handcuffs.py first.")
            return None
    
    def load_previous_status(self):
        """Load previous status from file."""
        status_file = "previous_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                self.previous_status = json.load(f)
    
    def save_previous_status(self):
        """Save current status to file."""
        with open("previous_status.json", 'w') as f:
            json.dump(self.previous_status, f, indent=2)
    
    def check_pink_variant_availability(self):
        """Check if the pink variant is available using requests."""
        try:
            print("🔍 Checking ASP Identifier Ultra Plus Chain Handcuffs - Pink availability...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            url = "https://www.handcuffwarehouse.com/asp-identifier-ultra-plus-chain-handcuffs/"
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the BCData JavaScript object which contains stock information
            scripts = soup.find_all('script')
            bcdata_found = False
            available_variants = []
            
            for script in scripts:
                if script.string and 'BCData' in script.string:
                    script_content = script.string
                    print("✅ Found BCData script")
                    
                    # Extract available_modifier_values and available_variant_values
                    if '"available_modifier_values":[' in script_content:
                        # Parse the available modifier values
                        start = script_content.find('"available_modifier_values":[')
                        end = script_content.find(']', start)
                        if end > start:
                            modifier_section = script_content[start:end+1]
                            print(f"📋 Modifier values: {modifier_section}")
                            
                            # Check if there are any available variants
                            if '[]' in modifier_section or 'available_modifier_values":[]' in modifier_section:
                                print("⚠️ No available modifier values found, checking other indicators...")
                                # Don't return False yet, check other indicators
                            else:
                                # Extract the actual values
                                import re
                                values_match = re.search(r'"available_modifier_values":\[(.*?)\]', script_content)
                                if values_match:
                                    values_str = values_match.group(1)
                                    if values_str.strip():
                                        available_variants = [v.strip('"') for v in values_str.split(',') if v.strip()]
                                        print(f"✅ Available variants: {available_variants}")
                                    else:
                                        print("⚠️ No available variants in modifier values, checking other indicators...")
                                else:
                                    print("⚠️ Could not parse modifier values, checking other indicators...")
                    
                    # Also check available_variant_values
                    if '"available_variant_values":[' in script_content:
                        start = script_content.find('"available_variant_values":[')
                        end = script_content.find(']', start)
                        if end > start:
                            variant_section = script_content[start:end+1]
                            print(f"📋 Variant values: {variant_section}")
                            
                            # Check if there are available variants
                            if '[]' not in variant_section:
                                import re
                                values_match = re.search(r'"available_variant_values":\[(.*?)\]', script_content)
                                if values_match:
                                    values_str = values_match.group(1)
                                    if values_str.strip():
                                        available_variants = [v.strip('"') for v in values_str.split(',') if v.strip()]
                                        print(f"✅ Available variants from variant_values: {available_variants}")
                                        return True, f"Color variants are available: {available_variants}"
                    
                    # Show the full BCData for debugging
                    print("🔍 Full BCData excerpt:")
                    bcdata_start = script_content.find('var BCData = {')
                    if bcdata_start != -1:
                        bcdata_end = script_content.find('};', bcdata_start) + 2
                        bcdata_excerpt = script_content[bcdata_start:bcdata_end]
                        print(bcdata_excerpt[:500] + "..." if len(bcdata_excerpt) > 500 else bcdata_excerpt)
                    
                    # Check for positive stock indicators
                    if '"instock":true' in script_content:
                        print("✅ Product shows as in stock")
                        return True, "Product is in stock"
                    
                    # Check for negative stock indicators
                    if '"instock":false' in script_content:
                        print("❌ Product shows as not in stock")
                        return False, "Product is not in stock"
                    
                    # Check purchasing message
                    if '"purchasing_message":"The selected product combination is currently unavailable."' in script_content:
                        print("❌ Product combination unavailable")
                        return False, "Selected product combination is currently unavailable"
                    
                    bcdata_found = True
                    break
            
            if not bcdata_found:
                print("⚠️ BCData not found, falling back to HTML parsing...")
            
            # Fallback: Look for color options in HTML
            color_options = soup.find_all('option', string=lambda text: text and any(color in text.lower() for color in ['blue', 'gray', 'pink', 'yellow']))
            if color_options:
                available_colors = [option.get_text().strip() for option in color_options if option.get_text().strip()]
                print(f"✅ Found color options in HTML: {available_colors}")
                return True, f"Color variants are available: {available_colors}"
            
            # Look for out of stock indicators in HTML
            out_of_stock_indicators = [
                "out of stock",
                "sold out", 
                "unavailable",
                "backorder",
                "preorder",
                "currently unavailable"
            ]
            
            page_text = soup.get_text().lower()
            for indicator in out_of_stock_indicators:
                if indicator in page_text:
                    print(f"❌ Found out of stock indicator: '{indicator}'")
                    return False, f"Product shows as {indicator}"
            
            # If we found available variants, check if any are available
            if available_variants:
                # Any color variant is available - send notification!
                return True, f"Color variants are now available: {available_variants}"
            else:
                return False, "No color variants are currently available"
            
            # If we get here and no variants were found, assume out of stock
            return False, "No color variants are currently available"
                
        except requests.RequestException as e:
            return None, f"Network error: {str(e)}"
        except Exception as e:
            return None, f"Error checking availability: {str(e)}"
    
    def check_item_stock(self):
        """Check stock for the ASP handcuffs."""
        item = self.config["items"][0]  # We're only monitoring one item
        
        print(f"\n{'='*60}")
        print(f"🔗 ASP Handcuffs Stock Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"Item: {item['name']}")
        print(f"URL: {item['url']}")
        
        in_stock, message = self.check_pink_variant_availability()
        
        print(f"Status: {message}")
        
        # Check if status changed
        item_key = f"{item['name']}_{item['url']}"
        previous_status = self.previous_status.get(item_key, None)
        
        if previous_status is None:
            # First time checking
            self.previous_status[item_key] = {
                'in_stock': in_stock,
                'message': message,
                'last_checked': datetime.now().isoformat()
            }
            print(f"📋 First check: {message}")
        elif previous_status['in_stock'] != in_stock:
            # Status changed
            if in_stock:
                self.send_notification(item, "PINK HANDCUFFS BACK IN STOCK!", message)
                print(f"🎉 {item['name']} is back in stock!")
            else:
                print(f"📦 {item['name']} is now out of stock")
            
            self.previous_status[item_key] = {
                'in_stock': in_stock,
                'message': message,
                'last_checked': datetime.now().isoformat()
            }
        else:
            # Status unchanged
            self.previous_status[item_key]['last_checked'] = datetime.now().isoformat()
            print(f"Status unchanged")
        
        self.save_previous_status()
        print(f"{'='*60}\n")
        sys.stdout.flush()
        return in_stock, message
    
    def send_notification(self, item, subject, message):
        """Send email notification."""
        try:
            email_config = self.config['email']
            
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['recipient_email']
            msg['Subject'] = f"🔗 ASP Handcuffs Alert: {subject}"
            
            body = f"""
            🎉 ASP HANDCUFFS COLOR VARIANTS ALERT! 🎉
            
            Item: {item['name']}
            URL: {item['url']}
            Status: {message}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            ASP Identifier Ultra Plus Chain Handcuffs color variants are now available!
            Price: $65.60
            
            🛒 Quick Link: {item['url']}
            
            Check the website to see which colors (Blue, Gray, Pink, Yellow) are in stock!
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            text = msg.as_string()
            server.sendmail(email_config['sender_email'], email_config['recipient_email'], text)
            server.quit()
            
            print(f"📧 Notification sent for {item['name']}")
            
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
    
    def run_scheduler(self):
        """Run the scheduler to check items periodically."""
        if not self.config:
            print("❌ Configuration not found. Please run setup_handcuffs.py first.")
            sys.stdout.flush()
            return
            
        print("🔗 Starting Simple ASP Handcuffs Monitor...")
        print(f"⏰ Checking every {self.config['schedule']['interval_hours']} hours")
        print("Press Ctrl+C to stop")
        sys.stdout.flush()
        
        # Schedule the job
        schedule.every(self.config['schedule']['interval_hours']).hours.do(self.check_item_stock)
        
        # Run initial check
        self.check_item_stock()
        sys.stdout.flush()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function to run the simple handcuffs monitor."""
    monitor = SimpleHandcuffsMonitor()
    
    try:
        monitor.run_scheduler()
    except KeyboardInterrupt:
        print("\n🔗 Simple ASP Handcuffs Monitor stopped by user")
    except Exception as e:
        print(f"Error running monitor: {str(e)}")

if __name__ == "__main__":
    main() 