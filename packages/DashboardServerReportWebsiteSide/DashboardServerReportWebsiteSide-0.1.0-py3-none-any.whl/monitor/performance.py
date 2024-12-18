import requests
import time
from bs4 import BeautifulSoup
import urllib.parse
import re


# Performance Metrics
def get_performance_metrics(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        load_time = time.time() - start_time
        html_size = len(response.content)
        contentEncoding = response.headers.get('Content-Encoding')
        TTFB = response.elapsed.total_seconds()
        return {
            "status_code": response.status_code,
            "response_time": load_time,
            "status": "Up" if response.status_code == 200 else "Down",
            "HTML_page_size": f"{html_size / 1024:.2f} KB",
            "Content-Encoding": contentEncoding,
            "Time To First Byte": TTFB,
        }
    except requests.exceptions.RequestException as e:
        return {"status": "Down", "error": str(e)}


# Security Headers
def get_security_headers(url):
    try:
        response = requests.get(url, timeout=10)
        return {
            "Strict Transport Security": response.headers.get('Strict-Transport-Security', 'Not Set'),
            "X Content Type Options": response.headers.get('X-Content-Type-Options'),
            "X Frame Options": response.headers.get('X-Frame-Options'),
            "Referrer Policy": response.headers.get('Referrer-Policy'),
            "Permissions Policy": response.headers.get('Permissions-Policy'),
            "Cross Origin Resource Policy": response.headers.get('Cross-Origin-Resource-Policy'),
            "Cache Control": response.headers.get('Cache-Control'),
            "Expect CT": response.headers.get('Expect-CT'),
            "Access Control Allow Origin": response.headers.get('Access-Control-Allow-Origin'),
            "X Xss Protection": response.headers.get('X-XSS-Protection'),
            "Content-Encoding": response.headers.get('Content-Encoding', 'Not Set'),
        }
    except requests.exceptions.RequestException as e:
        return {"status": "Down", "error": str(e)}


# Content Security Policy (CSP) components
def get_csp_components(url):
    try:
        response = requests.get(url, timeout=10)
        csp = response.headers.get('Content-Security-Policy')

        if not csp:
            return {"CSP": "Not Set"}

        csp_components = [
            "default-src", "script-src", "style-src", "img-src", "connect-src",
            "font-src", "object-src", "media-src", "frame-src", "child-src",
            "manifest-src", "worker-src", "form-action", "frame-ancestors",
            "block-all-mixed-content", "upgrade-insecure-requests", "require-trusted-types-for", "trusted-types"
        ]

        detected_components = {
            component: "Present" if component in csp else "Not Present"
            for component in csp_components
        }
        return {"CSP Components": detected_components}
    except requests.exceptions.RequestException as e:
        return {"status": "Down", "error": str(e)}


# Internal Linking Structure
def get_internal_links(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the base URL for relative links
        base_url = urllib.parse.urlparse(url).netloc

        internal_links = set()

        # Find all <a> tags and check if they link to the same domain
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            parsed_href = urllib.parse.urlparse(href)

            # Only consider internal links (same domain or relative links)
            if parsed_href.netloc == base_url or parsed_href.netloc == '':
                internal_links.add(urllib.parse.urljoin(url, href))

        return {"internal_links_count": len(internal_links), "internal_links": list(internal_links)}

    except requests.exceptions.RequestException as e:
        return {"status": "Down", "error": str(e)}


def get_cdn_usage(url):
    try:
        # Send a GET request to the URL to get the page content
        response = requests.get(url, timeout=10)

        # Check if the request was successful
        if response.status_code != 200:
            return {"status": "Down", "error": "Unable to access the page"}

        cdn_usage = []

        # Check for CDN-specific headers
        cdn_headers = [
            'X-Cache', 'X-CDN', 'X-Edge-Location', 'Via', 'X-Edge-Request-ID',
            'X-Served-By', 'X-Cache-Lookup', 'X-CDN-Region', 'X-Cloud-Trace-Context'
        ]
        for header in cdn_headers:
            if header in response.headers:
                cdn_usage.append(f"CDN Header Detected: {header} - {response.headers.get(header)}")

        # Define a list of common patterns that match CDN URLs
        cdn_patterns = [
            r'cdn[\w]*\.',  # Matches subdomains containing 'cdn'
            r'(\.cloudfront\.net|\.akamai\.net|\.amazonaws\.com|\.cdn\.jsdelivr\.net|\.cdn\.cloudflare\.com|\.fbcdn\.net|\.stackpath\.cdn\.com)',
            # Common CDN domains
            r'https?://(?:\w+\.)?(?:cdn|static)\.',  # Matches cdn or static subdomains
            r'(\.fastly\.net|\.stackpathcdn\.com|\.googleusercontent\.com|\.cloudflare\.com)',
            # Additional CDNs like Fastly, Google
            r'cdn[0-9]+\.akamai\.net',  # Matches dynamic CDN URLs with numbers (Akamai)
        ]

        # Look for potential CDN resources in the HTML content
        content = response.text
        urls = re.findall(r'(https?://[^\s]+)', content)  # Find all URLs in the content

        for url in urls:
            if any(re.search(pattern, url) for pattern in cdn_patterns):
                cdn_usage.append(f"Possible CDN URL Detected: {url}")

        # If any CDN usage is detected, return it, else indicate no CDN
        if cdn_usage:
            return {"cdn_usage": cdn_usage}
        else:
            return {"cdn_usage": "No CDN usage detected."}

    except requests.exceptions.RequestException as e:
        return {"status": "Down", "error": str(e)}
