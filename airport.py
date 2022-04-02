from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup
import requests
import json

url = "http://airportcode.55cha.com/"
rows = {
    "data": []
}

for i in range(284):
    print("正在爬取第 {} 页数据".format(i))

    temporaryUrl = url + "list_{}.html".format(i)
    
    response = requests.get(temporaryUrl)
    content = response.content.decode()

    soup = BeautifulSoup(content, "html.parser")

    table = soup.find("table", attrs={"class": "center f14"})
    trs = table.find_all("tr")[1:]

    for tr in trs:
        td = tr.find_all("td")

        cityName = td[0].getText()
        cityShort = td[1].getText()
        airportShort = td[2].getText()
        airportName = td[3].getText()
        cityFullName = td[4].getText()

        if airportShort == "" or airportName == "":
            continue

        appendData = {
            "cityName": cityName,
            "cityShortName": cityShort,
            "airportShortCode": airportShort,
            "airportFullName": airportName,
            "cityFullname": cityFullName
        }

        print("插入数据为：{}".format(appendData))
        
        rows["data"].append(appendData)

print(rows)

with open("./airports.json", "wb+") as file:
    file.write(json.dumps(rows).encode())