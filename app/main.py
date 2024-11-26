from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dbos import DBOS

# Welcome to DBOS!
# This is a template application built with DBOS and FastAPI.

app = FastAPI()
DBOS(fastapi=app)

# This is a simple DBOS workflow with two steps.
# It is served via FastAPI from the /hello endpoint.
# You can use workflows to build crashproof applications.
# Learn more here: https://docs.dbos.dev/python/programming-guide


@DBOS.step()
def hello_step() -> str:
    return "Hello"


@DBOS.step()
def world_step() -> str:
    return "world"


# @app.get("/hello")
# @DBOS.workflow()
# def hello_world() -> str:
#     hello = hello_step()
#     world = world_step()
#     return f"{hello}, {world}!"


# This code uses FastAPI to serve an HTML + CSS readme from the root path.


def send_email():
    message = Mail(
        from_email='audtracy@outlook.com',
        to_emails='audtracy@gmail.com',
        subject='ALERT: PCT PERMIT AVAILABLE IN MAY',
        html_content='<strong>GO GET THE PERMIT JOSH. GO. PERMIT. NOW.</strong>')
    try:
        sg = SendGridAPIClient(api_key="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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def scrape():

    element_list = []

    page_url = "https://portal.permit.pcta.org/availability/mexican-border.php"

    driver = webdriver.Chrome()
    driver.get(page_url)

    next_button = driver.find_elements(By.CLASS_NAME, "fc-icon.fc-icon-chevron-right")
    title = driver.find_elements(By.CLASS_NAME, "fc-left")

    ActionChains(driver).click(next_button[0]).perform() # into April
    ActionChains(driver).click(next_button[0]).perform() # into May

    while(True):

        permit_days = driver.find_elements(By.CLASS_NAME, "fc-event-container")

        for i in range(len(permit_days)):
            print("----------------")
            print(permit_days[i].text, permit_days[i].text.strip() != '35')
            print("----------------")

            if permit_days[i].text.strip() != '35':
                # send_email()
                print("HELLOOOO")
                # break

        time.sleep(1) # sleep 1 second

    driver.close() # close webdriver

@app.get("/")
def readme(background_tasks: BackgroundTasks) -> HTMLResponse:
    background_tasks.add_task(scrape)
    readme = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Scrape</title>
            <link rel="icon" href="https://dbos-blog-posts.s3.us-west-1.amazonaws.com/live-demo/favicon.ico" type="image/x-icon">
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="font-sans text-gray-800 p-6 max-w-2xl mx-auto">
            <h1 class="text-xl font-semibold mb-4">Welcome to DBOS!</h1>
            <p class="mb-4">
                Yo
            </p>
            <p class="mb-4">
                To get started building, edit <code class="bg-gray-100 px-1 rounded">app/main.py</code>, then visit the <a href="https://console.dbos.dev/applications" class="text-blue-600 hover:underline">cloud console</a> to redeploy your app.
            </p>
            <p class="mb-4">
                To learn more about DBOS, check out the <a href="https://docs.dbos.dev" class="text-blue-600 hover:underline">docs</a>.
            </p>
        </body>
        </html>
        """
    return HTMLResponse(readme)
