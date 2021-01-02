import requests
from bs4 import BeautifulSoup

LIMIT = 50

# 각 페이지를 불러오는 함
def get_last_page(URL):
    # HTML 정보를 다 가져옴
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    # pagination => page 매김 프로세스를 일컫는 용어
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page


def extract_job_info(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_a = company.find("a")
    if company_a is not None:
        company = str(company_a.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {"title": title, "company": company, "location": location,
            "link": f"https://www.indeed.com/viewjob?jk={job_id}"}


# 페이지 내의 직업 및 직장 정보 불러오는 함
def extract_jobs(URL, last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page+1} from Indeed")
        res = requests.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for r in result:
            job = extract_job_info(r)
            jobs.append(job)
    return jobs


def get_jobs(word):
    URL = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"
    last_page = get_last_page(URL)
    jobs = extract_jobs(URL, last_page)
    return jobs
