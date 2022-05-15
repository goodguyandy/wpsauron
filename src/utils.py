import io
import zipfile

import requests
from bs4 import BeautifulSoup


# credits to tomnomnom for the idea.
def waybackurls(target, include_subs=False):
    wildcard = "*"
    if include_subs:
        url = f'http://web.archive.org/cdx/search/cdx?url={wildcard}.{target}/*&output=json&fl=original&collapse=urlkey'
    else:
        url = f'http://web.archive.org/cdx/search/cdx?url={target}/*&output=json&fl=original&collapse=urlkey'

    r = requests.get(url)
    results = r.json()
    results = [item[0] for item in results][1:]
    return results


def extract_plugin_name_from_url(target):
    separator = "/wp-content/plugins/"
    if separator in target:
        name = target.split(separator)[1].split("/")[0].strip().lower()
        return name


def build_plugin_url(plugin_name):
    url = f"https://wordpress.org/plugins/{plugin_name}/"
    return url


def check_plugin_exists(plugin_name):
    """
    check if plugin exists in wordpress plugin database
    """
    r = requests.get(plugin_name)
    if "/plugins/search/" in r.url:
        return False
    return True


def download_plugin_and_extract(zip_file_url, extraction_path):
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(extraction_path)

def get_plugin_stats(plugin_url):
    """
    bad scraping here :)
    """
    data = {}
    r = requests.get(plugin_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    try:
        els = soup.find('div', {"class": ["widget plugin-meta", "widget"]}).find("ul").findAll("li")
    except:
        return data

    data["plugin_url"] = plugin_url
    for el in els:
        el = el.text.replace("\n", "")
        el = el.replace("\t", "")
        el = el.strip()
        if "Version" in el and "WordPress" not in el and "PHP" not in el:
            data["plugin_version"] = el.split("Version:")[1].strip()
        elif "Last updated:" in el:
            data["last_updated"] = el.split("Last updated:")[1].strip()
        elif "Active installations:" in el:
            data["active_installations"] = el.split("Active installations:")[1].strip()
        elif "WordPress" in el:
            data["wordpress_version"] = el.split("WordPress Version:")[1].strip()
        elif "PHP" in el:
            data["php_version"] = el.split("PHP Version:")[1].strip()

    try:
        download_url = soup.find('a', {"class": ["plugin-download", "button", "download-button", "button-large"]})["href"]
        data["download_url"] = download_url

    except:
        return data

    return data


def get_plugins_set_from_domain(domain):
    urls = waybackurls(domain)
    plugins = set()
    for u in urls:
        name = extract_plugin_name_from_url(u)
        if name:
            plugins.add(name)
    return plugins


def scrape_domain_and_get_plugins_info(domain):
    plugins = get_plugins_set_from_domain(domain)
    data = {}
    if plugins:
        for plugin_name in plugins:
            data[plugin_name] = {}
            plugin_url = build_plugin_url(plugin_name)
            results = get_plugin_stats(plugin_url)
            if results:
                data[plugin_name] = results
    return data




