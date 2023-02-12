import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_headers():
    return Headers(browser="chrome", os="win").generate()


def get_text(url):
    return requests.get(url, headers=get_headers()).text


def get_data():
    data_list = []
    link = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    page = '&page='
    num = 0
    html = get_text(link)
    while num < 10:
        src_page = BeautifulSoup(html, features="lxml")
        vacancies = src_page.find('div', class_="vacancy-serp-content").find_all('div', class_="serp-item")
        for vacancy in vacancies:
            if "Django" in vacancy.text and "Flask" in vacancy.text:
                salary = vacancy.find('span', class_="bloko-header-section-3")
                if salary is None:
                    salary = 'зарплата не указана'
                else:
                    salary = salary.text.replace('\u202f', ' ')
                if 'USD' in salary:  # Доп задание. Можно убрать иначе выборка может быть пустой.
                    data_list.append(
                        {
                            'Вакансия': vacancy.find('a', class_="serp-item__title").contents[0],
                            'Компания': vacancy.find('div', class_="vacancy-serp-item__meta-info-company")
                            .contents[0].text.replace('\xa0', ' '),
                            'Город': vacancy.find('div', class_="vacancy-serp-item__info").contents[1].contents[0],
                            'ссылка': vacancy.find('a', class_="serp-item__title").attrs['href'],
                            'заработная плата': salary
                        }
                    )
        num += 1
        link += f"{page}{str(num)}"
        html = get_text(link)
    return data_list


if __name__ == "__main__":
    data = get_data()
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=5)
