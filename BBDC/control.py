from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# TELEGRAM NOTIFICATIONS
TOKEN = ""
CHAT_ID = ""
CHAT_LOG = ""


def send_message(msg):
    '''
    Send message via telegram bot
    :param msg:
    :return:
    '''

    # For payload params refer: https://core.telegram.org/bots/api#sendmessage
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TOKEN), data=payload).content
def send_message_logs(msg):
    '''
    Send message via telegram bot
    :param msg:
    :return:
    '''

    # For payload params refer: https://core.telegram.org/bots/api#sendmessage
    payload = {
        "chat_id": CHAT_LOG,
        "text": msg,
        "parse_mode": "HTML"
    }
    return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TOKEN), data=payload).content
def space():
    print("\n")

with open("variable2.2.txt") as f:
    line = f.readlines()
    ID = line[1].replace("ID:", "")
    ID = ID.replace("\n", "")
    password = line[2].replace("Password:", "")
    password = password.replace("\n", "")
    date = line[4].replace("Date:", "")
    date = date.replace("\n", "").split(",")
    month = line[6].replace("Month:", "")
    month = month.replace("\n", "")
    month = month.split(",")
    session = line[8].replace("Session:", "")
    session = session.replace("\n", "")
    if session != "ALL":
        session = session.split(",")
    day = line[10].replace("Day:", "")
    day = day.replace("\n", "")
    if day != "ALL":
        day = day.split(",")
    type = line[12].replace("Type:", "")
    type = type.replace("\n", "")
    if type == "TPDS,1" or type == "TPDS,2" or type == "TPDS,3":
        type = type.split(",")
        simulator_module = type[1]
        type = type[0]
    else:
        simulator_module = "NIL"
    delay = line[14].replace("Delay:", "")
    delay = delay.replace("\n", "")
    try:
        delay = int(delay)
    except:
        delay = float(delay)
    path = line[16].replace("PATH:", "")
    path = path.replace("\n", "")
    if path == "NIL":
        PATH = "chromedriver.exe"
    USER = line[17].replace("USER:", "")
    USER = USER.replace("\n", "")
    max_restart = line[18].replace("Max Restart:", "")
    max_restart = max_restart.replace("\n", "")
    max_restart = int((max_restart))
    mode = line[19].replace("Mode:", "")
    mode = mode.replace("\n", "")
    drivingclass = line[20].replace("Class:","")
    drivingclass = drivingclass.replace("\n","")
    member = line[21].replace("Member:","")
    member = member.replace("\n","")

restart = True
print("Please confirm the following details:"
      "\n"
      f"Date: {date} | Month: {month} | Session: {session} | Day: {day}"
      "\n"
      f"Type: {type} | Module: {simulator_module} | Class: {drivingclass}"
      "\n"
      f"Mode: {mode} | Delay: {delay} | Restart: {restart} | Max Restart: {max_restart} | User: {USER}")

input("Press enter to confirm, else change the values in notepad and restart bot!")
print("Launching now...")
send_message_logs(f"")

rvalue = 0
pvalue = 0
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://info.bbdc.sg/members-login/")
while restart == True or rvalue != 1:
    rvalue = 1
    monitor = 1
    pvalue += 1
    retry = True

    try:
        driver.find_element_by_id("txtNRIC").send_keys(ID)
        driver.find_element_by_id("txtPassword").send_keys(password)
        driver.find_element_by_id("loginbtn").click()
        driver.find_element_by_id("proceed-button").click()

        try:
            if drivingclass == "2B":
                driver.find_element_by_css_selector("input[type='radio'][value='2B|933189|0|G0000']").click()
            elif drivingclass == "3":
                pass #Need to find class 3 value
            elif drivingclass == "3A":
                pass #Need to find class 3A value
            elif drivingclass == "P3A":
                driver.find_element_by_css_selector("input[type='radio'][value='P3A|924006|0|G0000']").click()

            driver.find_element_by_css_selector("input[type='submit'][value='Submit']").click()
        except NoSuchElementException:
            pass

        if type == "TPDS":
            exec(open('TPDS 2.2b.py').read())

        elif type == "BTT" or type == "FTT":
            exec(open('FTT.py').read())
            restart = False

        elif type == "RTT":
            exec(open('RTT.py').read())
            restart = False

        elif type == "LESSON":
            if drivingclass == "2B":
                exec(open('LESSON.py').read())
                restart = False
            elif drivingclass == "3A" or drivingclass == "3":
                exec(open('LESSON 3A.py').read())
                restart = False
            else:
                print("Select a valid driving class!")
        elif type == "FTE" or "BTE":
            exec(open('FTE.py').read())
            restart = False

        if restart == False:
            driver.save_screenshot(f"{USER}{type}.png")

            if type == "TPDS":
                confirm = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[8]/td[2]").get_attribute("innerHTML")
                confirm = confirm.replace("				", "")
                confirm = confirm.replace("\n", "")
                confirm = confirm.split("&")
                csession = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[9]/td[2]").get_attribute("innerHTML")
                csession = csession.replace("				", "")
                csession = csession.replace("\n","")
                csession = csession.replace("			","")
                print(f"{USER} successfully booked {type} {simulator_module} on {confirm[0]}, Session {csession}!")
                send_message_logs(f"{USER} successfully booked {type} {simulator_module} on {confirm[0]}, Session {csession}!")
                check = input("Would you like to post success?").upper()
                if check == "YES" or "Y":
                    send_message(f"{USER} successfully booked {type} {simulator_module} on {confirm[0]}, Session {csession}!")
            else:
                print(f"{USER} successfully booked {type} on {relative_y.get(element_x)} {month}, Session {relative_y.get(element_y)}!")
                check = input("Would you like to post success?").upper()
                if check == "YES" or "Y":
                    send_message(f"{USER} successfully booked {type} on {relative_y.get(element_x)} {month}, Session {relative_y.get(element_y)}!")

    except Exception:
        if restart == False:
            pass
        elif pvalue != max_restart:
            time.sleep(delay)
            driver.get("https://info.bbdc.sg/members-login/")
        elif pvalue == max_restart:
            restart = False
