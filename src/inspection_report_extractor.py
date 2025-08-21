#!/usr/bin/env python3
"""
Inspection Report Extractor - Headless Version
==============================================

This script specifically focuses on clicking "View full report" 
and extracting the complete inspection information that appears.
Running headless to avoid PowerShell display issues.

Author: AI Assistant
Version: 1.1 - Headless extraction
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright


async def extract_inspection_report(url: str):
    """Extract complete inspection report by clicking 'View full report'"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Running headless
        page = await browser.new_page()
        
        try:
            print(f"🔄 Loading page: {url}")
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(5000)
            
            print("🔍 Looking for 'View full report' button...")
            
            # Try multiple selectors for the "View full report" button
            button_selectors = [
                'button:has-text("View full report")',
                '*:has-text("View full report")',
                'button[aria-label*="report"]',
                '.view-report',
                'button:text("View full report")',
                '[aria-label="view-full-report-button"]'
            ]
            
            button_found = False
            for selector in button_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button:
                        print(f"✅ Found button with selector: {selector}")
                        
                        # Click the button
                        await button.click()
                        print("🖱️ Clicked 'View full report' button")
                        
                        # Wait for modal/content to load
                        await page.wait_for_timeout(5000)
                        
                        button_found = True
                        break
                        
                except Exception as e:
                    print(f"   ❌ Selector {selector} failed: {e}")
                    continue
            
            if not button_found:
                print("❌ Could not find 'View full report' button")
                # Still continue to extract what we can
            
            print("📋 Extracting inspection report content...")
            
            # Look for inspection content that appeared after clicking
            inspection_data = {}
            
            # Try to find modal or expanded content
            content_selectors = [
                '.modal-content',
                '.inspection-modal',
                '.report-content',
                '.inspection-details',
                '[role="dialog"]',
                '.inspection-report',
                '.modal',
                '.popup'
            ]
            
            for selector in content_selectors:
                try:
                    modal = await page.query_selector(selector)
                    if modal:
                        content = await modal.inner_text()
                        if content and len(content) > 10:
                            inspection_data[f'content_{selector}'] = content
                            print(f"✅ Found content with {selector}: {len(content)} chars")
                except:
                    continue
            
            # Extract all text content and look for inspection details
            try:
                body_content = await page.query_selector('body')
                if body_content:
                    full_text = await body_content.inner_text()
                    
                    # Look for inspection-related sections
                    lines = full_text.split('\n')
                    inspection_sections = {}
                    current_section = None
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Check if this line is a section header
                        if line.lower() in ['exterior', 'engine', 'electricals', 'suspension', 'interior']:
                            current_section = line.lower()
                            inspection_sections[current_section] = []
                        elif current_section and len(line) > 5:
                            # Add content to current section
                            inspection_sections[current_section].append(line)
                    
                    if inspection_sections:
                        inspection_data['sections'] = inspection_sections
                        print(f"✅ Found {len(inspection_sections)} inspection sections")
                    
                    # Also look for specific inspection keywords and capture context
                    inspection_keywords = ['excellent', 'good', 'fair', 'poor', 'condition', 'tested', 'working', 'functional']
                    inspection_lines = []
                    
                    for i, line in enumerate(lines):
                        line = line.strip()
                        if any(keyword in line.lower() for keyword in inspection_keywords):
                            # Capture context around this line
                            start = max(0, i-2)
                            end = min(len(lines), i+3)
                            context = [lines[j].strip() for j in range(start, end) if lines[j].strip()]
                            inspection_lines.extend(context)
                    
                    if inspection_lines:
                        inspection_data['keyword_context'] = list(set(inspection_lines))  # Remove duplicates
                        print(f"✅ Found {len(inspection_lines)} lines with inspection keywords")
                    
            except Exception as e:
                print(f"❌ Error extracting text: {e}")
            
            # Get page HTML to check if modal content is in DOM
            try:
                html_content = await page.content()
                
                # Look for inspection-related content in HTML
                import re
                inspection_patterns = [
                    r'inspection[^>]*>([^<]+)',
                    r'exterior[^>]*>([^<]+)',
                    r'engine[^>]*>([^<]+)',
                    r'electrical[^>]*>([^<]+)',
                    r'suspension[^>]*>([^<]+)'
                ]
                
                html_inspection_data = {}
                for pattern in inspection_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    if matches:
                        html_inspection_data[pattern] = matches
                
                if html_inspection_data:
                    inspection_data['html_patterns'] = html_inspection_data
                    print(f"✅ Found inspection patterns in HTML")
                    
            except Exception as e:
                print(f"❌ Error analyzing HTML: {e}")
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'button_found': button_found,
                'inspection_data': inspection_data,
                'data_sections': len(inspection_data),
                'extraction_method': 'Playwright headless'
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {'error': str(e)}
            
        finally:
            await browser.close()


async def main():
    """Main execution"""
    print("🎯 Inspection Report Extractor (Headless)")
    print("=" * 45)
    
    url = "https://albacars.ae/buy-used-cars/vehicle/10194-volvo-xc40"
    
    result = await extract_inspection_report(url)
    
    if result:
        # Save results
        with open('inspection_extraction_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n📊 Extraction Results:")
        print(f"   Button found: {result.get('button_found', False)}")
        print(f"   Data sections: {result.get('data_sections', 0)}")
        print(f"   Saved to: inspection_extraction_result.json")
        
        if 'inspection_data' in result and result['inspection_data']:
            print(f"\n🔍 Found inspection data:")
            for key, value in result['inspection_data'].items():
                if isinstance(value, list):
                    print(f"   • {key}: {len(value)} items")
                    for item in value[:2]:  # Show first 2
                        print(f"     - {item[:80]}...")
                elif isinstance(value, dict):
                    print(f"   • {key}: {len(value)} sections")
                    for subkey in list(value.keys())[:3]:
                        print(f"     - {subkey}")
                elif isinstance(value, str) and len(value) > 0:
                    print(f"   • {key}: {value[:100]}...")
        else:
            print("❌ No inspection data found")


if __name__ == "__main__":
    asyncio.run(main()) 