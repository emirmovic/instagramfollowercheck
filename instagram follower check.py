from tkinter import *

import sys
import getpass

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time


def finalArrayGUI(finalArray, driver):
    def confirm():
        unfollowList = []
        for i in range(len(finalArray)):
            if (check_boxes[finalArray[i]].get() == 1):
                unfollowList.append(finalArray[i])
        print(unfollowList)

        error_list = []
        for item in unfollowList:
            try:
                time.sleep(1.2)
                search = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')
                search.clear()
                search.send_keys(item)
                time.sleep(1.5)
                search.send_keys(Keys.TAB)
                search.send_keys(Keys.ENTER)

                time.sleep(1.5)
                clickunfollow = driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
                clickunfollow.click()
                driver.implicitly_wait(3)
                clicksure = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
                clicksure.click()
            except:
                error_list.append(item)
                continue


        print("We're sorry. These users didnt work.\n" , error_list)
        master2.destroy()

    master.destroy()

    master2 = Tk()
    master2.title("everyone")


    count = 0
    rownum = 5
    colnum = 0


    check_boxes = {item:IntVar() for item in finalArray} #create dict of check_boxes

    while count < len(finalArray):
        if colnum == 10:
            colnum = 0
            rownum += 2
        Label(master2, text = finalArray[count]).grid(row = rownum, column = colnum, ipadx = 30)

        C = Checkbutton(master2, text="unfollow", variable = check_boxes[finalArray[count]]).grid(row= rownum + 1, column = colnum, ipadx = 5)

        count += 1
        colnum += 1

    button = Button(master2, text="unfollow selected", fg="red", pady = 10, command = confirm)
    button.grid(row = rownum+2,column=4)

    master2.mainloop()

def analyzeFollowers(driver, followers, totalFollowers):
    driver.implicitly_wait(2)
    tabthrough = driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    tabthrough.click()

    actionChain = webdriver.ActionChains(driver)
    actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
    tabthrough.click()

    i = 0
    numberOfFollowersInList = len(tabthrough.find_elements_by_css_selector('li'))
    while (numberOfFollowersInList < totalFollowers):
        if i < 5:
            tabthrough.click()
            i += 1
        actionChain.key_down(Keys.SPACE).perform()
        numberOfFollowersInList = len(tabthrough.find_elements_by_css_selector('li'))
        time.sleep(0.5)
    actionChain.key_up(Keys.SPACE).perform()


    ### Put the followers into an array ###
    arrayOfFollowers = []

    for i in range(1, numberOfFollowersInList+1):
        account = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li[' + str(i) + ']/div/div[1]/div[2]/div[1]/a')
        arrayOfFollowers.append(account.get_attribute("title"))

    pressexit = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div[2]/button')
    pressexit.click()


    ### Scrolls down followers list ###
    totalFollowing = driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a/span')
    totalFollowing = int(totalFollowing.text.replace(",",""))

    print(totalFollowing)

    driver.implicitly_wait(2)

    following = driver.find_element_by_partial_link_text("following")
    following.click()

    driver.implicitly_wait(2)

    #following
    tabthrough = driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    tabthrough.click()

    actionChain = webdriver.ActionChains(driver)
    actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
    tabthrough.click()

    n = 0
    numberOfFollowingInList = len(tabthrough.find_elements_by_css_selector('li'))
    while (numberOfFollowingInList < totalFollowing):
        if n < 5:
            tabthrough.click()
            n += 1
        actionChain.key_down(Keys.SPACE).perform()
        numberOfFollowingInList = len(tabthrough.find_elements_by_css_selector('li'))
        time.sleep(0.5)
    actionChain.key_up(Keys.SPACE).perform()

    arrayOfFollowing = []

    for i in range(1, numberOfFollowingInList+1):
        account = driver.find_element_by_xpath('//html/body/div[3]/div/div[2]/ul/div/li[' + str(i) + ']/div/div[1]/div[2]/div[1]/a')
        arrayOfFollowing.append(account.get_attribute("title"))

    finalArray = []

    for i in range(len(arrayOfFollowing)):
        if arrayOfFollowing[i] not in arrayOfFollowers:
            finalArray.append(arrayOfFollowing[i])

    print("List of people that don't follow you back: " + str(finalArray))

    pressexit = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div[2]/button')
    pressexit.click()


    finalArrayGUI(finalArray, driver)

def goToProfile(driver, usernameInput, seconds):
    driver.implicitly_wait(2)
    search = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')
    search.clear()
    search.send_keys(usernameInput)
    time.sleep(seconds)
    search.send_keys(Keys.TAB)
    search.send_keys(Keys.ENTER)

    totalFollowers = driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a/span')
    totalFollowers = int(totalFollowers.text.replace(",",""))

    driver.implicitly_wait(2)
    followers = driver.find_element_by_partial_link_text("followers")
    followers.click()
    analyzeFollowers(driver, followers, totalFollowers)

def instagramLogin(usernameInput, passwordInput):
    opsys = sys.platform
    user = getpass.getuser()
    if opsys == "win32":
        driver = webdriver.Chrome('/Users/'+user+'/Documents/GitHub/instagramfollowercheck/chromedriver_windows')
    elif opsys == "darwin":
        driver = webdriver.Chrome('/Users/'+user+'/Desktop/instagramfollowercheck/chromedriver_mac')
    driver.get('https://www.instagram.com/accounts/login/?hl=en')

    driver.implicitly_wait(1)
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(usernameInput)

    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(passwordInput)

    password.send_keys(Keys.RETURN)

    time.sleep(1.8)
    try:
        notnow = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[1]")
        notnow.click()
    except:
        pass

    goToProfile(driver, usernameInput, 1)

def setVariables():
    usernameInput = entry1.get()
    passwordInput = entry2.get()
    instagramLogin(usernameInput, passwordInput)

### Sets up the starting GUI ###
master = Tk()
master.configure(background="#031229", padx = 10, pady = 20)
master.minsize(300,150)
master.title("Instagram Input")

entry1 = Entry(master, font =('Verdana', 10), justify = CENTER)
entry2 = Entry(master, font =('Verdana', 10), justify = CENTER, show="*")

Label(master, text = "Find Your Instagram Unfollowers", font =('Verdana', 18), bg = "#031229", fg = "white").grid(columnspan = 2, padx = 20, pady = 10)

Label(master, text = "Username:", font =('Verdana', 14), bg = "#031229", fg = "white").grid(row = 1, padx = 10, pady = 10, sticky = E)
entry1.grid(row = 1, column = 1, ipadx = 5, sticky = W, pady = 10)

Label(master, text = "Password:", font =('Verdana', 14), bg = "#031229", fg = "white").grid(row = 2, padx = 10, sticky = E)
entry2.grid(row = 2, column = 1, ipadx = 5, sticky = W+N, pady = 10)

button = Button(master, text="Submit", font = ('Verdana', 11), bg = "#29364a", fg = "white", command=setVariables)
button.grid(row=4,columnspan=2, ipadx = 40, pady = 20)

img = PhotoImage(file = r"../instagramfollowercheck/instagram_icon.png")
img1 = img.subsample(4, 4)

Label(master, image = img1, bg = "#031229").grid(row = 5,
       columnspan = 2, rowspan = 2, padx = 1, )

master.mainloop()
