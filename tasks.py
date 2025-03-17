from robocorp.tasks import task
from robocorp import browser

@task
def eventseekerMain():
    """main task, I put under here tasks getgigs_from_tikettiFI()"""
    getgigs_from_tikettiFI()


def getgigs_from_tikettiFI():
    """go to tiketti.fi, filter dates, screenshot, send email"""    
    """open tiketti.fi"""
    browser.goto("https://www.tiketti.fi/")
    """get browserfuctions for this page"""
    page = browser.page()
    """get rid of cookie consent, waits for popup to appead and then clicks on the decline button"""
    page.wait_for_selector("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll", state="visible", timeout=10000)  # Waits up to 10s
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    """click on haku"""
    page.click("span:text('Haku')")
    """click on calendar next month"""
    page.click(".fa.fa-angle-right")
    """click on calendar 1 day"""   
    page.wait_for_timeout(5000) 
    page.click("//td[text()='1']")    
    """select city Helsinki"""
    page.wait_for_timeout(5000)
    page.click('#event-search-city-select i.fa.fa-caret-right') #open the city selector
    page.click('#city\\|Helsinki')
    """select category music"""    
    page.click('#event-search-category-select i.fa.fa-caret-right')
    page.wait_for_selector("//li[text()='Musiikki']", state='visible')
    page.click("//li[text()='Musiikki']")
    """select genre punk hardcore"""
    page.wait_for_timeout(5000)
    page.click('#event-search-genre-select')
    page.click("//li[text()='Punk/Hardcore']") #Filters for <li> elements whose text content is exactly "Punk/Hardcore".

    """After filters, take screenshot of the results"""      
    # Ensure the page is fully loaded
    page.wait_for_load_state('load')
    page.wait_for_timeout(5000)
    page.screenshot(path="output/tiketti_results.png", full_page=True)









    






   


