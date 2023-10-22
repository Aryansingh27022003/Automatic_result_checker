from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create a web driver for your preferred browser

# Navigate to your website

  # Adjust the range as needed
driver = webdriver.Chrome()  # You can choose other browsers as well
driver.get("https://tsbie.cgg.gov.in/ResultMemorandum.do")
    # Define the text you are looking for in the result
text_to_find = "PIYUSH"

    # Generate the XPath for the radio button


    # Loop through the range of hallticket numbers

    # Fill in the input field
for hallticket_no in range(2058112000, 2058112600):
    time.sleep(0.5)
    radio_button_xpath = f"//input[@value='3']"

    # Use the find_element() method on the WebDriver object to find the element
    radio_button = driver.find_element(By.XPATH, radio_button_xpath)

    # Click the radio button
    radio_button.click()

    # Select the desired option in the dropdown
    select = Select(driver.find_element(By.NAME, "property(pass_year)"))  # Use By.NAME, not By.XPATH
    select.select_by_value("2020")  # Select by value
    
    input_field = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.NAME, 'hallticket_no')))
    input_field.send_keys(str(hallticket_no))
    # input_field.clear()
    
    # Submit the form
    submit_button = driver.find_element(By.CLASS_NAME, "button")  # Use By.CLASS_NAME, not By.XPATH
    submit_button.click()

    # Wait for the page to load and check if the text is present
    while text_to_find in driver.page_source:
        time.sleep(0.5)
    
    # If the desired text is found, stop the script
    if text_to_find in driver.page_source:
        print(f"Found the text: {text_to_find}")
        print(hallticket_no)
driver.quit()