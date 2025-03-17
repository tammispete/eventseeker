from robocorp.tasks import task

@task
def eventseekerMain():
    """main task, I put under here tasks tiketti():"""
    getgigs_from_tikettiFI()


def getgigs_from_tikettiFI():
    """go to tiketti.fi, filter dates, screenshot, send email"""

