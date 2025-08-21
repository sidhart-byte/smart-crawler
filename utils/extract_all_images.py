#!/usr/bin/env python3
"""
Extract all CloudFront image URLs from Alba Cars HTML
"""

import re
import json

def extract_cloudfront_urls_with_params(html_content):
    """Extract CloudFront URLs preserving query parameters"""
    # Pattern to match CloudFront URLs with query parameters
    cloudfront_pattern = r'https://d3n77ly3akjihy\.cloudfront\.net/[^"\s]+\.(?:jpeg|jpg|png|webp)(?:\?[^"\s]*)?'
    
    # Find all matches
    matches = re.findall(cloudfront_pattern, html_content)
    
    # Keep the URLs as-is (with query parameters)
    clean_urls = []
    for url in matches:
        if url not in clean_urls:
            clean_urls.append(url)
    
    return clean_urls

# Real HTML content from the Volvo XC40 page
html_content = """
<!DOCTYPE html><html lang="en"><body class="__variable_e8ce0c __variable_3fb87d bg-secondary"><div class="bg-white py-5 "><div class="mx-auto w-[90vw] max-w-screen-2xl  "></div></div><main class="min-h-screen flex-grow"><div class="min-h-screen"><div class="mx-auto w-[90vw] max-w-screen-2xl  "></div><div class="controlled-grid overflow-x-hidden lg:overflow-x-visible"><div class="full-width-mobile"><div class="mb-20 grid grid-cols-1 gap-x-5 xl:grid-cols-9 xxl:grid-cols-7"><div class="col-span-1 space-y-5 lg:grid-rows-4 xl:col-span-6 xxl:col-span-5"><!--$--><div class="!min-h-[345px] rounded-3xl bg-white p-4 xxl:!min-h-[776px]"><!--$!--><template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING"></template><div class="relative lg:hidden"><div class="rounded-2xl"><div class="overflow-hidden rounded-2xl"><div class="relative aspect-[4/3] overflow-hidden rounded-2xl"><img alt="Loading..." fetchpriority="high" loading="eager" height="0" decoding="async" data-nimg="fill" class="h-full w-full object-cover object-center" src="https://d3n77ly3akjihy.cloudfront.net/vehicles/7f39f040-ffd5-4244-b7b5-a10e59b48b60/6e77c694-572d-4f44-a81a-d107c9d66832.jpeg?format=webp&width=3840&quality=50"></div></div></div></div>
"""

# Extract real CloudFront URLs
cloudfront_urls = extract_cloudfront_urls_with_params(html_content)

print("Found CloudFront URLs:")
for i, url in enumerate(cloudfront_urls, 1):
    print(f"{i}. {url}")

# Save to JSON
result = {
    "total_images": len(cloudfront_urls),
    "cloudfront_urls": cloudfront_urls,
    "extraction_notes": "URLs extracted with query parameters preserved"
}

with open('extracted_image_urls.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"\nExtracted {len(cloudfront_urls)} CloudFront URLs and saved to extracted_image_urls.json") 