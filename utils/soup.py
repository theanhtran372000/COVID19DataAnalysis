from bs4 import BeautifulSoup
import urllib.request


def get_soup(url):
    page = urllib.request.urlopen(url)
    return BeautifulSoup(page, 'html.parser')


def extract_scripts(soup):
    return soup.findAll('script')


def filter_scipts(scripts):
    filteredScripts = []

    for script in scripts:
        if 'Highcharts.chart' in script.text:
            filteredScripts.append(script)

    return filteredScripts
