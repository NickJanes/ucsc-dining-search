import requests, json

from meal_parser import MealParser

headers = {
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', 
    #'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': 'PS_DEVICEFEATURES=width:1536 height:864 pixelratio:1.25 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; WebInaCartDates=; WebInaCartMeals=; WebInaCartRecipes=; WebInaCartQtys=; WebInaCartLocation=25',
}

dining_halls = [
    'Colleges+Nine+%26+Ten+Dining+Hall',
    'Cowell+Stevenson+Dining+Hall',
    'Crown+Merrill+Dining+Hall',
    'Porter+Kresge+Dining+Hall'
]

def update_menu_if_not_found(day, month, year):
    menu = load_menu(day, month, year)
    if menu:
        return menu
    
    menu = get_menu_for_day(day, month, year)
    if menu:
        return menu

    return None

def get_menu_for_day(day, month, year):
    text = ""
    for d_hall in dining_halls:
        url = "https://nutrition.sa.ucsc.edu/shortmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=25&locationName="+d_hall+"l&naFlag=1&WeeksMenus=UCSC+-+This+Week%27s+Menus&myaction=read&dtdate=" + str(month) + "%2f" + str(day) + "%2f" + str(year)
        result = requests.get(url, headers=headers)
        if (result.status_code != 200):
            print("Error - Status Code: " + str(result.status_code))
            return None
        text += result.text
    
    file = open(str(month) + '-' + str(day) + '-' + str(year) + '.html', 'w', encoding='utf-8')
    file.write(result.text)
    file.close
    return result.text

def load_menu(day, month, year):
    try:
        f = open(str(month) + '-' + str(day) + '-' + str(year) + '.html', 'r', encoding='utf-8')
        text = f.read()
        f.close()
        return text
    except:
        print('Could not read ' + str(month) + '-' + str(day) + '-' + str(year) + '.html')
        
    return None

def print_menu(menu, day, month, year):
    meal = ""
    for item in menu:
        if item[0] != meal:
            print(item[0])
            meal = item[0]
        print("\t" + item[1])

def scan_menu(menu, target_food):
    for item in menu:
        if target_food in item[1].lower():
            return item[0] + ": " + item[1]
    return None

month = 11
MAX_MONTH = 12
day = 22
MAX_DAY = 31
year = 2021
MAX_YEAR = 2022

search = "chicken"

parser = MealParser()
#for y in range(year, MAX_YEAR+1):
for m in range(month, MAX_MONTH+1):
    print("Month " + str(m))
    for d in range(day, MAX_DAY):
        menu = update_menu_if_not_found(d, m, year)
        if menu:
            parser.feed(menu)
            menu = parser.load()
            scan = scan_menu(menu, search)
            if scan:
                print(str(month) + "-" + str(d) + "-" + str(year))
                print(scan)
            #print_menu(menu, d, month, year)
            parser.reset_meals()
        else:
            print("No menu for " + str(month) + "-" + str(d) + "-" + str(year))
