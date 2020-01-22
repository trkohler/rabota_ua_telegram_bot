import requests
from bs4 import BeautifulSoup
import re
import pprint

URL_BASE = 'https://rabota.ua/'


def create_custom_rabota(titles: list, lines_with_salaries: list):
    jobs = []
    for inx, item in enumerate(titles):
        salary = lines_with_salaries[inx].select('.f-vacancylist-characs-block p.-price')
        if len(salary):
            salary = salary[0].get_text()
            salary = re.sub('[\xa0 грн]', '', salary)
            salary = int(salary)
        else:
            salary = 0
        a_tag = titles[inx].find('a')
        link = URL_BASE + a_tag.get('href')
        title = titles[inx].get_text()
        title = re.sub('[\r\n\t]', '', title)
        jobs.append({'title': title, 'link': link, 'salary': salary})
    return sort_jobs_by_salaries(jobs)


def sort_jobs_by_salaries(jobs):
    return sorted(jobs, key=lambda k: k['salary'], reverse=True)


response = requests.get(url='https://rabota.ua/zapros/Django/%d0%ba%d0%b8%d0%b5%d0%b2', timeout=5)
soup = BeautifulSoup(response.text, 'html.parser')
titles = soup.select('.fd-beefy-gunso')
lines_with_salaries = soup.select('.f-vacancylist-characs-block')
if __name__ == '__main__':
    pprint.pprint(create_custom_rabota(titles, lines_with_salaries))
