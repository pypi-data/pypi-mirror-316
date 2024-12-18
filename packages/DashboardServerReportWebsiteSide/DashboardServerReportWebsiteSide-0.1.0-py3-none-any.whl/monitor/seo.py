from bs4 import BeautifulSoup
import requests


def get_seo_details(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # seo_data = {
        #     "title": soup.title.string if soup.title else "No Title",
        #     "meta_description": soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={
        #         "name": "description"}) else "No Meta Description",
        #     "keywords": soup.find("meta", attrs={"name": "keywords"})["content"] if soup.find("meta", attrs={
        #         "name": "keywords"}) else "No Keywords",
        #     "h1": soup.find("h1").text if soup.find("h1") else "No H1 Tag"
        # }

        seo_data = {
            "title": soup.title.string if soup.title else "No Title",
            "meta_description": soup.find("meta", attrs={"name": "description"})["content"]
            if soup.find("meta", attrs={"name": "description"}) else "No Meta Description",
            "keywords": soup.find("meta", attrs={"name": "keywords"})["content"]
            if soup.find("meta", attrs={"name": "keywords"}) else "No Keywords",
            # "h1": soup.find("h1").text if soup.find("h1") else "No H1 Tag",
            "tag_counts": {
                "h1 tag": len(soup.find_all("h1")),
                "h2 tag": len(soup.find_all("h2")),
                "h3 tag": len(soup.find_all("h3")),
                "img tag": len(soup.find_all("img")),
                "a tag": len(soup.find_all("a")),
                "p tag": len(soup.find_all("p")),
            },
        }

        return seo_data
    except Exception as e:
        return {"error": str(e)}
