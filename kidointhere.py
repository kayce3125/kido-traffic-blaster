import random
import time
from selenium import webdriver

# Global Variables
proxylist = []
useragents = []
browsers = ['firefox', 'chrome', 'opera', 'chromium']

# Read proxies from proxies.txt
def read_proxies():
    global proxylist
    with open("proxies.txt", "r") as file:
        proxylist = file.readlines()

# Read user-agents from useragent.txt
def read_useragents():
    global useragents
    with open("useragent.txt", "r") as file:
        useragents = file.readlines()

# Get a random proxy
def get_random_proxy():
    return random.choice(proxylist).strip()

# Get a random user-agent
def get_random_useragent():
    return random.choice(useragents).strip()

# Get a random browser
def get_random_browser():
    return random.choice(browsers)

# Configure webdriver with proxy, user-agent, and browser
def configure_webdriver(proxy, user_agent, browser):
    options = None
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument(f'--proxy-server={proxy}')
        return webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    elif browser == 'firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy.split(":")[0])
        profile.set_preference("network.proxy.http_port", int(proxy.split(":")[1]))
        return webdriver.Firefox(executable_path="geckodriver.exe", firefox_profile=profile)
    elif browser == 'opera':
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument(f'--proxy-server={proxy}')
        return webdriver.Chrome(executable_path="operadriver.exe", options=options)
    elif browser == 'chromium':
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument(f'--proxy-server={proxy}')
        return webdriver.Chrome(executable_path="chromiumdriver.exe", options=options)
    else:
        raise ValueError("Invalid browser choice")

# Visit the provided URL, click on 1 or 2 random links, and scroll up and down
def visit_website(url, driver):
    try:
        driver.get(url)
        time.sleep(random.randint(60, 80))

        # Click on 1 or 2 random links
        links = driver.find_elements_by_tag_name('a')
        random_links = random.sample(links, min(2, len(links)))
        for link in random_links:
            link.click()
            time.sleep(random.randint(1, 3))

        # Scroll up and down
        for _ in range(random.randint(2, 5)):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(1, 3))
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.randint(1, 3))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    read_proxies()
    read_useragents()
    
    while True:
        try:
            url = input("Enter the URL of the website: ")
            proxy = get_random_proxy()
            user_agent = get_random_useragent()
            browser = get_random_browser()

            print(f"Using proxy: {proxy}")
            print(f"Using user-agent: {user_agent}")
            print(f"Using browser: {browser}")

            driver = configure_webdriver(proxy, user_agent, browser)
            visit_website(url, driver)

            print("Task completed. Waiting for next iteration...")
            time.sleep(random.randint(60, 80))

        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            break
