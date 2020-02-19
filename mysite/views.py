from django.shortcuts import render
from .models import Comics, ComicsDetail
from .comic_utils import find_comics
import requests
from seleniumwire import webdriver as wd
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
from blog import settings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Create your views here.


def index(request):
    comic_qs = Comics.objects.all()[:10]
    return render(request, 'index.html', {'comics': comic_qs})


def comic_viewer(request, title, episode):
    # 타이틀 코드로 우리가 해당 웹툰이 있는지 확인
    # 없다면, 없어요! 라고 경고띄우줄것
    # 있다면, 데이터베이스에 가서 주어진 episode 번호가 있는지 확인할 것.
    # 있다면, 그대로 웹툰을 보여줄것.
    # 없다면, 네이버에 가서 가지고 와 데이터베이스에 저장 후 보여줄것.

    comic_qs = Comics.objects.filter(title_code=title)

    if comic_qs.exists():
        try:
            comic_episode_qs = ComicsDetail.objects.get(comic_id=comic_qs.first().id)
        except Exception as e:
            print("코믹이 없어", e)
            # base_url = 'https://comic.naver.com/webtoon/detail.nhn'
            # header = {
            #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            # param = {"titleId": comic_qs.first().comic_code, "no": episode}
            # req = requests.get(base_url, params=param, headers=header)
            # print(req.text)
            profile = webdriver.FirefoxProfile()
            # profile.set_preference("general.useragent.override", "[user-agent string]")
            # Below is tested line
            profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0")
            driver = webdriver.Firefox(executable_path=os.path.join(settings.BASE_DIR, 'mysite/utils/geckodriver'), firefox_profile=profile)
            driver.get("https://comic.naver.com/webtoon/detail.nhn?titleId={}&no={}".format(comic_qs.first().comic_code, str(episode)))
            WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME,"wt_viewer")))
            html = driver.page_source
            print(html)





