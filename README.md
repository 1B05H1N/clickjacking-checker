# Clickjacking Checker Script

## Overview
This Python script checks if a given website is vulnerable to clickjacking attacks. It attempts to frame the target website in an HTML file and uses a WebDriver to capture a screenshot. If no WebDriver is found, it falls back to manual inspection and offers guidance for alternative testing methods.

## Requirements
- Python 3.x
- Selenium WebDriver
- ChromeDriver or GeckoDriver (Firefox WebDriver)
- `requests` and `BeautifulSoup` Python libraries
- `PIL` (Python Imaging Library)

## Installation
1. Ensure Python 3 is installed on your system.
2. Install Selenium WebDriver:
   ```
   pip install selenium
   ```
3. Install additional required Python libraries:
   ```
   pip install requests beautifulsoup4 pillow
   ```
4. Download ChromeDriver or GeckoDriver from their respective websites and ensure they are accessible in your system PATH, or modify the script to point to their locations.

## Usage
Run the script from the command line by passing the URL of the website you want to check:

```
python clickjacking_test.py <URL>
```

## How It Works
1. The script first checks for the `X-Frame-Options` header in the HTTP response.
2. If the header is not properly configured to prevent framing, the script creates a local HTML file attempting to frame the target website.
3. If ChromeDriver or GeckoDriver is found, it will use Selenium to take a screenshot of the framed page.
4. If no WebDriver is found, it prompts the user to manually open the HTML file in a browser.
5. The script provides an option to delete the generated HTML file and suggests alternative methods for clickjacking testing.

## Notes
- Always ensure you have permission to test the target website for vulnerabilities to avoid legal issues.
- The script does not check for Content Security Policy (CSP) frame-ancestors directive, which could also prevent clickjacking.
- For more comprehensive testing and resolution of clickjacking vulnerabilities, refer to the OWASP Clickjacking guide and consider using tools like Burp Suite.
