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
