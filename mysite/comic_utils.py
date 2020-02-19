from bs4 import BeautifulSoup
from .models import Comics, ComicsDetail
import requests


def find_comics(title):
    header = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

    title_url = 'https://search.naver.com/search.naver?query='+title
    title_req = requests.get(title_url, headers=header)
    title_soup = BeautifulSoup(title_req.text, 'html.parser')

    title_code = title_soup.find("div", {"class": "cont"}).find("h3").find("a", href=True)
    title_code = str(title_code['href']).split("titleId")[1]

    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId'+title_code+'&no=1'
    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    thumbnail = soup.find_all("div", {"class": "thumb"})

    src = thumbnail[0]
    src = str(src).split(" src=\"")
    thumbnail_img = src[1].split('" title')[0]
    print(thumbnail_img)

    detail = soup.find_all("div", {"class": "detail"})

    detail_child = detail[0].find("h2")
    author = detail_child.find("span").getText()
    author = str(author).strip()
    title = str(detail_child.getText()).replace(author, "").strip()
    catches = detail[0].find("p", {"class": "txt"}).getText()
    catches = str(catches)
    print(catches)
    print(title)
    print(author)

    find_qs = Comics.objects.get_or_create(
        title=title,
        author=author,
        image_path=thumbnail_img,
        catches=catches
    )