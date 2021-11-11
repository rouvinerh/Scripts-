import time

driver.switch_to.frame(frame)
driver.find_element_by_xpath(xpath).click()

driver.switch_to.frame(frame1)
driver.find_element_by_css_selector("input[type='radio'][value='" + simulator_module + "']").click()
driver.find_element_by_css_selector("input[type='submit'][value='Submit']").click()
for e in range(0,len(month)):
    driver.find_element_by_css_selector(f"input[type='checkbox'][value='{month[e]}/2021']").click()
driver.find_element_by_name("allSes").click()
driver.find_element_by_name("allDay").click()
while retry == True:
    try:
        driver.find_element_by_name("btnSearch").click()
        if driver.find_element_by_name ("slot").is_displayed() ==  True:
            try:
                driver.find_element_by_name("slot").click()
                driver.find_element_by_css_selector("input[type='button'][value='Submit']").click()
                driver.find_element_by_css_selector("input[type='submit'][value='Confirm']").click()
                try:
                    checkout = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td/span/table/tbody/tr/td/table/tbody/tr[2]/td/ul/span[2]").get_attribute("innerHTML")
                    if checkout == "* No Slot available (MaxCap)":
                        print(f"{member} checkout failed for {USER}, {type} {simulator_module}!")
                        send_message_logs(f"{member} checkout failed for {USER}, {type} {simulator_module}!")
                except:
                    print("Checkout success")
                    restart = False
                    retry = False
                finally:
                    break
            except NoSuchElementException:
                pass
    except NoSuchElementException:
        pass
    if retry == True:
        time.sleep(delay)
        driver.find_element_by_name ("btnBack").click()
        monitor += 1
    else:
        pass
    if monitor == 3000:
        driver.close()
        monitor = 1
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://info.bbdc.sg/members-login/")
    else:
        pass
