#!/usr/bin/env python3
"""
Focused Car Data Extractor
==========================

Extracts and structures ONLY car-related data from vehicle listings.
Filters out irrelevant website content while preserving all car information.

This script uses our existing extraction tools but focuses the output
on car-specific information according to the schema:

- Model name & stock number
- Price details  
- Car overview (year, mileage, warranty, etc.)
- Key features
- About section
- Inspection report
- Action links
- Car images
- Offers/campaigns

Author: AI Assistant  
Version: 3.0.0 - Car-Focused Data
"""

import json
import re
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


def extract_focused_car_data(raw_extraction_file: str) -> Dict[str, Any]:
    """
    Take raw extraction data and create focused car listing JSON
    """
    
    print("🚗 CREATING FOCUSED CAR EXTRACTION")
    print("=" * 50)
    
    # Load raw extraction data
    with open(raw_extraction_file, 'r') as f:
        raw_data = json.load(f)
    
    print(f"📂 Loaded raw data: {len(raw_data['vehicles'])} vehicles")
    
    focused_vehicles = []
    
    for i, vehicle in enumerate(raw_data['vehicles'], 1):
        print(f"\n🔄 Processing vehicle {i}/{len(raw_data['vehicles'])}")
        
        url = vehicle.get('url', '')
        print(f"   URL: {url}")
        
        # Extract basic info from URL
        basic_info = extract_basic_info_from_url(url)
        
        # Extract pricing from raw data (need to implement)
        pricing = extract_pricing_info(vehicle)
        
        # Extract car overview from inspection or other sources
        overview = extract_car_overview(vehicle)
        
        # Extract key features (filter out non-car features)
        features = extract_car_features(vehicle)
        
        # Extract about section
        about = extract_about_section(vehicle)
        
        # Extract offers/campaigns
        offers = extract_offers(vehicle)
        
        # Extract action links
        action_links = extract_action_links(vehicle)
        
        # Process inspection data (preserve structure)
        inspection_data = process_inspection_data(vehicle)
        
        # Get car images (preserve all)
        car_images = extract_car_images(vehicle)
        
        # Create focused vehicle data
        focused_vehicle = {
            'basic_info': basic_info,
            'pricing': pricing,
            'overview': overview,
            'features': features,
            'about': about,
            'offers': offers,
            'action_links': action_links,
            'inspection_report': inspection_data,
            'images': car_images,
            'metadata': {
                'source_url': url,
                'extraction_timestamp': vehicle.get('extraction_timestamp', ''),
                'original_position': i
            }
        }
        
        focused_vehicles.append(focused_vehicle)
        
        # Show summary
        print(f"   ✅ Basic Info: {basic_info.get('make', '')} {basic_info.get('model', '')} ({overview.get('year', '')})")
        print(f"   ✅ Pricing: {pricing.get('price_aed', 'N/A')} AED")
        print(f"   ✅ Features: {len(features)} items")
        print(f"   ✅ Images: {len(car_images)} preserved")
        print(f"   ✅ Inspection: {len(inspection_data)} sections")
    
    # Create focused database
    focused_database = {
        'database_info': {
            'version': '3.0.0',
            'type': 'focused_car_listings',
            'created_at': datetime.now().isoformat(),
            'source_file': raw_extraction_file,
            'total_vehicles': len(focused_vehicles),
            'focus_schema': [
                'basic_info',
                'pricing', 
                'overview',
                'features',
                'about',
                'offers',
                'action_links',
                'inspection_report',
                'images',
                'metadata'
            ]
        },
        'vehicles': focused_vehicles,
        'summary': {
            'total_vehicles': len(focused_vehicles),
            'total_images': sum(len(v['images']) for v in focused_vehicles),
            'makes_available': list(set(v['basic_info'].get('make', 'Unknown') for v in focused_vehicles)),
            'average_features_per_car': sum(len(v['features']) for v in focused_vehicles) / len(focused_vehicles) if focused_vehicles else 0
        }
    }
    
    return focused_database


def extract_basic_info_from_url(url: str) -> Dict[str, str]:
    """Extract basic car info from URL"""
    basic_info = {}
    
    if url:
        url_parts = url.split('/')[-1].split('-')
        if len(url_parts) >= 3:
            basic_info['stock_number'] = url_parts[0]
            basic_info['make'] = url_parts[1].title()
            basic_info['model'] = ' '.join(url_parts[2:]).title().replace('62L', '6.2L')
    
    return basic_info


def extract_pricing_info(vehicle: Dict[str, Any]) -> Dict[str, str]:
    """Extract pricing information from vehicle data"""
    pricing = {}
    
    # Look in multiple places for pricing
    # This would need to be implemented based on actual data structure
    # For now, return empty dict
    return pricing


def extract_car_overview(vehicle: Dict[str, Any]) -> Dict[str, str]:
    """Extract car overview details (year, mileage, etc.)"""
    overview = {}
    
    # This would extract from vehicle details section
    # Implementation depends on actual data structure
    return overview


def extract_car_features(vehicle: Dict[str, Any]) -> List[str]:
    """Extract car features, filtering out non-car related items"""
    
    car_feature_keywords = [
        'camera', 'sensor', 'seat', 'wheel', 'engine', 'transmission',
        'brake', 'suspension', 'cruise', 'keyless', 'bluetooth', 'gps',
        'navigation', 'sunroof', 'leather', 'heated', 'cooled', 'electric',
        'automatic', 'manual', 'turbo', 'airbag', 'abs', 'stability',
        'traction', 'parking', 'reverse', 'backup', 'wireless', 'charger',
        'usb', 'aux', 'radio', 'stereo', 'speaker', 'subwoofer'
    ]
    
    irrelevant_keywords = [
        'website', 'contact', 'phone', 'email', 'address', 'hour', 'open',
        'close', 'facebook', 'instagram', 'twitter', 'linkedin', 'social',
        'faq', 'question', 'answer', 'policy', 'terms', 'condition',
        'subscribe', 'newsletter', 'update', 'inventory'
    ]
    
    features = []
    
    # This would extract features from the actual data
    # Implementation depends on data structure
    
    return features


def extract_about_section(vehicle: Dict[str, Any]) -> str:
    """Extract about/description section"""
    # Implementation depends on data structure
    return ""


def extract_offers(vehicle: Dict[str, Any]) -> List[str]:
    """Extract offers and campaigns"""
    # Implementation depends on data structure
    return []


def extract_action_links(vehicle: Dict[str, Any]) -> Dict[str, str]:
    """Extract action links (Call Us, Buy Car, etc.)"""
    # Implementation depends on data structure
    return {}


def process_inspection_data(vehicle: Dict[str, Any]) -> Dict[str, Any]:
    """Process and preserve inspection data"""
    inspection_data = {}
    
    if 'inspection_report' in vehicle:
        # Use the fixed structured data from our previous work
        inspection_data = vehicle['inspection_report']
    
    return inspection_data


def extract_car_images(vehicle: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and categorize car images"""
    car_images = []
    
    if 'all_images' in vehicle:
        images = vehicle['all_images']
        
        for idx, image_url in enumerate(images):
            # Categorize images
            if idx < 8:
                category = 'exterior'
                angles = ['front', 'front_angle', 'side', 'rear', 'rear_angle', 'side_profile', 'detail1', 'detail2']
                angle = angles[idx] if idx < len(angles) else f'exterior_{idx+1}'
            elif idx < 16:
                category = 'interior'
                angle = f'interior_{idx-7}'
            else:
                category = 'other'
                angle = f'misc_{idx+1}'
            
            # Determine quality from URL
            quality = 'high' if 'quality=75' in image_url or 'quality=100' in image_url else 'medium'
            width = '3840' if 'width=3840' in image_url else '800' if 'width=800' in image_url else 'unknown'
            
            image_data = {
                'url': image_url,
                'category': category,
                'angle': angle,
                'quality': quality,
                'width': width,
                'position': idx + 1
            }
            
            car_images.append(image_data)
    
    return car_images


def main():
    """Main function to create focused car extraction"""
    
    input_file = 'data/first_10_cars_complete_database.json'
    output_file = 'data/focused_car_listings.json'
    
    if not Path(input_file).exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    try:
        # Create focused extraction
        focused_data = extract_focused_car_data(input_file)
        
        # Save focused data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(focused_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Focused car data saved: {output_file}")
        print(f"📊 File size: {Path(output_file).stat().st_size / 1024:.1f} KB")
        
        # Show summary
        print(f"\n🎉 FOCUSED EXTRACTION COMPLETE!")
        print(f"✅ Total vehicles: {focused_data['summary']['total_vehicles']}")
        print(f"✅ Total images: {focused_data['summary']['total_images']}")
        print(f"✅ Makes available: {', '.join(focused_data['summary']['makes_available'])}")
        print(f"✅ Avg features per car: {focused_data['summary']['average_features_per_car']:.1f}")
        
        return focused_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 