import argparse
import time
from scraply.scraper import scrape_urls, clone_page

def main():
    parser = argparse.ArgumentParser(description="Scrape and collect all URLs from a website.")
    parser.add_argument('url', help="The base URL of the website to scrape (e.g., https://facebook.com).")
    parser.add_argument('--output', '-o', help="Output file to save the URLs.", type=str)
    parser.add_argument('--clone', '-c', help="Clone each URL and save the HTML page.", action='store_true')
    parser.add_argument('--clone-single', '-cs', help="Clone a single specific URL from the site.", type=str)

    args = parser.parse_args()

    start_time = time.time()

    urls = scrape_urls(args.url)

    if args.output:
        with open(args.output, 'w') as f:
            for url in urls:
                f.write(url + '\n')

    if args.clone:
        for url in urls:
            clone_start_time = time.time()
            clone_page(url)
            clone_end_time = time.time()

    if args.clone_single:
        clone_start_time = time.time()
        clone_page(args.clone_single)
        clone_end_time = time.time()

    end_time = time.time()
    print(f"\nTotal scraping time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
