import time
import re
from automation_framework.utilities.api_helpers import ApiHelper

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


CITY_NAMES = [
    "London", "Paris", "Tokyo", "New York", "Berlin",
    "Cairo", "Moscow", "Sydney", "Rome", "Madrid"
]
DISCREPANCY_THRESHOLD = 2.0


def run_fast_comparison():
    print("Starting FAST temperature comparison...")
    results = []
    driver = None

    try:
        api = ApiHelper()

        print("Setting up WebDriver...")
        service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(5)
        print("WebDriver ready.")

        for city in CITY_NAMES:
            print(f"\n--- Processing: {city} ---")
            api_temp = None
            website_temp = None

            api_temp = api.get_weather_by_city_name(city)
            if api_temp is not None:
                print(f"API Temp: {api_temp:.1f}°C")
            else:
                print("API Temp: Failed")


            try:
                driver.get("https://www.timeanddate.com/weather/")
                search_box = driver.find_element(By.ID, "query")
                search_box.clear()
                search_box.send_keys(city)
                search_box.send_keys(Keys.ENTER)
                print(f"Searched for {city} on timeanddate.com")

                # !!! UPDATE THIS SELECTOR !!! Check using Browser Dev Tools (F12) !!!
                temp_element_selector = (By.CSS_SELECTOR, ".my-city__data-note .h2")

                time.sleep(3)

                temp_element = driver.find_element(*temp_element_selector)
                temp_text = temp_element.text
                print(f"Found text: {temp_text}")

                match = re.search(r"(-?\d+)", temp_text)
                if match:
                    website_temp = float(match.group(1))
                    print(f"Website Temp: {website_temp:.1f}°C")
                else:
                    print(f"Could not parse website temp from: '{temp_text}'")

            except NoSuchElementException:
                print(f"Could not find temp element for {city}. Check selector / website.")
            except Exception as e:
                print(f"Error scraping {city}: {e}")

            if api_temp is not None and website_temp is not None:
                diff = abs(api_temp - website_temp)
                results.append({
                    'city': city,
                    'api_temp': api_temp,
                    'website_temp': website_temp,
                    'discrepancy': diff
                })
            else:
                print("--> Skipping result storage due to missing data.")

            time.sleep(1)

    except Exception as e:
        print(f"\n--- An error stopped the process: {e} ---")
    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed.")

    print("\n--- Comparison Report ---")
    if not results:
        print("No comparison results were recorded.")
        return

    discrepancy_found = False
    print(f"Cities with temperature discrepancy > {DISCREPANCY_THRESHOLD}°C:")
    for res in results:
        if res['discrepancy'] > DISCREPANCY_THRESHOLD:
            print(f"- {res['city']}: API={res['api_temp']:.1f}°C, Website={res['website_temp']:.1f}°C, Diff={res['discrepancy']:.1f}°C")
            discrepancy_found = True

    if not discrepancy_found:
        print(f"No cities found with discrepancy > {DISCREPANCY_THRESHOLD}°C.")

    print("\nFull Results:")
    for res in results:
         print(f"- {res['city']}: API={res['api_temp']:.1f}°C, Website={res['website_temp']:.1f}°C, Diff={res['discrepancy']:.1f}°C")


if __name__ == "__main__":
    run_fast_comparison()