from robocorp.tasks import task
from robocorp import browser

@task
def eventseekerMain():
    """main task, I put under here tasks getgigs_from_tikettiFI()"""
    getgigs_from_tikettiFI()


def getgigs_from_tikettiFI():
    """go to tiketti.fi, filter dates, screenshot, send email"""
    """slowed browser down to see whats happening"""
    browser.configure(
        slowmo=500,
    )
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
    """click on calendar 1 day, then click on down arrow to open the calendar again"""
    page.click("//td[text()='1']")
    locator = page.locator(".fa.fa-caret-down").nth(0)
    locator.wait_for(state="visible")  # Wait for the element to be visible
    locator.click()
    """Does an IF-statement to find the last date of the month, then Click on the calendar last date"""
    # Try to click the last date in the month, starting from 31, 30, 29, 28
    try:
        page.click("//td[text()='31']")  # Try to click 31
    except:
        try:
            page.click("//td[text()='30']")  # If 31 doesn't exist, try 30
        except:
            try:
                page.click("//td[text()='29']")  # If 30 doesn't exist, try 29
            except:
                page.click("//td[text()='28']")  # If 29 doesn't exist, try 28
    """select city Helsinki"""
    page.click('#event-search-city-select i.fa.fa-caret-right') #open the city selector
    page.click('#city\\|Helsinki')
    """select category music"""
    page.click('#event-search-category-select i.fa.fa-caret-right')
    page.click("#tag\\|0\\|1")
    """"""



   


