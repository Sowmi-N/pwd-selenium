from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait                                           
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

# Load local .env
load_dotenv()

# Load variables
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

# Defining default options for chrome browser
options = webdriver.ChromeOptions()               
options.add_argument('--ignore-ssl-erros=yes')    
options.add_argument('--ignore-certificate-errors')

# Set chrome driver port
driver = webdriver.Remote(
        command_executor = 'http://localhost:4444/wd/hub',                                                  options = options                         )

# Global variables
to = 30 # Timeout
errors = [NoSuchElementException, ElementNotInteractableException]
wait = WebDriverWait(driver, timeout=to, poll_frequency=.9, ignored_exceptions=errors)
actions = ActionChains(driver)

# Implicit wait
driver.implicitly_wait(to)

# Create variable for docker login page

docker_login_url = "https://login.docker.com/u/login"
play_with_docker_url = "https://labs.play-with-docker.com/"
docker_hub_url = "https://hub.docker.com"

def login_to_docker():
    # Go to docker login page
    driver.get(docker_login_url)

    # Get the current window handle
    current_window = driver.current_window_handle

    # Now fill the username into username input   
    #username_xpath = '/html/body/div/main/section/div[1]/div/div/div[1]/div/form/div[1]/div/div/div/div'
    username_ele = WebDriverWait(driver, to).until(
            EC.visibility_of_element_located((By.ID, "username"))
            )
    #username = driver.find_element(By.XPATH, username_xpath)
    print("Writing username...")
    wait.until(lambda d : username_ele.send_keys(username, Keys.RETURN) or True)

    # Now fill the password
    #password_xpath = '//*[@id="password"]'
    password_ele = WebDriverWait(driver, to).until(
            EC.visibility_of_element_located((By.ID, "password"))
            )
    print("Writing password...")
    wait.until(lambda d : password_ele.send_keys(password, Keys.RETURN) or True)

#   while(a != "exit"):
#       print("Enter exit to exit...")
#       a = input("")
    time.sleep(20)
    #driver.close()

def logout_from_docker():
    # Open docker hub (assume already logged in)
    driver.get(docker_hub_url)

    try:
        # Click x button to close accept cookies popup
        x_div_id = 'onetrust-close-btn-container'
        x_div = WebDriverWait(driver, to).until(
                EC.visibility_of_element_located((By.ID, x_div_id))
                )
        x_button = x_div.find_element(By.TAG_NAME, 'button')
        print("Closing cookies popup")
        actions.move_to_element(x_div).click().perform()
        #x_button.click()
    except Exception as error:
        print("Something went wrong, failed to click X butn. skipping it.", error)

    # Click user profile icon
    user_profile_xpath = '/html/body/div[2]/div/header/div/div/div[2]/button[2]/div'
    user_profile_css = 'button.MuiIconButton-root:nth-child(6)'
    user_profile = WebDriverWait(driver, to).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, user_profile_css))
            )
    print("Clicking user profile")
    actions.move_to_element(user_profile).click().perform()
    #user_profile.click()

    # Click signout button to sign out
    sign_out_xpath = '/html/body/div[2]/div/header/div/div/div[2]/div[4]/div[3]/div/nav/button'
    sign_out_css = '.css-10dwyil'
    sign_out = WebDriverWait(driver, to).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, sign_out_css))
            )
    print("clicking signout")
    actions.move_to_element(sign_out).click().perform()
    #sign_out.click()
    time.sleep(20)
    driver.close()

try:
    time.sleep(20)
    login_to_docker()
    logout_from_docker()
finally:
    # Finally close driver
    driver.quit()

