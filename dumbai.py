import requests
from bs4 import BeautifulSoup

def extract_useful_text(html_source):
    # Parse the HTML content
    soup = BeautifulSoup(html_source, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Extract text
    text = soup.get_text(separator=' ')
    
    # Break the text into lines and remove leading/trailing whitespace on each
    lines = [line.strip() for line in text.splitlines()]
    
    # Break multi-headlines into a line each
    chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
    
    # Remove any empty strings from the list
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def main(url):
    html_source = fetch_html(url)
    if html_source:
        useful_text = extract_useful_text(html_source)
        print(useful_text)

# Example usage
url = 'https://www.prepbytes.com/blog/stacks/applications-of-stack-in-data-structure/'
main(url)