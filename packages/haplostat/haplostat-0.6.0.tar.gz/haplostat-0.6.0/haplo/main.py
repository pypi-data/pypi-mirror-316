from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request, jsonify
import platform

app = Flask(__name__)

def map_populations(user_selected_populations):
    """
    Maps user-selected populations to the corresponding population codes.
    """
    population_mapping = {
        "African American": "AFA",
        "Asian or Pacific Islander": "API",
        "Caucasian": "CAU",
        "Hispanic": "HIS",
        "Native American": "NAM",
    }
    return population_mapping.get(user_selected_populations, "CAU")

def parse_top_hla_group(soup):
    """
    Parses the results page for HLA group information.
    """
    table = soup.find("table", {"class": "compact"})
    if not table:
        return {"error": "No table found in the results page"}

    tbody = table.find("tbody")
    if not tbody:
        return {"error": "No table body found in the results page"}

    results = [[], []]
    rows = tbody.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            hla_right = cols[0].text.strip()
            hla_left = cols[1].text.strip()
            results[0].append(hla_right)
            results[1].append(hla_left)

    return results

def run_convert_hla(population_1, hla_a="", hla_a1="", hla_b="", hla_b1="", hla_c="", hla_c1="", hla_drb1="", hla_drb2="", hla_dqb1="", hla_dqb2=""):
    """
    Main function to perform HLA conversion by interacting with the haplostats website.
    """
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")

        # Initialize WebDriver with webdriver-manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("WebDriver initialized successfully.")

        # Navigate to the website
        driver.get("https://www.haplostats.org/haplostats")
        print("Navigated to haplostats.org.")

        # Clear previous selections
        clear_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "popButton2"))
        )
        clear_button.click()

        # Select population
        pop_val = map_populations(population_1)
        if pop_val:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//fieldset[@class='criteria']//input[@type='checkbox' and @value='{pop_val}']"))
            )
            checkbox.click()

        # Select haplotype loci
        try:
            dropdown = driver.find_element(By.NAME, "haplotypeLoci")
            select = Select(dropdown)
            select.select_by_visible_text("A~C~B~DRBX~DRB1~DQB1")
            print("Selected option 'A~C~B~DRBX~DRB1~DQB1' from dropdown.")
        except Exception as e:
            raise RuntimeError(f"Error selecting option from dropdown: {e}")

        # Fill the form fields
        payload = {
            "a1": hla_a,
            "b1": hla_b,
            "c1": hla_c,
            "drb11": hla_drb1,
            "dqb11": hla_dqb1,
            "a2": hla_a1,
            "b2": hla_b1,
            "c2": hla_c1,
            "drb12": hla_drb2,
            "dqb12": hla_dqb2
        }
        for field_name, value in payload.items():
            if value:
                field = driver.find_element(By.NAME, field_name)
                field.clear()
                field.send_keys(value)

        # Submit the form
        submit_button = driver.find_element(By.NAME, "_eventId_success")
        submit_button.click()
        print("Form submitted.")

        # Switch to the results tab
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        print("Switched to results tab.")

        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "_title_A-C-B-DRBX-DRB1-DQB1_mug_id"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print("Results page loaded successfully.")
        return parse_top_hla_group(soup)

    except Exception as e:
        print(f"Error during run_convert_hla: {e}")
        raise

    finally:
        if driver:
            driver.quit()

@app.route('/convert_hla', methods=['POST'])
def convert_hla():
    """
    Flask API endpoint to handle HLA conversion requests.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        population_1 = data.get('population_1', "")
        hla_a = data.get('hla_a', "")
        hla_a1 = data.get('hla_a1', "")
        hla_b = data.get('hla_b', "")
        hla_b1 = data.get('hla_b1', "")
        hla_c = data.get('hla_c', "")
        hla_c1 = data.get('hla_c1', "")
        hla_drb1 = data.get('hla_drb1', "")
        hla_drb2 = data.get('hla_drb2', "")
        hla_dqb1 = data.get('hla_dqb1', "")
        hla_dqb2 = data.get('hla_dqb2', "")

        results = run_convert_hla(
            population_1, hla_a, hla_a1, hla_b, hla_b1, hla_c, hla_c1,
            hla_drb1, hla_drb2, hla_dqb1, hla_dqb2
        )
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
