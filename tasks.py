from robocorp.tasks import task
from robocorp import browser
import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

@task
def eventseekerMain():
    """main task, I put under here tasks getgigs_from_tikettiFI()"""
    getgigs_from_tikettiFI()
    getgigs_from_lippuFI()
    getgigs_from_metelinet()
    send_email()


def getgigs_from_tikettiFI():
    """go to tiketti.fi, filter dates, screenshot, send email"""    
    """open tiketti.fi"""
    browser.goto("https://www.tiketti.fi/")
    """get browserfuctions for this page"""
    page = browser.page()

    """accept consent, waits for popup to appead and then clicks on the accept button"""
    page.wait_for_selector("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll", state="visible", timeout=10000)  # Waits up to 10s
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")

    """click on haku"""
    page.click("span:text('Haku')")

    """click on calendar next month"""
    page.click(".fa.fa-angle-right")
    """click on calendar 1 day"""   
    page.wait_for_timeout(5000) #wait for 5 seconds, issue with page loading
    page.click("//td[text()='1']")   

    """select city Helsinki"""
    page.wait_for_timeout(5000) #wait for 5 seconds, issue with page loading
    page.click('#event-search-city-select i.fa.fa-caret-right') #open the city selector
    page.click('#city\\|Helsinki')

    """select category music"""    
    page.click('#event-search-category-select i.fa.fa-caret-right')
    page.wait_for_selector("//li[text()='Musiikki']", state='visible') #testing another way to wait for page loading, waiting for element
    page.click("//li[text()='Musiikki']")

    """select genre punk hardcore"""
    page.wait_for_timeout(5000) #wait for 5 seconds, issue with page loading
    page.click('#event-search-genre-select')
    page.click("//li[text()='Punk/Hardcore']") #Filters for <li> elements whose text content is exactly "Punk/Hardcore".

    """After filters, take screenshot of the results"""      
    # Ensure the page is fully loaded
    page.wait_for_load_state('load') #waiting for page, issues with loading
    page.wait_for_timeout(5000) #wait for 5 seconds, issue with page loading
    page.screenshot(path="output/tiketti_results.png", full_page=True)

def getgigs_from_lippuFI():
    page = browser.goto("https://www.lippu.fi")

    """accept cookie consent, waits for popup to appead and then clicks on the accept button"""
    page.wait_for_selector("#cmpwelcomebtnno", state="visible", timeout=10000)  # Waits up to 10s
    page.click("#cmpwelcomebtnno")
    
    # Click "Kategoriat"
    page.click("#categories")
    
    # Select "Keikat ja konsertit"
    page.click("[data-qa='nav-cat-46']")    
    page.wait_for_timeout(1000)
    
    # Apply "Punk ja hardcore" filter    
    page.click("[data-qa='category-filter']")
    page.click("a[title='Punk ja hardcore']")
    page.wait_for_load_state("networkidle")
    
    # Select "Alkaen" -> "Next month"
    page.click("#datepicker-from")
    page.click("[data-qa='datepicker-quick-link-6']")
    page.wait_for_load_state("networkidle")
    
    screenshots = []
    page_num = 1
    
    while True:
        screenshot_path = f"output/page_{page_num}.png" 
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        page.screenshot(path=screenshot_path)
        screenshots.append(screenshot_path)
        
        # Check if there is a next page button inside an <a> tag (clickable)
        next_button = page.query_selector("a[data-qa='nextPage']")
        if next_button:
            next_button.click()
            page.wait_for_load_state("networkidle")
            page_num += 1
        else:
            break

def getgigs_from_metelinet():
    today = datetime.today()
    first_day_next_month = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
    first_day_after_next_month = (first_day_next_month.replace(day=1) + timedelta(days=32)).replace(day=1)
    last_day_next_month = first_day_after_next_month - timedelta(days=1)
    start_date = first_day_next_month.strftime("%Y-%#m-%#d")
    end_date = last_day_next_month.strftime("%Y-%#m-%#d") 

    url = f"https://www.meteli.net/tapahtumahaku?g=punk%2Fhardcore&l=70&a={start_date}-{end_date}"
    page = browser.goto(url)
    
    # Accept cookies if button exists
    consent_button = page.query_selector(".fc-button.fc-cta-consent.fc-primary-button")
    if consent_button:
        consent_button.click()
    
    page.wait_for_timeout(1000)
    
    screenshots = []
    page_num = 1
    
    while True:
        screenshot_path = f"output/meteli_{page_num}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        screenshots.append(screenshot_path)
        
        # Check if there is a next page button inside an <a> tag (clickable)
        next_button = page.query_selector("a:has-text('Seuraava')")
        if next_button:
            next_button.click()
            page.wait_for_timeout(1000)
            page_num += 1
        else:
            break
    

def send_email():
    #load environment variables from .env file
    load_dotenv()

    """get email credentials from env"""
    SENDER_EMAIL = os.getenv("EMAIL_USER") #email used
    SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
    RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

    """check if credentials are available"""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Error: Email credentials not found")
        exit(1)

    """create email message"""
    msg = EmailMessage()
    msg["Subject"] = "Punkkikeikat"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content("Here is the screenshots of gigs")

    """Attach screenshot to email"""
    # Get all PNG files from the "output" folder
    output_folder = "output"
    attachments = [f for f in os.listdir(output_folder) if f.endswith(".png")]

    # Attach all PNG files dynamically
    for file_name in attachments:
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "rb") as file:
            msg.add_attachment(file.read(), maintype="image", subtype="png", filename=file_name)

    """Send email"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)









    






   


