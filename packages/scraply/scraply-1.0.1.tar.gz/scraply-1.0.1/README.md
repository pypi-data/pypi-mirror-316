# Scraply

**Scraply** is a Python package designed to scrape websites, extract all internal URLs, and clone pages by saving them as HTML files. You can use it through the command line interface or import it as a library in your Python scripts.

## Features
- Scrape all internal URLs from a given website.
- Clone and save HTML content from all URLs or a specific URL.
- Simple command-line interface (CLI) for easy usage.

## Installation

### Using `pip`

To install **Scraply**, use the following command:

```bash
pip install scraply
```

## Usage

### Command-Line Usage

You can use **Scraply** via the command line for scraping URLs and cloning pages.

#### Scrape All URLs from a Website

To scrape all internal URLs from a given website (e.g., `https://example.com`), run the following command:

```bash
scraply https://example.com
```

This command will print all the internal URLs found on the website.

#### Save Scraped URLs to a File

To scrape all URLs and save them to a file (`urls.txt`), use the `--output` flag:

```bash
scraply https://example.com --output urls.txt
```

#### Clone All Pages from a Website

To clone (download) the HTML content of all internal pages on the website, use the `--clone` flag:

```bash
scraply https://example.com --clone
```

This will save each HTML page from the website locally.

#### Clone a Specific Page

To clone a specific page (e.g., `https://example.com/privacy`), use the `--clone-single` flag:

```bash
scraply https://facebook.com --clone-single https://example.com/privacy
```

### Python Library Usage

You can also use **Scraply** as a Python library in your script. Here’s how:

#### Scraping All URLs from a Website

```python
import time
from scraply import scrape_urls

# URL to scrape
url = 'https://example.com'

# Scraping all URLs from the website
start_time = time.time()
urls = scrape_urls(url)

# Print the scraped URLs
for url in urls:
    print(url)

end_time = time.time()
print(f"Total scraping time: {end_time - start_time:.2f} seconds")
```

#### Cloning All Pages

```python
from scraply import clone_page

# Clone each URL from a list
urls = ['https://example.com/privacy', 'https://example.com/about']

for url in urls:
    clone_page(url)
```

#### Cloning a Single Specific Page

```python
from scraply import clone_page

# Clone a single page
clone_page('https://example.com/privacy')
```

### Example Directory Structure

Here's an example of how your project structure should look after installation:


### License

This project is licensed under the MIT License.

## Contributing

Feel free to fork, contribute, or open issues on the [GitHub repository](https://github.com/ByteBreach/scraply).

## Author

Developed by **Fidal**.  
Email: mrfidal@proton.me 
GitHub: [mr-fidal](https://github.com/mr-fidal)
