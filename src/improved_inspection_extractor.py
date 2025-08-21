#!/usr/bin/env python3
"""
Improved Inspection Report Extractor
====================================

This script properly structures inspection data with key-value relationships
instead of flat lists, making it easier for LLMs to process.

Author: AI Assistant
Version: 2.0.0 - Structured Data Extraction
"""

import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright
from typing import Dict, List, Any


class StructuredInspectionExtractor:
    """Extract inspection reports with proper data structure"""
    
    def __init__(self):
        self.status_keywords = ['passed', 'failed', 'good', 'excellent', 'poor', 'fair', 'warning', 'attention']
        self.section_headers = ['exterior', 'engine', 'electricals', 'suspension', 'interior', 'mechanical']
    
    def parse_inspection_text(self, text_lines: List[str]) -> Dict[str, Any]:
        """Parse inspection text into structured data"""
        structured_data = {}
        current_section = None
        current_category = None
        i = 0
        
        while i < len(text_lines):
            line = text_lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Check if this is a section header
            if line.lower() in self.section_headers:
                current_section = line.lower()
                structured_data[current_section] = {}
                current_category = None
                i += 1
                continue
            
            # Check if this is a category header (ends with "condition", "conditions", etc.)
            if (line.lower().endswith(('condition', 'conditions', 'assessment', 'check')) and 
                not any(status in line.lower() for status in self.status_keywords)):
                current_category = line
                if current_section:
                    structured_data[current_section][current_category] = {}
                i += 1
                continue
            
            # Check if this is an item-value pair
            if current_section and current_category and i + 1 < len(text_lines):
                next_line = text_lines[i + 1].strip()
                
                # If next line looks like a status/condition
                if any(status in next_line.lower() for status in self.status_keywords):
                    structured_data[current_section][current_category][line] = next_line
                    i += 2  # Skip both lines
                    continue
            
            # Check for direct key-value patterns in the same line
            if ':' in line and current_section:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if current_category:
                        structured_data[current_section][current_category][key] = value
                    else:
                        # Create a general category for direct items
                        if 'general' not in structured_data[current_section]:
                            structured_data[current_section]['general'] = {}
                        structured_data[current_section]['general'][key] = value
            
            i += 1
        
        return structured_data
    
    def extract_pricing_info(self, text_lines: List[str]) -> Dict[str, str]:
        """Extract pricing and financial information"""
        pricing_data = {}
        
        for i, line in enumerate(text_lines):
            line = line.strip()
            
            # Look for pricing patterns
            if 'starts from' in line.lower() and i + 1 < len(text_lines):
                next_line = text_lines[i + 1].strip()
                if 'aed' in next_line.lower() or any(char.isdigit() for char in next_line):
                    pricing_data['starts_from'] = next_line
            
            elif 'full price' in line.lower() and i + 1 < len(text_lines):
                next_line = text_lines[i + 1].strip()
                if 'aed' in next_line.lower() or any(char.isdigit() for char in next_line):
                    pricing_data['full_price'] = next_line
            
            elif 'monthly' in line.lower() and 'aed' in line:
                pricing_data['monthly_payment'] = line
            
            elif line.startswith('AED') and any(char.isdigit() for char in line):
                if 'price' not in pricing_data:
                    pricing_data['price'] = line
        
        return pricing_data
    
    def extract_vehicle_specs(self, text_lines: List[str]) -> Dict[str, str]:
        """Extract vehicle specifications"""
        specs = {}
        
        spec_keywords = {
            'year': ['year'],
            'mileage': ['mileage', 'km', 'odometer'],
            'warranty': ['warranty'],
            'service_contract': ['service contract'],
            'spec': ['spec', 'specification'],
            'cylinders': ['cylinders'],
            'engine': ['engine'],
            'fuel_type': ['fuel', 'petrol', 'diesel', 'hybrid'],
            'transmission': ['automatic', 'manual', 'transmission'],
            'color': ['color', 'colour']
        }
        
        for line in text_lines:
            line = line.strip()
            
            for spec_type, keywords in spec_keywords.items():
                if any(keyword in line.lower() for keyword in keywords):
                    if spec_type not in specs:
                        specs[spec_type] = line
        
        return specs

async def extract_structured_inspection_report(url: str) -> Dict[str, Any]:
    """Extract inspection report with proper structure"""
    extractor = StructuredInspectionExtractor()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print(f"🔄 Loading page: {url}")
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(5000)
            
            # Look for and click "View full report" button
            button_found = False
            try:
                print("🔍 Looking for 'View full report' button...")
                button_selector = "button:has-text('View full report')"
                button = await page.query_selector(button_selector)
                
                if button:
                    print(f"✅ Found button with selector: {button_selector}")
                    print("🖱️ Clicking 'View full report' button")
                    await button.click()
                    await page.wait_for_timeout(3000)  # Wait for modal/content to load
                    button_found = True
                else:
                    print("⚠️ 'View full report' button not found")
                    
            except Exception as e:
                print(f"❌ Error clicking button: {e}")
            
            # Extract all text content
            body_content = await page.query_selector('body')
            if not body_content:
                raise Exception("Could not find page body")
            
            full_text = await body_content.inner_text()
            text_lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            print(f"📄 Extracted {len(text_lines)} lines of text")
            
            # Parse structured inspection data
            structured_inspection = extractor.parse_inspection_text(text_lines)
            
            # Extract pricing information
            pricing_info = extractor.extract_pricing_info(text_lines)
            
            # Extract vehicle specifications
            vehicle_specs = extractor.extract_vehicle_specs(text_lines)
            
            # Extract features
            features = []
            for line in text_lines:
                # Look for feature patterns (typically short descriptive phrases)
                if (5 < len(line) < 50 and 
                    not any(char.isdigit() for char in line[:3]) and
                    not line.lower().startswith(('http', 'www', 'tel:', 'mailto:')) and
                    any(keyword in line.lower() for keyword in ['wireless', 'cruise', 'camera', 'sensor', 'seat', 'air', 'navigation', 'bluetooth', 'usb', 'audio', 'climate', 'keyless', 'parking', 'safety'])):
                    if line not in features:
                        features.append(line)
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'button_found': button_found,
                'extraction_method': 'Structured Playwright',
                'data': {
                    'inspection_report': structured_inspection,
                    'pricing_information': pricing_info,
                    'vehicle_specifications': vehicle_specs,
                    'key_features': features[:20],  # Limit to top 20 features
                },
                'data_quality': {
                    'inspection_sections': len(structured_inspection),
                    'pricing_fields': len(pricing_info),
                    'specification_fields': len(vehicle_specs),
                    'features_count': len(features),
                    'total_text_lines': len(text_lines)
                }
            }
            
            print(f"✅ Structured extraction complete!")
            print(f"   📋 Inspection sections: {len(structured_inspection)}")
            print(f"   💰 Pricing fields: {len(pricing_info)}")
            print(f"   🔧 Specification fields: {len(vehicle_specs)}")
            print(f"   ⭐ Features found: {len(features)}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
            
        finally:
            await browser.close()


async def main():
    """Test the structured extraction"""
    print("🎯 Improved Inspection Report Extractor")
    print("=" * 45)
    
    url = "https://albacars.ae/buy-used-cars/vehicle/10194-volvo-xc40"
    
    result = await extract_structured_inspection_report(url)
    
    if result and 'error' not in result:
        # Save results in a more readable format
        output_file = f"data/structured_inspection_sample.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Sample structured extraction saved to: {output_file}")
        
        # Show a sample of the structured data
        if 'data' in result and 'inspection_report' in result['data']:
            print(f"\n📋 Sample Structured Inspection Data:")
            for section, categories in result['data']['inspection_report'].items():
                print(f"\n🔧 {section.upper()}:")
                if isinstance(categories, dict):
                    for category, items in categories.items():
                        print(f"  📝 {category}:")
                        if isinstance(items, dict):
                            for item, status in list(items.items())[:3]:  # Show first 3 items
                                print(f"    • {item}: {status}")
                            if len(items) > 3:
                                print(f"    ... and {len(items) - 3} more items")
        
        if 'data' in result and 'pricing_information' in result['data']:
            pricing = result['data']['pricing_information']
            if pricing:
                print(f"\n💰 Pricing Information:")
                for key, value in pricing.items():
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    else:
        print(f"❌ Extraction failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(main()) 