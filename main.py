#!/usr/bin/env python3
"""
Alba Cars Scraper Suite - Main Entry Point
==========================================

This script provides a user-friendly interface to run different scrapers
based on your specific needs.

Author: AI Assistant
Version: 2.0.0 - Refactored Architecture
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("🚗 Alba Cars UAE Scraper Suite v2.0.0")
    print("=" * 60)
    print("Choose your extraction method:\n")

def print_menu():
    """Print the main menu options"""
    print("1. 🔥 Firecrawl Scraper        - Fast structured data extraction")
    print("2. 🖼️  Image Extractor         - Carousel navigation + images")
    print("3. 🎯 Comprehensive Scraper    - Complete data + images")
    print("4. 📋 Inspection Extractor     - Detailed inspection reports")
    print("5. 🚀 Extract First 10 Cars   - Automated batch extraction")
    print("6. 🛠️  Utility Tools           - Data processing utilities")
    print("7. ❓ Help                     - Show detailed information")
    print("0. 🚪 Exit")
    print("\n" + "-" * 60)

def show_help():
    """Show detailed help information"""
    print("\n📖 DETAILED INFORMATION:\n")
    
    print("🔥 FIRECRAWL SCRAPER:")
    print("   • Best for: Quick structured data extraction")
    print("   • Speed: Fast")
    print("   • Data: Vehicle specs, pricing, basic features")
    print("   • File: src/alba_cars_scraper.py\n")
    
    print("🖼️ IMAGE EXTRACTOR:")
    print("   • Best for: Getting all vehicle images")
    print("   • Speed: Moderate")
    print("   • Data: Real CloudFront image URLs")
    print("   • File: src/fixed_playwright_scraper.py\n")
    
    print("🎯 COMPREHENSIVE SCRAPER:")
    print("   • Best for: Complete vehicle profiles")
    print("   • Speed: Slower but thorough")
    print("   • Data: Everything combined")
    print("   • File: src/playwright_comprehensive_scraper.py\n")
    
    print("📋 INSPECTION EXTRACTOR:")
    print("   • Best for: Detailed inspection reports")
    print("   • Speed: Targeted")
    print("   • Data: Modal-based inspection details")
    print("   • File: src/inspection_report_extractor.py\n")
    
    print("🛠️ UTILITY TOOLS:")
    print("   • Image URL cleaner")
    print("   • Database assembly tools")
    print("   • Data processing utilities")
    print("   • Location: utils/ directory\n")

def run_firecrawl_scraper():
    """Run the Firecrawl-based scraper"""
    print("\n🔥 Starting Firecrawl Scraper...")
    print("Note: This requires Firecrawl MCP tools to be available")
    
    try:
        from alba_cars_scraper import AlbaCarsScraper
        
        print("✅ Initializing scraper...")
        scraper = AlbaCarsScraper()
        
        # Get sample URLs (in production, this would fetch from listing page)
        urls = scraper.get_vehicle_urls_from_listing()
        
        if urls:
            print(f"📝 Found {len(urls)} vehicle URLs")
            vehicles = scraper.scrape_multiple_vehicles(urls)
            
            if vehicles:
                scraper.save_database()
                print(f"✅ Successfully scraped {len(vehicles)} vehicles!")
                print(f"💾 Data saved to data/vehicles_database.json")
            else:
                print("❌ No vehicles were successfully scraped")
        else:
            print("❌ No vehicle URLs found")
            
    except ImportError as e:
        print(f"❌ Error importing scraper: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error running scraper: {e}")

def run_image_extractor():
    """Run the Playwright image extractor"""
    print("\n🖼️ Starting Image Extractor...")
    print("Note: This requires Playwright to be installed")
    
    try:
        import asyncio
        from fixed_playwright_scraper import extract_real_vehicle_data
        
        # Sample URL for demonstration
        url = "https://albacars.ae/buy-used-cars/vehicle/9667-bmw-x2-xdrive-20i"
        
        print(f"🔄 Extracting images from: {url}")
        
        # Run the async function
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(extract_real_vehicle_data(url))
        
        if result:
            print("✅ Image extraction completed!")
            print(f"💾 Check logs/ directory for detailed results")
        else:
            print("❌ Image extraction failed")
            
    except ImportError as e:
        print(f"❌ Error importing Playwright: {e}")
        print("💡 Install Playwright: pip install playwright && playwright install chromium")
    except Exception as e:
        print(f"❌ Error running image extractor: {e}")

def run_comprehensive_scraper():
    """Run the comprehensive Playwright scraper"""
    print("\n🎯 Starting Comprehensive Scraper...")
    
    try:
        import asyncio
        from playwright_comprehensive_scraper import extract_all_vehicle_data
        
        url = "https://albacars.ae/buy-used-cars/vehicle/9667-bmw-x2-xdrive-20i"
        
        print(f"🔄 Extracting comprehensive data from: {url}")
        
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(extract_all_vehicle_data(url))
        
        if result:
            print("✅ Comprehensive extraction completed!")
            print(f"💾 Check data/ directory for results")
        else:
            print("❌ Comprehensive extraction failed")
            
    except ImportError as e:
        print(f"❌ Error importing dependencies: {e}")
    except Exception as e:
        print(f"❌ Error running comprehensive scraper: {e}")

def run_inspection_extractor():
    """Run the inspection report extractor"""
    print("\n📋 Starting Inspection Extractor...")
    
    try:
        import asyncio
        from inspection_report_extractor import extract_inspection_report
        
        url = "https://albacars.ae/buy-used-cars/vehicle/9667-bmw-x2-xdrive-20i"
        
        print(f"🔄 Extracting inspection report from: {url}")
        
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(extract_inspection_report(url))
        
        if result:
            print("✅ Inspection extraction completed!")
            print(f"💾 Check data/ directory for inspection results")
        else:
            print("❌ Inspection extraction failed")
            
    except ImportError as e:
        print(f"❌ Error importing dependencies: {e}")
    except Exception as e:
        print(f"❌ Error running inspection extractor: {e}")

def run_first_10_extractor():
    """Run the automated first 10 cars extractor"""
    print("\n🚀 Starting First 10 Cars Batch Extractor...")
    print("This will extract complete data for the first 10 cars from Alba Cars UAE")
    
    confirm = input("\nThis may take 5-8 minutes. Continue? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Extraction cancelled")
        return
    
    try:
        import subprocess
        import sys
        
        print("\n🔄 Running automated extraction script...")
        
        # Run the extraction script
        result = subprocess.run([
            sys.executable, 
            "src/scripts/extract_first_10_cars.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Batch extraction completed successfully!")
            print(f"💾 Check data/first_10_cars_complete_database.json for results")
            if result.stdout:
                print("\n📋 Extraction Summary:")
                print(result.stdout.split("🎉 EXTRACTION COMPLETE!")[-1] if "🎉 EXTRACTION COMPLETE!" in result.stdout else result.stdout[-500:])
        else:
            print("❌ Batch extraction failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
                
    except Exception as e:
        print(f"❌ Error running batch extractor: {e}")
        print("💡 Try running manually: python3 extract_first_10_cars.py")

def show_utility_tools():
    """Show available utility tools"""
    print("\n🛠️ UTILITY TOOLS:\n")
    
    print("Available utilities in utils/ directory:")
    print("• extract_all_images.py     - Clean CloudFront image URLs")
    print("• create_final_real_database.py - Combine data from multiple sources")
    print("• final_complete_database.py     - Final data processing pipeline")
    
    print("\n💡 Run utilities directly:")
    print("   python3 utils/extract_all_images.py")
    print("   python3 utils/create_final_real_database.py")
    print("   python3 utils/final_complete_database.py")

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ["data", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def main():
    """Main application loop"""
    setup_directories()
    
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input("Select an option (0-7): ").strip()
            
            if choice == "0":
                print("\n👋 Thanks for using Alba Cars Scraper Suite!")
                break
            elif choice == "1":
                run_firecrawl_scraper()
            elif choice == "2":
                run_image_extractor()
            elif choice == "3":
                run_comprehensive_scraper()
            elif choice == "4":
                run_inspection_extractor()
            elif choice == "5":
                run_first_10_extractor()
            elif choice == "6":
                show_utility_tools()
            elif choice == "7":
                show_help()
            else:
                print("\n❌ Invalid option. Please choose 0-7.")
            
            if choice != "0":
                input("\n📱 Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("\n📱 Press Enter to continue...")

if __name__ == "__main__":
    main() 