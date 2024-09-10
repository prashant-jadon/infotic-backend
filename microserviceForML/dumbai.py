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

def fetch_links_from_nodejs(keyword):
    nodejs_url = 'http://localhost:3000/data'  # Replace with your Node.js URL
    try:
        response = requests.post(nodejs_url, json={'keyword': keyword})
        response.raise_for_status()
        data = response.json()
        print(data)
        return [link['href'] for link in data.get('links', [])]  # Extracting URLs
    except requests.RequestException as e:
        print(f"Error fetching links from Node.js server: {e}")
        return []

def main(keyword):
    links = fetch_links_from_nodejs(keyword)
    useful_texts = []

    for link in links:
        html_source = fetch_html(link)
        if html_source:
            useful_text = extract_useful_text(html_source)
            useful_texts.append(useful_text)

    # Output or save the useful texts
    for index, text in enumerate(useful_texts):
        print(f"Text from link {index + 1}:\n{text}\n")

# Example usage
keyword = 'stacks in data structure'  # Replace with your keyword
main(keyword)
