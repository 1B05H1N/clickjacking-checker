import requests
import sys
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from urllib.parse import urlparse

def find_driver(driver_name):
    search_paths = ["/usr/bin", "/usr/local/bin", "~/bin", "/usr/local/sbin", "/usr/sbin", "/sbin"]
    try:
        for path in search_paths:
            result = subprocess.run(['find', path, '-name', driver_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            paths = result.stdout.strip().split('\n')
            if paths and paths[0]:
                return paths[0]
        return None
    except Exception as e:
        print(f"Error finding {driver_name}: {e}")
        return None

def add_http_schema_if_missing(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "http://" + url
    return url

def is_clickjackable(url):
    try:
        response = requests.get(url)
        x_frame_options = response.headers.get('X-Frame-Options', '').lower()
        return not x_frame_options or 'sameorigin' not in x_frame_options and 'deny' not in x_frame_options
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return False

def create_framing_html_file(url, filename='frame_test.html'):
    html_content = f"""
    <html>
      <head><title>Clickjacking Test</title></head>
      <body>
        <iframe src="{url}" width="100%" height="100%"></iframe>
      </body>
    </html>
    """
    with open(filename, 'w') as file:
        file.write(html_content)
    return os.path.abspath(filename)

def take_screenshot(driver_path, html_file, screenshot_filename='screenshot.png', browser='chrome'):
    driver = None
    try:
        if browser == 'chrome':
            chrome_options = ChromeOptions()
            chrome_options.headless = True
            driver = webdriver.Chrome(driver_path, options=chrome_options)
        elif browser == 'firefox':
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            driver = webdriver.Firefox(executable_path=driver_path, options=firefox_options)
        driver.get(f"file://{html_file}")
        driver.save_screenshot(screenshot_filename)
        print(f"Screenshot saved as {screenshot_filename}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
    finally:
        if driver:
            driver.quit()

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"Deleted file: {filename}")
    except Exception as e:
        print(f"Error deleting file: {e}")

if len(sys.argv) != 2:
    print("Usage: python clickjacking_test.py <URL>")
    sys.exit(1)

url = add_http_schema_if_missing(sys.argv[1])
if is_clickjackable(url):
    print(f"The website {url} might be vulnerable to clickjacking.")
    html_file = create_framing_html_file(url)
    chrome_driver_path = find_driver('chromedriver')
    firefox_driver_path = find_driver('geckodriver')

    if chrome_driver_path:
        take_screenshot(chrome_driver_path, html_file, browser='chrome')
    elif firefox_driver_path:
        take_screenshot(firefox_driver_path, html_file, browser='firefox')
    else:
        print("No suitable WebDriver found (ChromeDriver or GeckoDriver).")
        print(f"Please open the file {html_file} in a web browser manually to check for clickjacking. If the page renders within that file, the website is vulnerable to clickjacking.")
        if input("Delete the generated HTML file? (yes/no): ").lower() == "yes":
            delete_file(html_file)
        print(f"Alternatively, you can use a tool like Burp Suite to check for clickjacking. See https://portswigger.net/web-security/clickjacking for more details.")
else:
    print(f"The website {url} is not vulnerable to clickjacking.")

print("For more information on resolving clickjacking issues, visit the OWASP Clickjacking defense cheatsheet at https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html.")