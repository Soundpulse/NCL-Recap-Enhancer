#importing necessary libs
import os
import time
import getpass
import glob
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

print("[!] Starting script")

SLEEP_TIME = 5

# Asking user for login credentials
username = input("Enter your uni username: ")
password = getpass.getpass()
print("[+] Details accepted")

# Set current running path
currentPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Setup & launch web driver
print("[+] Launching chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") # Start maximized
options.add_argument("--mute-audio") # Mute audio
# Remove remember password dialog box
options.add_experimental_option('prefs', {'credentials_enable_service': False,'profile': {'password_manager_enabled': False}})
capabilities = DesiredCapabilities().CHROME.copy()
capabilities["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(currentPath + '\chromedriver.exe',chrome_options=options,desired_capabilities=capabilities)

print("[+] Starting login process")
try:	
    driver.get("https://campus.recap.ncl.ac.uk/Panopto/Pages/Sessions/List.aspx?embedded=0#maxResults=250&isSharedWithMe=true")
    time.sleep(2*SLEEP_TIME)
    driver.find_element_by_xpath('//*[@id="loginButton"]').click()
    driver.find_element_by_xpath('//*[@id="loginControl_externalLoginButton"]').click()
    time.sleep(SLEEP_TIME)
    id = driver.find_element_by_id("loginFormList").find_element_by_id("user_id")
    id.clear()
    id.send_keys(username)

    pw = driver.find_element_by_id("password")
    pw.clear()
    pw.send_keys(password)
	
    driver.find_element_by_xpath('//*[@id="entry-login"]').click()

    # Wait for user to login
    while True:
        time.sleep(SLEEP_TIME)
        if driver.current_url == "https://campus.recap.ncl.ac.uk/Panopto/Pages/Sessions/List.aspx?embedded=0#maxResults=250&isSharedWithMe=true":
            print("[+] Logged in as "+username.upper())
            break
except:
    # Error
    print("[+] Unable to login - Restart script and try again with correct login details")
    print("[!] Exiting the script")
    exit()

# Sleep to allow browser to load page fully (aspx)
print("[+] Waiting for page to load")
time.sleep(SLEEP_TIME)

# Find all links that lead to videos
print("[+] Begin link scrapping")
videos = driver.find_elements_by_xpath("//a[@class='detail-title']")

# Empty dict to store links and file names
links_dict={}

# Loop through video objects and and save links
video_count = 0;

for video in videos:
    if video.text != "" and re.search("^CSC2024.*|^CSC2026.*|^CSC2021.*", video.text): # Gets rid of non video links
        print("Retrieving..." + str(video.text));
        links_dict[video.get_attribute("href")] = video.text
        video_count += 1;

print("Retrieved " + str(video_count) + " videos.");
		
# Make output directory
if not os.path.exists(currentPath+"\\raw_vids"):
    os.makedirs(currentPath+"\\raw_vids")

video_count = 0;
# Iterate through each video
for key, value in links_dict.items():
#   try:
    driver.get(key) # Go to video page
    time.sleep(SLEEP_TIME)
    # Find link to podcast file
    link = driver.find_element_by_xpath("//meta[@name='twitter:player:stream']").get_attribute("content")
    print("Trying to get link...")
    driver.get(link) # Go to podcast file and allow for redirect
    time.sleep(SLEEP_TIME)
    url = str(driver.current_url)
    print("Downloading " + url)
    os.system('youtube-dl.exe {0}'.format(url)) # Download the file
    newest = max(glob.iglob('*.[Mm][Pp]4'), key=os.path.getctime) # Get newest file
    os.rename(newest, currentPath+"\\raw_vids\\"+value.replace("/","-").replace(" ","-").replace(":","") +".mp4") # Rename file to correct name
    video_count += 1;
    print("Finished downloading (" + str(video_count) + "): " + value+"\n") # Output that file has finished downloading
#   except Exception as e:
#       print("Error fetching: "+str(value)+" at "+str(key)+"\n") # Error message
#       print(e)

driver.quit() # Close the webdriver

# Add ffmpeg compression script here if not lazy

# Remove debug log made by chrome driver
try:
    os.remove("debug.log")
except Exception as e:
    pass

# Print exit messages
print("[+] Script has finished downloading all files")
print("[+] Exiting script")
exit()
