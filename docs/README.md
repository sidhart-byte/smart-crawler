# Alba Cars UAE Scraper Suite

A comprehensive, production-ready web scraping toolkit for extracting vehicle data from Alba Cars UAE website. This refactored codebase provides specialized tools for different extraction methods and data types.

## 🚀 Features

- **Multi-Method Extraction**: Firecrawl, Playwright, and specialized extractors
- **Advanced Image Extraction**: Full carousel navigation with real CloudFront URLs  
- **Inspection Reports**: Automated extraction of detailed vehicle inspection data
- **Clean Architecture**: Organized, maintainable codebase structure
- **Production Ready**: Proper error handling, logging, and data validation

## 📁 Project Structure

```
discover-generator/
├── src/                          # Core scraper modules
│   ├── alba_cars_scraper.py      # Main Firecrawl-based scraper
│   ├── fixed_playwright_scraper.py           # Image extraction with carousel
│   ├── playwright_comprehensive_scraper.py   # Comprehensive Playwright scraper
│   └── inspection_report_extractor.py        # Inspection report specialist
├── utils/                        # Utility scripts
│   ├── extract_all_images.py     # CloudFront URL extraction
│   ├── create_final_real_database.py  # Database assembly
│   └── final_complete_database.py     # Final data processing
├── docs/                         # Documentation
├── data/                         # Generated databases (auto-created)
├── logs/                         # Log files (auto-created)
└── requirements.txt             # Dependencies
```

## 🛠️ Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd discover-generator
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## 🔧 Usage

### Quick Start

```bash
# Easy way - use the automated runner
./run.sh

# Or run manually
python3 main.py

# Direct access to specific scrapers
python3 src/alba_cars_scraper.py
python3 src/fixed_playwright_scraper.py
python3 src/playwright_comprehensive_scraper.py
python3 src/inspection_report_extractor.py
```

### Python API

```python
from src.alba_cars_scraper import AlbaCarsScraper

# Initialize scraper
scraper = AlbaCarsScraper(headless=True, log_level="INFO")

# Scrape multiple vehicles
vehicle_urls = [
    "https://albacars.ae/buy-used-cars/vehicle/10194-volvo-xc40",
    "https://albacars.ae/buy-used-cars/vehicle/10193-gmc-sierra-denali"
]
vehicles = scraper.scrape_multiple_vehicles(vehicle_urls)

# Save results
scraper.save_database()
```

## 📊 Extraction Methods

### 1. **Firecrawl Scraper** (`alba_cars_scraper.py`)
- **Best for**: Structured data extraction
- **Features**: Vehicle specs, pricing, basic features
- **Speed**: Fast, reliable
- **Output**: Clean JSON with metadata

### 2. **Playwright Image Scraper** (`fixed_playwright_scraper.py`)
- **Best for**: Image extraction with carousel navigation
- **Features**: All vehicle images, CloudFront URLs
- **Speed**: Moderate (browser automation)
- **Output**: Real, working image URLs

### 3. **Comprehensive Playwright** (`playwright_comprehensive_scraper.py`)
- **Best for**: Complete data + images in one pass
- **Features**: Everything combined
- **Speed**: Slower but comprehensive
- **Output**: Full vehicle profile

### 4. **Inspection Extractor** (`inspection_report_extractor.py`)
- **Best for**: Detailed inspection reports
- **Features**: Modal clicking, detailed assessments
- **Speed**: Targeted, efficient
- **Output**: Complete inspection data

## 📈 Performance & Scaling

- **Rate Limiting**: Built-in delays to respect website
- **Error Handling**: Graceful failure recovery
- **Logging**: Comprehensive operation tracking
- **Memory Efficient**: Streaming JSON output
- **Scalable**: Can handle hundreds of vehicles

## 🔍 Data Output

All scrapers generate structured JSON with:

```json
{
  "extraction_info": {
    "timestamp": "2025-01-15T12:00:00",
    "total_vehicles": 10,
    "scraper_version": "2.0.0"
  },
  "vehicles": [
    {
      "id": "10194",
      "make": "Volvo",
      "model": "XC40",
      "specifications": {...},
      "images": ["https://cloudfront.net/..."],
      "features": [...],
      "inspection_report": {...}
    }
  ]
}
```

## 🧰 Utilities

- **`extract_all_images.py`**: CloudFront URL cleaner
- **`create_final_real_database.py`**: Multi-source data combiner  
- **`final_complete_database.py`**: Final processing pipeline

## 📝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational and research purposes. Please respect Alba Cars UAE's terms of service and robots.txt.

## 🚨 Disclaimer

Use responsibly and in accordance with website terms of service. This tool is intended for legitimate data analysis and research purposes only.
