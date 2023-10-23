from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from twilio.rest import Client

# Twilio credentials
twilio_account_sid = 'AC4e299d8241657eb2fa43d187724ba9dd'
twilio_auth_token = '6bb2fa6f60ee49255c545278de34508d'
twilio_phone_number = '+13617923663'
recipient_phone_number = '+918051431138'  # Replace with the recipient's phone number

# Create a web driver for your preferred browser
driver = webdriver.Chrome()
driver.get("https://tsbie.cgg.gov.in/ResultMemorandum.do")

# Define the text you are looking for in the result
text_to_find = "PIYUSH"

# Loop through the range of hall ticket numbers
for hallticket_no in range(2058112338, 2058112342):
    time.sleep(0.5)
    radio_button_xpath = f"//input[@value='3']"

    radio_button = driver.find_element(By.XPATH, radio_button_xpath)
    radio_button.click()

    select = Select(driver.find_element(By.NAME, "property(pass_year)"))
    select.select_by_value("2020")

    input_field = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.NAME, 'hallticket_no')))
    input_field.send_keys(str(hallticket_no))

    submit_button = driver.find_element(By.CLASS_NAME, "button")
    submit_button.click()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        continue  # If the page changes too quickly, just skip this iteration

    if text_to_find in driver.page_source:
        print(f"Found the text: {text_to_find}")
        print(hallticket_no)
        roll_number = str(hallticket_no)

        # Create a TwiML response with the dynamic roll number
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say voice="woman">Hi Piyush Kumar, this is Aryan Kumar's robot. Your roll number is {roll_number}.</Say>
            <Play>http://demo.twilio.com/docs/classic.mp3</Play>
        </Response>"""

        # Create a Twilio client
        twilio_client = Client(twilio_account_sid, twilio_auth_token)

        # Make a phone call with the dynamic TwiML
        call = twilio_client.calls.create(
            to=recipient_phone_number,
            from_=twilio_phone_number,
            twiml=twiml
        )

driver.quit()
