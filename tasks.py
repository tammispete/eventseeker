from robocorp.tasks import task
from robocorp import browser

@task
def eventseekerMain():
    """main task, I put under here tasks tiketti():"""
    getgigs_from_tikettiFI()


def getgigs_from_tikettiFI():
    """go to tiketti.fi, filter dates, screenshot, send email"""
    """slowed browser down to see whats happening"""
    browser.configure(
        slowmo=1500,
    )
    """open tiketti.fi"""
    browser.goto("https://www.tiketti.fi/")
    """get browserfuctions for this page"""
    page = browser.page()
    """get rid of cookie consent, waits for popup to appead and then clicks on the decline button"""
    page.wait_for_selector("#CybotCookiebotDialogBodyButtonDecline", state="visible", timeout=10000)  # Waits up to 10s
    page.click("#CybotCookiebotDialogBodyButtonDecline")
    """click on haku"""
    page.click("span:text('Haku')")
    """click on calendar next month"""
    page.click(".fa.fa-angle-right")
    """click on calendar 1 day"""
   


