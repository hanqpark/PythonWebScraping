import requests
from bs4 import BeautifulSoup


def get_last_page(URL):
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job_info(html):
    title = html.find("h2").find("a")["title"]
    # recursive=False는 span안의 span을 더 탐색하지 않도록 방지해 줌. 쓸모없는 정보를 가져오지 않게 하기 위해 사용
    company, location = html.find("h3").find_all("span", recursive=False)
    id = html['data-jobid']
    return {"title": title, 'company': company.get_text(strip=True), 'location': location.get_text(strip=True),
            'link': f"https://stackoverflow.com/jobs/{id}"}


def extract_jobs(URL, last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page+1} from StackOverFlow")
        res = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(res.text, "html.parser")
        result = soup.find_all("div", {"class": "-job"})
        for r in result:
            job = extract_job_info(r)
            #print(job)     잘 구동되는지 확인하기
            jobs.append(job)
    return jobs


def get_jobs(word):
	URL = f"https://stackoverflow.com/jobs?q={word}"
	last_page = get_last_page(URL)
	jobs = extract_jobs(URL, last_page)
	return jobs
 