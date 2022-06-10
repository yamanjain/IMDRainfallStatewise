import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import time
from datetime import date

options = Options()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


today = str(date.today())
url = 'http://hydro.imd.gov.in/hydrometweb/(S(12xczcij0lp2xf3bi0fyw045))/DistrictRaifall.aspx'
# opening the url
driver.get(url)
time.sleep(2)

# Change the value of sleeplarge to make program run fast or slow depending on internet speed
sleeplarge = 0.1

dropdown_1 = driver.find_element(by=By.ID,value="listItems")
drp = Select(dropdown_1)
state_nos = len(drp.options) - 1
print("Total number of States is - ", state_nos)

mdataset = pd.DataFrame()

i = 0

while i < state_nos:
    i = i + 1
    j = 1

    dropdown_1 = driver.find_element(by=By.ID, value="listItems")
    drp = Select(dropdown_1)

    drp.select_by_index(i)
    time.sleep(sleeplarge)

    o = Select(driver.find_element(by=By.ID, value="listItems")).first_selected_option
    statename = o.text
    print("Selected State is: " + statename)

    dropdown_2 = driver.find_element(by=By.ID, value="DistrictDropDownList")
    drp_2 = Select(dropdown_2)
    district_nos = len(drp_2.options)
    print("Total number of districts in ", o.text, " is - ", district_nos)

    while j < district_nos:
        dropdown_2 = driver.find_element(by=By.ID, value="DistrictDropDownList")
        drp_2 = Select(dropdown_2)
        drp_2.select_by_index(j)

        p = drp_2.first_selected_option
        distname = p.text
        print("Selected district is: " + distname)

        go = driver.find_element(by=By.ID, value="GoBtn")
        go.click()

        try:
            # Find table in page
            imdtbl = driver.find_element(by=By.ID, value="GridId")
            # Goto parent element since only then table tag will be there for Pandas in innerHTML
            tblparent = imdtbl.find_element(by=By.XPATH, value='..')
            imdtblsrc = tblparent.get_attribute('innerHTML')
            # Use pandas to read all tables in page
            wthtable = pd.read_html(str(imdtblsrc))
            # Weather website has just one table, so select the first table into dataonly
            dataonly = wthtable[0]
            # Repeat District Name in each row
            dataonly.iloc[:, 0] = distname
            # Changing column header
            dataonly.columns.values[0] = "DistName"
            # Repeat State Name in each row
            dataonly.insert(0, 'StateName', statename)

            # Delete top row so that it does not repeat
            dataonly = dataonly.iloc[1:, :]
        except NoSuchElementException as e:
            # No data found case like Lakhswadeep
            print('No data found for ' + statename + ',' + distname)
            dataonly = dataonly.iloc[0]
            dataonly.iloc[2:] = "NODATA"
            dataonly.iloc[1] = distname
            dataonly.iloc[0] = statename
            pass

        # append dataonly for one district to masterdataset
        mdataset = pd.concat([mdataset, dataonly])

        #deprecated
        #mdataset = mdataset.append(dataonly, ignore_index=False, verify_integrity=False)


        # without using pandas with granular control over excel, did not use this approach
        # for row in imdtbl.Find_Elements_By_XPath(".//tr"):
        #     for cell in row.Find_Elements_By_XPath("./td"):
        #         y = y + 1
        #         arrcells[x,y]=cell.text
        # x = x + 1
        # y = 0

        j += 1
        time.sleep(sleeplarge)

# Write everything to excel
mdataset.to_excel(r"C:\Users\yaman\Downloads\output.xlsx", sheet_name=today)

# Use if multiple sheets required datewise
# with pd.ExcelWriter('d:\desktop\output.xlsx',  mode='a', if_sheet_exists="replace") as writer:
#     dataonly.to_excel(writer, sheet_name=today)


print("All done")
