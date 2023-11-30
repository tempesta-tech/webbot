#!/usr/bin/env python3
import argparse
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

__author__ = "Tempesta Technologies, Inc."
__copyright__ = "Copyright (C) 2023 Tempesta Technologies, Inc."
__license__ = "GPL2"


arg_parser = argparse.ArgumentParser(description="Website crawler for performance and security tasks")
arg_parser.add_argument("--log", action="store", type=str, default='info', help="Logging verbosity (debug, info, warning, error, critical)")
arg_parser.add_argument("--chrome_bin", action="store", type=str, default=None, help="Custom path to Chrome browser binary")
arg_parser.add_argument("--domain", action="store", type=str, default="tempesta-tech.com", help="Domain to explore")
arg_parser.add_argument("--broken", action="store", type=int, default=0, help="Check broken URLs")
args = arg_parser.parse_args()

retrieved = {}

def to_retrieve(url):
    """ Rules which URLs we should retrieve.
    At the moment only not visited yet.
    """
    if url in retrieved:
        return False
    retrieved[url] = 1
    return True

def retrieve(drv, domain, url):
    logging.info(f'retrieve {url}')

    drv.get(url)

    try:
        # Get all links from the page.
        links = drv.find_elements(By.CSS_SELECTOR, "a")
    except selenium.common.exceptions.TimeoutException:
        logging.warning(f'could not load links for {url}')
        return

    scopeset=set()

    for l in links:
        u = l.get_attribute('href')
        if not u:
            continue
        elif '#' in u:
            u=u.split('#')[0]
        scopeset.add(u)


    for u in scopeset:
        # Get the status with requests library and then retrieve the URL again
        # recursively with Selenium driver. We need the double requests for now
        # becauseit's not easy to get response status from selenium.
        # Trust self-signed certificates.
        logging.info(f'get {u}')
        try:
            result = requests.get(u, verify=False)
            if result.status_code != 200:
                logging.warning(f'BROKEN LINK {u} on {url} (status {result.status_code})')
        except:
            logging.warning(f'BROKEN LINK {u} on {url} (can not connect)')

        if '://{domain}/' in u and to_retrieve(u):
            retrieve(drv, domain, u)

def run_crawler(domain):
    options = webdriver.ChromeOptions()
    if args.chrome_bin:
        options.binary_location = args.chrome_bin
    # Don't care about certificates validity and accept self-signed certificates.
    options.add_argument('ignore-certificate-errors')

    drv = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)

    retrieve(drv, domain, f'https://{domain}/')

if __name__ == '__main__':
    log_lvl = getattr(logging, args.log.upper(), None)
    if not isinstance(log_lvl, int):
        raise ValueError('Invalid log level: %s' % args.log)
    logging.basicConfig(level=log_lvl)

    # Ignore warnings about self-signed certificates.
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    run_crawler(args.domain)
