# webbot

Website crawler for performance and security tasks:
* reveal dead links on a target website
* warm web accelerator's cache
* emulate bots behaviour (e.g. scrappers) to test a bots mitigation software


## Installation

Prerequisites for Ubuntu 22:
```sh
sudo apt update
sudo apt install -y unzip xvfb libxi6 libgconf-2-4
sudo apt install default-jdk
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
sudo apt -y update
sudo apt -y install google-chrome-stable
```

[Download](https://chromedriver.storage.googleapis.com/index.html) the latest Chrome
driver and install it:
```sh
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver 
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
```

Install the [Selenium Python driver](https://pypi.org/project/selenium/) with:
```sh
pip install selenium
```

You might experience exception
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 114
Current browser version is 117.0.5938.132 with binary path /usr/bin/google-chrome
```
in this case you should install a Chrome or Chromium version of matching major
version number. [Here](https://chromium.cypress.io/) the list of old binary versions
of the browser.

You can run `wbot` with the custom browser like
```sh
./wbot.py --crome_bin /opt/google/chromium-114/chrome
```

## References

* [Selenium documentation](https://www.selenium.dev/documentation/), including Python API
