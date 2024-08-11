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
pwd_url = "https://labs.play-with-docker.com/"
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
    time.sleep(50)
    try:
        # Click x button to close accept cookies popup
        cookies_div_id = 'onetrust-group-container'
        try:
            cookies_div = False
            cookies_div = WebDriverWait(driver, to).until(
                    EC.visibility_of_element_located((By.ID, cookies_div_id))
                    )
        except:
            print("Cookies pop not found!")
        if(cookies_div):
            #x_button = x_div.find_element(By.TAG_NAME, 'button')
            accept_button_id = 'onetrust-accept-btn-handler'
            accept_button = WebDriverWait(driver, to).until(
                    EC.visibility_of_element_located((By.ID, accept_button_id))
                    )
            print("Closing cookies popup")
            actions.move_to_element(accept_button).click().perform()
            time.sleep(50)
            #x_button.click()
    except Exception as error:
        print("Something went wrong, failed to click X butn. skipping it.", error)

    #driver.close()

def create_pwd_container():
    # Go to pwd
    driver.get(pwd_url)

    # Get the login button

    print(driver.title)
    button1 = driver.find_element(By.ID, "btnGroupDrop1")
    # Click the login button (button1)
    print("Clicking login button...")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "btnGroupDrop1"))).click()
    # Get the docker button
    button2 = driver.find_element(By.CLASS_NAME, "ng-binding")

    dropdown_menu = driver.find_elements(By.CLASS_NAME, "dropdown-menu")
    print("Clicking the docker parent div of a tag")
    actions = ActionChains(driver)
    actions.move_to_element(dropdown_menu[0]).click().perform()

    # select form element
    form_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "landingForm")))

    # select start button
    time.sleep(10)
    start_button = form_element.find_element(By.TAG_NAME, "a")
    # Next click on start button
    print("Clicking the start button...")
    print(start_button.text)
    actions.move_to_element(start_button).click().perform()
    print("")

    #print(driver.title)
    #print(driver.current_url)

    print("Sleeping 10 seconds...")
    time.sleep(10)
    print("")

    print(driver.title)
    print(driver.current_url)
    print("")

    if("ooc" in driver.current_url):
        print("Out of Capacity detected...")
        print("Sleep 10 seconds..")
        time.sleep(10)
        print("Getting to start url")
        driver.get("https://labs.play-with-docker.com/")
    else:
        layout_column = driver.find_element(By.CLASS_NAME, "layout-column")
        md_sidenav = layout_column.find_element(By.TAG_NAME, "md-sidenav")
        md_content_main = layout_column.find_element(By.TAG_NAME, "md-content")
        md_content_sidenav = md_sidenav.find_element(By.TAG_NAME, "md-content")
        add_button = md_content_sidenav.find_element(By.TAG_NAME, "button")
    #start_button = form_element.find_element(By.TAG_NAME, "a")
    print("Clicking add new instance button...")
    print(add_button.text)
    actions.move_to_element(add_button).click().perform()
    
    print("Sleeping 20 seconds....")
    time.sleep(20)

    print("Getting ssh command...")
    try:
        md_card = layout_column.find_element(By.TAG_NAME, "md-card")
        input_3 = md_card.find_element(By.ID, "input_3")
        print(input_3.get_attribute("value"))

        terminal_instance = layout_column.find_element(By.CLASS_NAME, "terminal-instance")
        terminal = terminal_instance.find_element(By.CLASS_NAME, "terminal")
        command = "kill -9 $(ps aux | grep 'sshd: /usr' | awk '{print $1}') && /usr/sbin/sshd -o PermitRootLogin=yes -o PrintMotd=yes -o AllowAgentForwarding=yes -o AllowTcpForwarding=yes -o X11Forwarding=yes -o X11DisplayOffset=10 -o X11UseLocalhost=no"
        print("Clicking terminal....")
        actions.move_to_element(terminal).click().perform()
        print("Sending commands...")
        terminal.send_keys(command, Keys.RETURN)
        print("Started docker")
        # Now we reached desired state so stay here
        print(driver.get_cookies())
        print(driver.current_url)
        print("")
        cookies = driver.get_cookies()
        print(cookies[-1])
        stop = input("")
    except:
        print("Failed to create new instance retrying..., sleep 10 seconds...")
        time.sleep(10)
        #continue
    # Find the close session button
    md_toolbar = md_sidenav.find_element(By.TAG_NAME, "md-toolbar")
    close_button = md_toolbar.find_element(By.TAG_NAME, "button")
    print("Pressing close button...")
    actions.move_to_element(close_button).click().perform()
    print("Waiting until session closes...")
    time.sleep(10)

def logout_from_docker():
    # Open docker hub (assume already logged in)
    driver.get(docker_hub_url)
    time.sleep(50)
    try:
        # Click x button to close accept cookies popup
        cookies_div_id = 'onetrust-group-container'
        try:
            cookies_div = False
            cookies_div = WebDriverWait(driver, to).until(
                    EC.visibility_of_element_located((By.ID, cookies_div_id))
                    )
        except:
            print("Cookies pop not found!")
        if(cookies_div):
            #x_button = x_div.find_element(By.TAG_NAME, 'button')
            accept_button_id = 'onetrust-accept-btn-handler'
            accept_button = WebDriverWait(driver, to).until(
                    EC.visibility_of_element_located((By.ID, accept_button_id))
                    )
            print("Closing cookies popup")
            actions.move_to_element(accept_button).click().perform()
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
    create_pwd_container()
    logout_from_docker()
finally:
    # Finally close driver
    driver.quit()

