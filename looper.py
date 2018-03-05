from selenium import webdriver
import os, random, time

i = 0
numPage = 0
allUsers = []

def getButtons(driver):
    global numPage

    nextButton = None

    pagination = driver.find_elements_by_class_name("pagination")

    for button in pagination:
        buttons = button.find_elements_by_tag_name("a")

        for button in buttons:
            if button.text == "Next":
                nextButton = button

                if nextButton.get_attribute("class") == "disabled":
                    return False
                else:
                    numPage += 1
                    return True

def getFollowers(driver):
    global allUsers

    #Grab user blocks
    userItems = driver.find_elements_by_class_name('pl-1')

    for userItem in userItems:
        if userItem not in allUsers:
            allUsers.append(userItem.text)

def getUsers():
    global numPage, i, allUsers

    users = []


    fname = "users" + str(random.randint(1000000, 9999999)) + '.txt'

    #os.environ['MOZ_HEADLESS'] = '1'
    driver = webdriver.Firefox()

    driver.get("http://calmkai.oyosite.com/listofusers.html")

    #Grab table cells
    table = driver.find_elements_by_tag_name('tbody')

    for tableCell in table:
        aTags = tableCell.find_elements_by_tag_name('a')

        for aTag in aTags:
            users.append(aTag.text)

    for user in users:
        global i, numPage

        if user and i <= 10:
            driver.get("https://github.com/" + user + "?tab=followers")

            numPage = 0

            nextVal = getButtons(driver)

            while nextVal:

                driver.get("https://github.com/" + user + "?page=" + str(numPage) + "&tab=followers")

                getFollowers(driver)

                nextVal = getButtons(driver)

                time.sleep(random.randint(3, 6))

            i += 1

    print len(allUsers)

    with open('temp/' + fname, 'w') as f:
        for user in allUsers:
            f.write(user + "\n")
    print fname

getUsers()
