from bs4 import BeautifulSoup
import requests


def web_scrape(searchData, link, class_name, list):
    searchData = searchData.replace(" ", "+")
    response = requests.get(link + searchData.lower())
    soup = BeautifulSoup(response.content, "html.parser")
    page = (
        soup.find("div", {"class": class_name})
        if not list
        else soup.find_all("div", {"class": class_name})
    )
    return page


def search(searchData):
    try:
        page = web_scrape(
            searchData,
            "https://www.fandom.com/?s=",
            "post grid-block small-12 mediawiki-article",
            False,
        )
        results = page.find_all("a")
        finalResponse = requests.get(results[0]["href"])
        finalSoup = BeautifulSoup(finalResponse.content, "html.parser")
        information = finalSoup.find("div", {"class": "mw-parser-output"})
        textSection = information.find_all("p", recursive=False)
        return textSection[1].text
    except:
        return "No Data Found On This Topic"


def getNews():
    response = requests.get("https://www.bbc.com/news")

    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find("body").find_all("h2")

    responses = ""
    for i in range(len(headlines)):
        if i > 6:
            break
        if headlines[i].text not in responses:
            responses += headlines[i].text + "\n"
            i -= 1
    return responses


def getWeather():
    response = requests.get(
        "https://weather.com/weather/today/l/1df7354798a71c2a87c94fad701382c964decc25e1250e3ec34e7739d42b41e7"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    temp = soup.find("span", {"class": "CurrentConditions--tempValue--MHmYY"})
    forecast = soup.find("div", {"class": "CurrentConditions--phraseValue--mZC_p"})

    return "It is currently " + temp.text + " and " + forecast.text
