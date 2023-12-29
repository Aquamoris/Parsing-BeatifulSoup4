import requests
import pickle
from bs4 import BeautifulSoup

url = 'https://auto.drom.ru/mercedes-benz/'
amount = 15


def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r


def get_data(url, tag, className):
    soup = BeautifulSoup(url, 'html.parser')
    raw_data = soup.find_all(tag, className)
    raw_data = raw_data[:amount]

    data = []

    if tag == 'a':
        [data.append(i.get('href')) for i in raw_data]
    else:
        [data.append(i.text) for i in raw_data]

    [print(i) for i in data]
    print('\n')

    return data


def get_content(html):
    titles = get_data(html, 'div', 'css-1wgtb37 e3f4v4l2')

    links = get_data(html, 'a', 'css-1oas0dk e1huvdhj1')

    prices = get_data(html, 'span', 'css-46itwz e162wx9x0')
    for i in range(amount):
        prices[i] = prices[i].replace(u'\xa0', u' ')

    info = get_data(html, 'div', 'css-1fe6w6s e162wx9x0')

    cars_info = []

    for i in range(amount):
        cars_info.append({
            'title': titles[i],
            'link': links[i],
            'price': prices[i],
            'info': info[i]
        })

    [print(i) for i in cars_info]

    with open(r'file.txt', 'w+', encoding='UTF-8') as f:
        for i in range(amount):
            write_data = cars_info[i].values()
            [f.write(f'{i} ') for i in write_data]
            f.write('\n')

    f.close()


def parse():
    html = get_html(url)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


parse()
