# Shopify Website Detector

This script detects if a given website is built using **Shopify** by analyzing its source code, HTTP headers, and common Shopify-specific patterns.

## Features
✅ Extracts and normalizes the root domain from any provided URL  
✅ Checks for Shopify-specific meta tags, CDN links, and checkout redirects  
✅ Inspects HTTP headers for Shopify-related information  
✅ Analyzes `robots.txt` and `sitemap.xml` for Shopify-specific rules  
✅ Works with full URLs or root domains  

## Installation

Ensure you have **Python 3.7+** installed. Then, install dependencies:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script with a website URL:

```bash
python shopify_checker.py https://store.example.com/products/item
```

### Example Output:
```
Checked: store.example.com
Is Shopify: True, Reason: Found Shopify CDN links.
```

## How It Works
1. **Extracts the root domain** from the provided URL.
2. **Sends requests** to the homepage, `/cart`, `robots.txt`, and `sitemap.xml`.
3. **Checks for Shopify indicators**, including:
   - Shopify meta tags (`<meta name="generator" content="Shopify">`)
   - Shopify CDN assets (`cdn.shopify.com`)
   - Redirects to `checkout.shopify.com`
   - Shopify-related HTTP headers (`X-ShopId`, `X-Shopify-Stage`)
   - Common Shopify sitemap patterns (`/collections/`, `/products/`)

## Example Detection Scenarios

| Website URL | Detection Result |
|-------------|-----------------|
| `https://mycoolstore.com` | ✅ Shopify detected (CDN links found) |
| `https://randomsite.com` | ❌ Not a Shopify site |
| `https://example.com/products/item123` | ✅ Shopify detected (Shopify headers found) |

## Contributing
Feel free to submit issues or contribute improvements! 🚀

## License
This project is open-source under the MIT License.
