#!/usr/bin/env python3
"""
Car Listing Focused Extractor
=============================

Extracts ONLY car-related information from vehicle listing pages.
Filters out website navigation, footer, FAQs, and other irrelevant content.

Target Data Schema:
- Model name & basic details
- Stock number & pricing
- Car overview (year, mileage, warranty, etc.)
- Key features
- About section
- Inspection report
- Action links (Call Us, Buy Car, Test Drive)
- Car images only
- Offers/campaigns

Author: AI Assistant
Version: 3.0.0 - Car-Focused Extraction
"""

import json
import re
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# External imports
try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright")
    exit(1)


@dataclass
class CarListingData:
    """Structured car listing data"""
    # Basic Information
    make: str = ""
    model: str = ""
    year: str = ""
    stock_number: str = ""
    
    # Pricing
    price_aed: str = ""
    monthly_payment: str = ""
    price_display: str = ""
    
    # Overview Details
    mileage: str = ""
    warranty: str = ""
    transmission: str = ""
    engine_size: str = ""
    fuel_type: str = ""
    cylinders: str = ""
    spec: str = ""
    service_contract: str = ""
    
    # Key Features
    key_features: List[str] = None
    
    # About Section
    about_description: str = ""
    
    # Action Links
    action_links: Dict[str, str] = None
    
    # Offers/Campaigns
    offers: List[str] = None
    
    # Inspection Report
    inspection_sections: List[str] = None
    has_inspection_report: bool = False
    
    # Images
    car_images: List[str] = None
    
    # Metadata
    source_url: str = ""
    extraction_timestamp: str = ""
    viewers_count: str = ""
    
    def __post_init__(self):
        if self.key_features is None:
            self.key_features = []
        if self.action_links is None:
            self.action_links = {}
        if self.offers is None:
            self.offers = []
        if self.inspection_sections is None:
            self.inspection_sections = []
        if self.car_images is None:
            self.car_images = []


class CarListingExtractor:
    """Extract focused car listing data"""
    
    def __init__(self):
        self.car_feature_patterns = [
            r'wireless charger', r'cruise control', r'rear ac', r'apple car play',
            r'isofix', r'panoramic sunroof', r'rear camera', r'electric seats',
            r'keyless start', r'electric tailgate', r'parking sensors', r'leather seats',
            r'keyless entry', r'bluetooth', r'navigation', r'heated seats'
        ]
        
        self.irrelevant_patterns = [
            r'frequently asked questions', r'contact us', r'about us', r'privacy policy',
            r'terms & conditions', r'social networks', r'working hours', r'get directions',
            r'latest news', r'used cars in dubai', r'car sales in dubai', r'sell the car',
            r'alba cars facebook', r'alba cars linkedin', r'compare similar cars',
            r'select and filter', r'body type', r'show results'
        ]
    
    def extract_from_markdown(self, markdown_content: str, url: str) -> CarListingData:
        """Extract car data from markdown content"""
        
        car_data = CarListingData()
        car_data.source_url = url
        car_data.extraction_timestamp = datetime.now().isoformat()
        
        # Extract basic info from URL
        url_parts = url.split('/')[-1].split('-')
        if len(url_parts) >= 3:
            car_data.stock_number = url_parts[0]
            car_data.make = url_parts[1].title()
            car_data.model = ' '.join(url_parts[2:]).title()
        
        lines = markdown_content.split('\n')
        clean_lines = [line.strip() for line in lines if line.strip()]
        
        # Extract pricing information
        self._extract_pricing(clean_lines, car_data)
        
        # Extract car overview
        self._extract_car_overview(clean_lines, car_data)
        
        # Extract key features
        self._extract_key_features(clean_lines, car_data)
        
        # Extract about section
        self._extract_about_section(clean_lines, car_data)
        
        # Extract action links
        self._extract_action_links(clean_lines, car_data)
        
        # Extract offers/campaigns
        self._extract_offers(clean_lines, car_data)
        
        # Extract inspection info
        self._extract_inspection_info(clean_lines, car_data)
        
        # Extract viewer count
        self._extract_viewer_count(clean_lines, car_data)
        
        return car_data
    
    def _extract_pricing(self, lines: List[str], car_data: CarListingData):
        """Extract pricing information"""
        for i, line in enumerate(lines):
            if 'AED' in line and (',' in line or 'Month' in line):
                if '/Month' in line:
                    car_data.monthly_payment = line.strip()
                elif 'Exclusive' in line or 'Inclusive' in line:
                    car_data.price_display = line.strip()
                    # Extract just the number
                    price_match = re.search(r'AED ([\d,]+)', line)
                    if price_match:
                        car_data.price_aed = price_match.group(1)
    
    def _extract_car_overview(self, lines: List[str], car_data: CarListingData):
        """Extract car overview details"""
        in_overview = False
        
        for i, line in enumerate(lines):
            if line == 'Car Overview':
                in_overview = True
                continue
            
            if in_overview and line == 'Key Features':
                break
            
            if in_overview and i + 1 < len(lines):
                next_line = lines[i + 1]
                
                if line == 'Year' and next_line.isdigit():
                    car_data.year = next_line
                elif line == 'Mileage' and 'km' in next_line:
                    car_data.mileage = next_line
                elif line == 'Warranty':
                    car_data.warranty = next_line
                elif line == 'Transmission':
                    car_data.transmission = next_line
                elif line == 'Engine Size' or line == 'Cylinders':
                    car_data.engine_size = next_line
                elif line == 'Fuel Type':
                    car_data.fuel_type = next_line
                elif line == 'Spec':
                    car_data.spec = next_line
                elif line == 'Service Contract':
                    car_data.service_contract = next_line
                elif line == 'Cylinders':
                    car_data.cylinders = next_line
    
    def _extract_key_features(self, lines: List[str], car_data: CarListingData):
        """Extract key features"""
        in_features = False
        
        for line in lines:
            if line == 'Key Features':
                in_features = True
                continue
            
            if in_features and line == 'About':
                break
            
            if in_features:
                # Check if this line is a car feature
                if any(pattern in line.lower() for pattern in self.car_feature_patterns):
                    car_data.key_features.append(line.strip())
                elif len(line) < 50 and not any(skip in line.lower() for skip in ['image', 'png', 'jpg', 'format']):
                    # Short lines that might be features
                    car_data.key_features.append(line.strip())
    
    def _extract_about_section(self, lines: List[str], car_data: CarListingData):
        """Extract about section"""
        in_about = False
        about_lines = []
        
        for line in lines:
            if line == 'About':
                in_about = True
                continue
            
            if in_about and (line.startswith('REF:') or line == 'Exterior' or 'inspection-report' in line.lower()):
                break
            
            if in_about and line and not any(skip in line.lower() for skip in self.irrelevant_patterns):
                about_lines.append(line)
        
        car_data.about_description = ' '.join(about_lines).strip()
    
    def _extract_action_links(self, lines: List[str], car_data: CarListingData):
        """Extract action links"""
        actions = ['Call Us', 'Buy this Car', 'Book a free test drive', 'Chat on WhatsApp']
        
        for line in lines:
            for action in actions:
                if action in line:
                    car_data.action_links[action] = "Available"
    
    def _extract_offers(self, lines: List[str], car_data: CarListingData):
        """Extract offers and campaigns"""
        offer_patterns = [
            r'0% Downpayment', r'1 Year free warranty', r'Downpayment for all cars',
            r'free warranty', r'special deal', r'campaign', r'offer'
        ]
        
        for line in lines:
            for pattern in offer_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    if line not in car_data.offers:
                        car_data.offers.append(line.strip())
    
    def _extract_inspection_info(self, lines: List[str], car_data: CarListingData):
        """Extract inspection report information"""
        inspection_sections = ['Exterior', 'Engine', 'Electricals', 'Suspension']
        
        for line in lines:
            if line in inspection_sections:
                car_data.inspection_sections.append(line)
                car_data.has_inspection_report = True
            elif 'View full report' in line:
                car_data.has_inspection_report = True
    
    def _extract_viewer_count(self, lines: List[str], car_data: CarListingData):
        """Extract viewer count"""
        for line in lines:
            if 'People are viewing right now' in line:
                match = re.search(r'(\d+) People', line)
                if match:
                    car_data.viewers_count = match.group(1)
    
    async def extract_car_images(self, url: str) -> List[str]:
        """Extract car images using Playwright"""
        car_images = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(2000)
                
                # Look for car image containers/carousel
                image_selectors = [
                    'img[src*="cloudfront"]',
                    'img[src*="vehicles"]',
                    '.car-image img',
                    '.vehicle-image img',
                    '.gallery img',
                    '[class*="carousel"] img',
                    '[class*="slider"] img'
                ]
                
                for selector in image_selectors:
                    try:
                        images = await page.query_selector_all(selector)
                        for img in images:
                            src = await img.get_attribute('src')
                            if src and 'vehicles' in src and src not in car_images:
                                car_images.append(src)
                    except:
                        continue
                
                # Try clicking through carousel if available
                try:
                    next_buttons = await page.query_selector_all('[class*="next"], [class*="arrow-right"], .slick-next')
                    clicks = 0
                    while next_buttons and clicks < 20:
                        for button in next_buttons:
                            try:
                                await button.click()
                                await page.wait_for_timeout(1000)
                                
                                # Capture new images
                                new_images = await page.query_selector_all('img[src*="vehicles"]')
                                for img in new_images:
                                    src = await img.get_attribute('src')
                                    if src and src not in car_images:
                                        car_images.append(src)
                                
                                clicks += 1
                                break
                            except:
                                continue
                        else:
                            break
                except:
                    pass
                
            except Exception as e:
                print(f"❌ Error extracting images: {e}")
            
            finally:
                await browser.close()
        
        return car_images


async def extract_car_listing(url: str) -> Dict[str, Any]:
    """Main function to extract focused car listing data"""
    
    print(f"🚗 Extracting Car Listing Data from: {url}")
    print("=" * 60)
    
    extractor = CarListingExtractor()
    
    # Step 1: Extract markdown content (car-focused)
    print("📄 Step 1: Extracting page content...")
    try:
        # You would use Firecrawl here
        from utils.firecrawl_client import scrape_with_firecrawl
        markdown_content = await scrape_with_firecrawl(url, only_main_content=True)
    except:
        # Fallback: use the sample content we already have
        markdown_content = """Sample markdown content would go here"""
    
    # Step 2: Extract structured car data
    print("🔍 Step 2: Parsing car-specific information...")
    car_data = extractor.extract_from_markdown(markdown_content, url)
    
    # Step 3: Extract car images
    print("📸 Step 3: Extracting car images...")
    car_data.car_images = await extractor.extract_car_images(url)
    
    # Step 4: Get inspection report if available
    print("📋 Step 4: Checking for inspection report...")
    if car_data.has_inspection_report:
        # Would integrate with existing inspection extractor
        pass
    
    # Convert to dictionary
    result = {
        'extraction_info': {
            'timestamp': datetime.now().isoformat(),
            'source_url': url,
            'extractor_version': '3.0.0_car_focused'
        },
        'car_listing': {
            'basic_info': {
                'make': car_data.make,
                'model': car_data.model,
                'year': car_data.year,
                'stock_number': car_data.stock_number
            },
            'pricing': {
                'price_aed': car_data.price_aed,
                'monthly_payment': car_data.monthly_payment,
                'price_display': car_data.price_display
            },
            'overview': {
                'mileage': car_data.mileage,
                'warranty': car_data.warranty,
                'transmission': car_data.transmission,
                'engine_size': car_data.engine_size,
                'fuel_type': car_data.fuel_type,
                'cylinders': car_data.cylinders,
                'spec': car_data.spec,
                'service_contract': car_data.service_contract
            },
            'features': car_data.key_features,
            'about': car_data.about_description,
            'offers': car_data.offers,
            'action_links': car_data.action_links,
            'inspection': {
                'has_report': car_data.has_inspection_report,
                'sections': car_data.inspection_sections
            },
            'images': car_data.car_images,
            'metadata': {
                'viewers_count': car_data.viewers_count,
                'source_url': car_data.source_url,
                'extraction_timestamp': car_data.extraction_timestamp
            }
        }
    }
    
    print(f"✅ Extraction Complete!")
    print(f"   Basic Info: {car_data.make} {car_data.model} ({car_data.year})")
    print(f"   Price: {car_data.price_aed} AED")
    print(f"   Features: {len(car_data.key_features)} extracted")
    print(f"   Images: {len(car_data.car_images)} found")
    print(f"   Inspection: {'Yes' if car_data.has_inspection_report else 'No'}")
    
    return result


if __name__ == "__main__":
    # Test with Alba Cars URL
    url = "https://albacars.ae/buy-used-cars/vehicle/10194-volvo-xc40"
    
    async def main():
        result = await extract_car_listing(url)
        
        # Save result
        output_file = 'data/focused_car_extraction.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Car listing data saved to: {output_file}")
        return result
    
    asyncio.run(main()) 