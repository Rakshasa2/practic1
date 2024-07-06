import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def fetch_url(url: str) -> requests.Response:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Ошибка при запросе URL {url}: {e}")
        return None

def parse_hh(keyword: str) -> List[Dict[str, str]]:
    url = f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&fromSearchLine=true&text={keyword}'
    response = fetch_url(url)
    if not response:
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    vacancies = []
    for item in soup.find_all('div', class_='vacancy-serp-item'):
        title = item.find('a', class_='bloko-link').text
        company = item.find('div', class_='vacancy-serp-item__meta-info-company').text.strip()
        link = item.find('a', class_='bloko-link')['href']
        vacancies.append({'title': title, 'company': company, 'link': link})
    return vacancies

def parse_avito(keyword: str) -> List[Dict[str, str]]:
    url = f'https://www.avito.ru/moskva/vakansii?q={keyword}'
    response = fetch_url(url)
    if not response:
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    vacancies = []
    for item in soup.find_all('div', class_='item__line'):
        title = item.find('a', class_='snippet-link').text
        link = 'https://www.avito.ru' + item.find('a', class_='snippet-link')['href']
        vacancies.append({'title': title, 'link': link})
    return vacancies

def parse_habr(keyword: str) -> List[Dict[str, str]]:
    url = f'https://career.habr.com/vacancies?q={keyword}'
    response = fetch_url(url)
    if not response:
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    vacancies = []
    for item in soup.find_all('div', class_='vacancy-card'):
        title = item.find('div', class_='vacancy-card__title').text.strip()
        link = 'https://career.habr.com' + item.find('a')['href']
        vacancies.append({'title': title, 'link': link})
    return vacancies