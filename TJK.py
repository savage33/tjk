# main.py
import time
import pandas as pd
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from config import CHROME_DRIVER_PATH, OUTPUT_PATH, BASE_URL, DAYS_BACK

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Set up the Chrome WebDriver with options."""
    chrome_options = Options()
    prefs = {
        "excludeSwitches": ["enable-automation"],
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'useAutomationExtension': False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
    driver.maximize_window()
    return driver

def navigate_to_site(driver):
    """Navigate to the TJK website."""
    try:
        driver.get(BASE_URL)
        logging.info("Navigated to TJK website.")
        time.sleep(5)
    except Exception as e:
        logging.error(f"Failed to load the website: {e}")
        driver.quit()
        raise

def extract_data(driver):
    """Extract horse racing data from the website."""
    try:
        race_data = []
        yarisbilgisi = driver.find_element(By.CLASS_NAME, "gunluk-tabs")
        yarislistesi = yarisbilgisi.find_elements(By.TAG_NAME, "li")
        logging.info(f"Found {len(yarislistesi)} races.")

        action = ActionChains(driver)
        previous_day_btn = driver.find_element(By.XPATH, "//a[@title='Önceki Gün']")

        for _ in range(DAYS_BACK):
            previous_day_btn.click()
            time.sleep(5)
            tables = driver.find_elements(By.XPATH, "//table[@summary='Kosular']")

            for table in tables:
                df_list = pd.read_html(table.get_attribute('outerHTML'))
                for df in df_list:
                    race_data.append(df)
                    
        return pd.concat(race_data, ignore_index=True)

    except Exception as e:
        logging.error(f"Error during data extraction: {e}")
        driver.quit()
        raise

def save_to_excel(df):
    """Save the extracted data to an Excel file."""
    try:
        output_file = os.path.join(OUTPUT_PATH, "TJK.xlsx")
        df.to_excel(output_file, index=False)
        logging.info(f"Data saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to save data to Excel: {e}")
        raise

def main():
    """Main function to run the scraper."""
    driver = setup_driver()
    try:
        navigate_to_site(driver)
        race_data = extract_data(driver)
        save_to_excel(race_data)
    finally:
        driver.quit()
        logging.info("Driver closed.")

if __name__ == "__main__":
    main()
