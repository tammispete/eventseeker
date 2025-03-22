from robocorp.tasks import task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

@task
def getgigs_from_metelinet():
    today = datetime.today()
    first_day_next_month = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
    first_day_after_next_month = (first_day_next_month.replace(day=1) + timedelta(days=32)).replace(day=1)
    last_day_next_month = first_day_after_next_month - timedelta(days=1)
    start_date = first_day_next_month.strftime("%Y-%-m-%-d")
    end_date = last_day_next_month.strftime("%Y-%-m-%-d")

    url = f"https://www.meteli.net/tapahtumahaku?g=punk%2Fhardcore&l=70&a={start_date}-{end_date}"
    driver = webdriver.Chrome()

    driver.get(url)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button")))
    consent_button = driver.find_element(By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button")
    consent_button.click()

    time.sleep(1)

    event_lists = driver.find_elements(By.XPATH, "//div[@class='event-list']")
    previous_event_count = len(event_lists)

    screenshots = []
    for index, event in enumerate(event_lists):
        try:
            screenshot_path = f'event_list_{index + 1}_screenshot.png'
            event.screenshot(screenshot_path)
            screenshots.append(screenshot_path)
        except Exception as e:
            print(f"Error taking screenshot of event {index + 1}: {e}")

    event_lists = driver.find_elements(By.XPATH, "//div[@class='event-list']")
    for index, event in enumerate(event_lists[previous_event_count:]):
        try:
            screenshot_path = f'event_list_{index + previous_event_count + 1}_screenshot.png'
            event.screenshot(screenshot_path)
            screenshots.append(screenshot_path)
        except Exception as e:
            print(f"Error taking screenshot of event {index + previous_event_count + 1}: {e}")

    print("Sending email with screenshots...")
    send_email(screenshots)

def send_email(screenshots):
    load_dotenv()

    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))

    subject = 'Tulevat "Punk/Hardcore"-keikat!'
    body = "Meteli.net tulevat keikat!"
    receiver_email = "onni.pajarinen@student.laurea.fi"

    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    for screenshot in screenshots:
        if os.path.exists(screenshot):
            with open(screenshot, "rb") as f:
                msg.add_attachment(f.read(), maintype="image", subtype="png", filename=screenshot)
        else:
            print(f"Warning: Screenshot not found - {screenshot}")

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
