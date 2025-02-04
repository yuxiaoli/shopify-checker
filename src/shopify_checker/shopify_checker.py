import requests
from bs4 import BeautifulSoup
import re
import argparse
from urllib.parse import urlparse

def get_root_domain(url):
    """Extracts the root domain from a given URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path  # Handle cases where no scheme is provided
    return domain.split('/')[0]  # Remove anything after the root domain

def is_shopify(url):
    try:
        # Normalize URL
        domain = get_root_domain(url)
        url = f"https://{domain}"

        # Fetch HTML content
        response = requests.get(url, timeout=5)
        html = response.text

        # Check for Shopify-related patterns in HTML
        soup = BeautifulSoup(html, "html.parser")
        
        # Look for Shopify meta tags
        if soup.find("meta", {"name": "generator", "content": "Shopify"}):
            return True, "Found Shopify meta tag."

        # Look for Shopify CDN assets
        if "cdn.shopify.com" in html:
            return True, "Found Shopify CDN links."

        # Check common Shopify-specific URLs
        checkout_url = url + "/cart"
        cart_response = requests.get(checkout_url, timeout=5)
        if "checkout.shopify.com" in cart_response.url:
            return True, "Redirected to Shopify checkout."

        # Check HTTP Headers
        headers = response.headers
        if "X-ShopId" in headers or "X-Shopify-Stage" in headers:
            return True, "Found Shopify-related HTTP headers."

        # Check robots.txt for Shopify-specific disallow rules
        robots_url = url + "/robots.txt"
        robots_response = requests.get(robots_url, timeout=5)
        if "Disallow: /admin" in robots_response.text and "Disallow: /cart" in robots_response.text:
            return True, "Shopify-style robots.txt detected."

        # Check sitemap.xml
        sitemap_url = url + "/sitemap.xml"
        sitemap_response = requests.get(sitemap_url, timeout=5)
        if re.search(r'<loc>.*?/collections/</loc>', sitemap_response.text):
            return True, "Shopify-style sitemap detected."

        return False, "No Shopify indicators found."
    
    except requests.RequestException as e:
        return False, f"Error fetching website: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect if a website is built on Shopify.")
    parser.add_argument("url", type=str, help="Website URL to check (e.g., https://example.com/product)")
    args = parser.parse_args()

    root_domain = get_root_domain(args.url)
    result, reason = is_shopify(root_domain)
    print(f"Checked: {root_domain}")
    print(f"Is Shopify: {result}, Reason: {reason}")
