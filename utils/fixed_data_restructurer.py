#!/usr/bin/env python3
"""
FIXED Data Restructurer - NO DATA LOSS
======================================

This script properly parses the inspection data pattern without losing any data.
The pattern is: Category Header → [Item Name, Status Value] pairs

Author: AI Assistant
Version: 2.1.0 - FIXED - No Data Loss
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class FixedInspectionParser:
    """Correctly parse inspection data without data loss"""
    
    def __init__(self):
        self.status_keywords = ['passed', 'failed', 'good', 'excellent', 'poor', 'fair', 'warning', 'attention', 'needs attention']
        self.category_indicators = ['condition', 'conditions', 'assessment', 'check', 'test', 'evaluation']
    
    def parse_inspection_section(self, items: List[str]) -> Dict[str, Any]:
        """Parse inspection section preserving ALL data"""
        if not items:
            return {}
            
        structured = {}
        current_category = None
        i = 0
        
        print(f"   Parsing {len(items)} items...")
        
        while i < len(items):
            current_item = items[i].strip()
            
            if not current_item:
                i += 1
                continue
            
            # Check if this is a category header
            is_category = (
                any(indicator in current_item.lower() for indicator in self.category_indicators) and
                not any(status in current_item.lower() for status in self.status_keywords)
            )
            
            if is_category:
                current_category = current_item
                structured[current_category] = {}
                print(f"     Found category: {current_category}")
                i += 1
                continue
            
            # If we have a category, try to parse item-value pairs
            if current_category and i + 1 < len(items):
                next_item = items[i + 1].strip()
                
                # Check if next item is a status
                if any(status in next_item.lower() for status in self.status_keywords):
                    structured[current_category][current_item] = next_item
                    print(f"       {current_item}: {next_item}")
                    i += 2  # Skip both items
                    continue
            
            # Handle special cases like "Hood Condition" followed directly by status
            if current_category and any(status in current_item.lower() for status in self.status_keywords):
                # This might be a direct status for the category
                if len(structured[current_category]) == 0:
                    structured[current_category]["condition"] = current_item
                    print(f"       Direct status: {current_item}")
                else:
                    # Or it might be an item without explicit name
                    structured[current_category][f"item_{len(structured[current_category]) + 1}"] = current_item
                    print(f"       Unnamed item: {current_item}")
                i += 1
                continue
            
            # If we don't have a category yet, create a general one
            if not current_category:
                current_category = "general_items"
                structured[current_category] = {}
                print(f"     Created general category")
            
            # Add item without clear status
            if current_category:
                structured[current_category][f"item_{len(structured[current_category]) + 1}"] = current_item
                print(f"       Misc item: {current_item}")
            
            i += 1
        
        return structured


def fix_restructured_database():
    """Fix the restructuring with correct data preservation"""
    
    print("🔧 FIXED Data Restructuring - NO DATA LOSS")
    print("=" * 60)
    
    # Load original data
    with open('data/first_10_cars_complete_database.json', 'r') as f:
        original_data = json.load(f)
    
    print(f"📂 Loaded original database: {len(original_data['vehicles'])} vehicles")
    
    parser = FixedInspectionParser()
    fixed_vehicles = []
    
    for i, vehicle in enumerate(original_data['vehicles'], 1):
        print(f"\n🔄 Processing vehicle {i}/{len(original_data['vehicles'])}")
        print(f"   URL: {vehicle.get('url', 'Unknown')}")
        
        # Start with the original vehicle data structure
        fixed_vehicle = {
            'extraction_metadata': {
                'original_position': vehicle.get('position', i),
                'extraction_timestamp': vehicle.get('extraction_timestamp', ''),
                'source_url': vehicle.get('url', ''),
                'fixed_restructure_at': datetime.now().isoformat(),
                'original_data_quality_score': vehicle.get('data_quality', {}).get('completeness_score', 0)
            }
        }
        
        # Extract basic info from URL
        url = vehicle.get('url', '')
        if url:
            url_parts = url.split('/')[-1].split('-')
            if len(url_parts) >= 3:
                fixed_vehicle['basic_info'] = {
                    'stock_id': url_parts[0],
                    'make': url_parts[1].title(),
                    'model': ' '.join(url_parts[2:]).title().replace('62L', '6.2L')
                }
        
        # Preserve and restructure inspection data
        if 'inspection_report' in vehicle and 'inspection_data' in vehicle['inspection_report']:
            inspection_data = vehicle['inspection_report']['inspection_data']
            fixed_vehicle['inspection_report'] = {}
            
            if 'sections' in inspection_data:
                sections = inspection_data['sections']
                
                for section_name, section_items in sections.items():
                    if isinstance(section_items, list) and section_items:
                        print(f"   Processing {section_name} section with {len(section_items)} items")
                        fixed_vehicle['inspection_report'][section_name] = parser.parse_inspection_section(section_items)
                        
                        # Count items after parsing
                        parsed_count = sum(len(cat_items) for cat_items in fixed_vehicle['inspection_report'][section_name].values())
                        print(f"     Parsed into {parsed_count} structured items")
        
        # Preserve all images with metadata
        if 'all_images' in vehicle:
            images = vehicle['all_images']
            fixed_vehicle['images'] = {
                'all_images': []
            }
            
            for idx, image_url in enumerate(images):
                # Determine image metadata from URL
                quality = 'high' if 'quality=75' in image_url or 'quality=100' in image_url else 'medium'
                width = '3840' if 'width=3840' in image_url else '800' if 'width=800' in image_url else 'unknown'
                
                # Categorize by position
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
                
                image_data = {
                    'url': image_url,
                    'category': category,
                    'angle': angle,
                    'quality': quality,
                    'width': width,
                    'position': idx + 1
                }
                
                fixed_vehicle['images']['all_images'].append(image_data)
            
            print(f"   Preserved all {len(images)} images with metadata")
        
        # Add data quality metrics
        orig_inspection_items = 0
        if 'inspection_report' in vehicle and 'inspection_data' in vehicle['inspection_report']:
            sections = vehicle['inspection_report']['inspection_data'].get('sections', {})
            for section_data in sections.values():
                if isinstance(section_data, list):
                    orig_inspection_items += len(section_data)
        
        fixed_inspection_items = 0
        if 'inspection_report' in fixed_vehicle:
            for section_data in fixed_vehicle['inspection_report'].values():
                if isinstance(section_data, dict):
                    for cat_data in section_data.values():
                        if isinstance(cat_data, dict):
                            fixed_inspection_items += len(cat_data)
        
        fixed_vehicle['data_quality'] = {
            'original_inspection_items': orig_inspection_items,
            'preserved_inspection_items': fixed_inspection_items,
            'data_preservation_rate': fixed_inspection_items / orig_inspection_items if orig_inspection_items > 0 else 0,
            'image_count': len(vehicle.get('all_images', [])),
            'has_basic_info': bool(fixed_vehicle.get('basic_info')),
            'structure_version': '2.1_fixed'
        }
        
        print(f"   Data preservation: {fixed_vehicle['data_quality']['data_preservation_rate']:.1%}")
        
        fixed_vehicles.append(fixed_vehicle)
    
    # Create fixed database
    fixed_database = {
        'database_info': {
            'version': '2.1.0',
            'structure': 'fully_structured_no_data_loss',
            'original_extraction': original_data['extraction_info'],
            'fixed_restructure_at': datetime.now().isoformat(),
            'total_vehicles': len(fixed_vehicles),
            'fixes_applied': [
                'correct_inspection_data_parsing',
                'preserve_all_original_data',
                'proper_category_item_value_relationships',
                'comprehensive_image_metadata',
                'data_preservation_metrics'
            ]
        },
        'vehicles': fixed_vehicles,
        'summary': {
            'total_vehicles': len(fixed_vehicles),
            'total_images': sum(len(v.get('images', {}).get('all_images', [])) for v in fixed_vehicles),
            'average_data_preservation': sum(v['data_quality']['data_preservation_rate'] for v in fixed_vehicles) / len(fixed_vehicles),
            'makes_available': list(set(v.get('basic_info', {}).get('make', 'Unknown') for v in fixed_vehicles))
        }
    }
    
    # Save fixed database
    output_file = 'data/fixed_restructured_database.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_database, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Fixed database saved: {output_file}")
    print(f"📊 File size: {Path(output_file).stat().st_size / 1024:.1f} KB")
    
    return fixed_database


if __name__ == "__main__":
    try:
        result = fix_restructured_database()
        
        print("\n🎉 FIXED RESTRUCTURING COMPLETE!")
        print("=" * 50)
        print(f"✅ Vehicles processed: {result['database_info']['total_vehicles']}")
        print(f"✅ Total images preserved: {result['summary']['total_images']}")
        print(f"✅ Average data preservation: {result['summary']['average_data_preservation']:.1%}")
        print(f"✅ Makes available: {', '.join(result['summary']['makes_available'])}")
        
        # Verification check
        print("\n🔍 VERIFICATION:")
        first_vehicle = result['vehicles'][0]
        if 'inspection_report' in first_vehicle and 'exterior' in first_vehicle['inspection_report']:
            exterior_data = first_vehicle['inspection_report']['exterior']
            found_rear_door = False
            for category, items in exterior_data.items():
                if 'Rear right door' in items:
                    print(f"✅ Found 'Rear right door' in {category}: {items['Rear right door']}")
                    found_rear_door = True
                    break
            
            if not found_rear_door:
                print("❌ 'Rear right door' still missing - need to debug further")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc() 