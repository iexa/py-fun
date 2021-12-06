from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# microsoft edge driver for selenium required (on the path)
driver = webdriver.Edge()

driver.get('https://www.seleniumeasy.com/python/example-code-using-selenium-webdriver-python')

# try:
#     el = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, 'recaptcha-anchor')))
# except TimeoutException:
#     print('could not locate captcha in 10 secs')

comment_name = driver.find_element_by_xpath('//*[@id="edit-name"]')
comment_name.send_keys('Flik-flak')
comment_btn = driver.find_elements_by_xpath('//*[@id="edit-comment-body-und-0-value"]')
comment_btn.click()

