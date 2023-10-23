from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyttsx3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import ImageGrab

# Create a web driver for your preferred browser
driver = webdriver.Chrome()
driver.get("https://tsbie.cgg.gov.in/ResultMemorandum.do")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define the text you are looking for in the result
text_to_find = "PIYUSH"

# Generate the XPath for the radio button

# Initialize SMTP server details
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Your Gmail credentials and the App Password
from_email = 'aryansingh27022003@gmail.com'  # Your Gmail address
to_email = 'aryan21_ug@cse.nits.ac.in'  # Recipient's email address
app_password = 'odys hlmn jrah adiy'  # Replace with your generated App Password

# Email details
subject = 'Screenshot of Page'
message = 'Screenshot of the page where text was found'

# Loop through the range of hallticket numbers
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
        engine.say("piyush kumar")
        engine.runAndWait()

        screenshot = ImageGrab.grab()
        screenshot.save('screenshot.png')

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        text = MIMEText(message)
        msg.attach(text)

        image = open('screenshot.png', 'rb').read()
        image = MIMEImage(image, name='screenshot.png')
        msg.attach(image)

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, app_password)  # Use your Gmail address and App Password
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {str(e)}")

driver.quit()
