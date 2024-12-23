import os
import json
import requests
import re
import tempfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import argparse

# Define the list of keywords to ignore
# Define the list of keywords to ignore
nopelist = [
    "node_modules", "jquery", "bootstrap", "react", "vue", "angular", "favicon.ico", "logo", "style.css", 
    "font-awesome", "materialize", "semantic-ui", "tailwindcss", "bulma", "d3", "chart.js", "three.js", 
    "vuex", "express", "axios", "jquery.min.js", "moment.js", "underscore", "lodash", "jquery-ui", 
    "angular.min.js", "react-dom", "redux", "chartist.js", "anime.min.js", "highcharts", "leaflet", 
    "pdf.js", "fullcalendar", "webfontloader", "swiper", "slick.js", "datatables", "webfonts", "react-scripts", 
    "vue-router", "vite", "webpack", "electron", "socket.io", "codemirror", "angularjs", "firebase", "swagger", 
    "typescript", "p5.js", "ckeditor", "codemirror.js", "recharts", "bluebird", "lodash.min.js", "sweetalert2", 
    "polyfils", "runtime", "bootstrap", "google-analytics", 
    "application/json", "application/x-www-form-urlencoded", "json2.js", "querystring", "axios.min.js", 
    "ajax", "formdata", "jsonschema", "jsonlint", "json5", "csrf", "jQuery.ajax", "superagent", 
    "body-parser", "urlencoded", "csrf-token", "express-session", "content-type", "fetch", "protobuf", 
    "formidable", "postman", "swagger-ui", "rest-client", "swagger-axios", "graphql", "apollo-client", 
    "react-query", "jsonapi", "json-patch", "urlencoded-form", "url-search-params", "graphql-tag", 
    "vue-resource", "graphql-request", "restful-api", "jsonwebtoken", "fetch-jsonp", "reqwest", "lodash-es", 
    "jsonwebtoken", "graphene", "axios-jsonp", "postman-collection", 
    "application/xml", "text/xml", "text/html", "text/plain", "multipart/form-data", "image/jpeg", 
    "image/png", "image/gif", "audio/mpeg", "audio/ogg", "video/mp4", "video/webm", "text/css", 
    "application/pdf", "application/octet-stream", "image/svg+xml", "application/javascript", 
    "application/ld+json", "text/javascript", "application/x-www-form-urlencoded", ".dtd", "google.com", "application/javascript", "text/css", "w3.org", "www.thymeleaf.org", "application/javascrip", "toastr.min.js", "spin.min.js" "./" ,"DD/MM/YYYY"
]

# Regex pattern to match JavaScript file URLs and other patterns
regex_str = r"""
  (?:"|')                               # Start newline delimiter
  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
    |
    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be
    |
    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/.]{1,}                # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-/]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
  )
  (?:"|')                               # End newline delimiter
"""

# Function to check if any keyword in nopelist is present in the JS URL
def is_nopelist(js_url):
    return any(keyword in js_url.lower() for keyword in nopelist)

def fetch_js_links(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        js_links = set()
        
        # Extract script tags with src attribute
        for script in soup.find_all('script', src=True):
            js_url = script['src']
            # Convert relative URL to absolute URL using urljoin
            full_url = urljoin(url, js_url)

            # Ignore URLs that match any keyword in the nopelist
            if not is_nopelist(full_url):
                js_links.add(full_url)
        
        # Return only if there are JS links found
        if js_links:
            return url, list(js_links)
        else:
            return None  # No JS links found, return None

    except requests.RequestException:
        return None  # In case of error, return None

def fetch_js_and_apply_regex(js_url, headers):
    try:
        # Download the JS file to a temporary location
        response = requests.get(js_url, headers=headers)
        response.raise_for_status()

        # Use temporary file to store the JS content
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(response.text)
            temp_file_path = temp_file.name
        
        # Apply regex to the content of the JS file
        with open(temp_file_path, 'r', encoding='utf-8') as file:
            js_content = file.read()
            regex_matches = re.findall(regex_str, js_content, re.VERBOSE)

        # Clean up temp file after reading
        os.remove(temp_file_path)

        # Filter out empty matches
        filtered_matches = [match[0] for match in regex_matches if match[0].strip() and not any(keyword in match[0] for keyword in nopelist)]
        filtered_matches = list(set(filtered_matches))

        # Return filtered matches
        return filtered_matches

    except requests.RequestException as e:
        print(f"Error fetching JS URL {js_url}: {e}")
        return []

def process_urls(urls, headers, verbose=False):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_js_links, url, headers): url for url in urls}
        
        for future in futures:
            result = future.result()
            if result:
                url, js_links = result

                # For each JS link, fetch and apply regex
                for js_link in js_links:
                    regex_matches = fetch_js_and_apply_regex(js_link, headers)
                    if regex_matches:
                        results.append({
                            "input": url,
                            "jslink": js_link,
                            "endpoints": regex_matches
                        })
                
                if verbose:
                    print(f"Processed: {url} - Found {len(js_links)} JS links and {len(results)} links with matches.")
    
    return results

def load_urls(input_source):
    if input_source.startswith("http://") or input_source.startswith("https://"):
        return [input_source]
    else:
        with open(input_source, 'r') as file:
            return [line.strip() for line in file.readlines()]

def parse_headers(header_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    for header in header_list:
        try:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
        except ValueError:
            print(f"Invalid header format: {header}")
    return headers

def main():
    parser = argparse.ArgumentParser(description="Extract JS links from a URL or a list of URLs")
    parser.add_argument('-i', '--input', required=True, help="URL or file containing URLs")
    parser.add_argument('-o', '--output', help="Output JSON file to save results (optional, prints to CLI if not specified)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")
    parser.add_argument('-H', '--header', action='append', help="Add custom header (can be used multiple times)")
    args = parser.parse_args()

    # Load URLs from input
    urls = load_urls(args.input)
    
    # Parse custom headers, including defaults
    headers = parse_headers(args.header if args.header else [])

    # Process URLs and extract JS links
    results = process_urls(urls, headers, verbose=args.verbose)

    # If output file is specified, write results to it; otherwise, print to CLI
    if args.output:
        with open(args.output, 'w') as out_file:
            json.dump(results, out_file, indent=2)
        if args.verbose:
            print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
