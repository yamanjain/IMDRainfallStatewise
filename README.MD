
# IMD Rainfall Data Scraper

Python project to get districtwise annual rainfall historical data from Indian Metrological Data offical website.
http://hydro.imd.gov.in/hydrometweb/(S(12xczcij0lp2xf3bi0fyw045))/DistrictRaifall.aspx

## Usage/Examples

Usage:
Install all the dependencies needed


```
pip install pipreqs

pip install -r requirements.txt
```

Alternatively you can install the following:
```
pip install selenium
pip install webdriver-manager
pip install pandas
pip install lxml
pip install openpyxl
```

Update the path of output.xlsx in this line:
mdataset.to_excel(r"C:\Users\yaman\Downloads\output.xlsx", sheet_name=today)


## Screenshots

#### Rainfall districtwise data from IMD Website
![IMD Website](/Screenshots/IMD%20Website.jpg?raw=true)

#### Sample Output Excel Sheet
![Excel Output](/Screenshots/Output%20Excel%20sheet.png?raw=true)
