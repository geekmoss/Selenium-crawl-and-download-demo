from selenium.webdriver import Firefox
from time import sleep
import click


# Wait time for scrolling - time for loading Async requests
SCROLL_WAIT_TIME = 3


# CSS Selector + Attr to get
CSS_SELECTORS = [
    ('img', 'src'),
    ('video[src]', 'src'),
    ('video > source[type="video/mp4"]', 'src'),
]


def run_browser_and_crawl_urls(urls: list, need_scrolling=False, already_downloaded: list = None) -> list:
    """
    Start browser & crawl urls. Parse Sources url and return it.

    :param urls: Urls for crawling
    :param need_scrolling: Scrollings is needed?
    :param already_downloaded: Downloaded url for breakepoints in scrolling
    :return:
    """
    # Function for get sources links from HTML
    def get_sources(brwr) -> list:
        """
        :param brwr: Selenium Driver instance
        :return:
        """
        _sources = []

        for selector, attr in CSS_SELECTORS:
            for e in browser.find_elements_by_css_selector(selector):
                _sources.append(e.get_attribute(attr))
                pass
            pass

        return _sources

    browser = Firefox()
    sources = []

    for url in urls:
        browser.get(url)
        page = browser.page_source
        # If scrollings is needed, then scroll to end.
        while True and need_scrolling:
            browser.execute_script(f'window.scrollTo(0, 9999999999999)')
            sleep(SCROLL_WAIT_TIME)  # Wait for Async loading

            if already_downloaded:  # Breakpoints url
                if len(set(already_downloaded) & set(get_sources(browser))) > 0:
                    break
                pass

            if page == browser.page_source:  # If same content then break this loop
                break

            page = browser.page_source
            pass

        sources += get_sources(browser)
        pass

    browser.close()
    return sources


@click.command()
@click.argument('url', nargs=-1)
@click.option('--urls', type=click.File('r'), help='Read urls from file')
@click.option('--scrolling', is_flag=True, help='Use scrolling in pages')
@click.option('--downloaded', type=click.File('r'), help='File with url per line, downloaded urls are used for breakepoint in scrolling.')
def cli(url, urls, scrolling, downloaded):
    """
    python demo.py https://url1.com https://url2.com ...
    """
    url = (list(url) + [item.strip() for item in urls.readlines() if len(item.strip()) > 0]) if urls else url
    downloaded = [item.strip() for item in downloaded.readlines() if len(item.strip()) > 0] if downloaded else None

    if len(url) == 0:
        click.echo("No url provided, exiting.")
        return

    sources = run_browser_and_crawl_urls(url, scrolling, downloaded)
    click.echo('\n'.join(set(sources)))  # Print links, set for uniq list
    pass


if __name__ == '__main__':
    cli()
    pass
