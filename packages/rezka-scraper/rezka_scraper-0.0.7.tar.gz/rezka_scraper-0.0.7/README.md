# RezkaScraper

**RezkaScraper** — это мини библиотека на Python для асинхронного поиска контента (аниме, фильмов, сериалов и мультфильмов) на сайте [Rezka.ag](https://Rezka.ag).

## Возможности:
- **Поиск по названию:** Выполняет поиск по ключевому слову и возвращает первое совпадение.
- **Поиск по категориям:** Поддержка категорий аниме, фильмы, сериалы, мультфильмы с пагинацией.
- **Возврат изображений:** Возможность получать ссылки на обложки контента.

## Установка:
```
pip install rezka-scraper
```

## Пример использование:
```
import asyncio
from rezka_scraper import RezkaScraper

async def main():
    scraper = RezkaScraper()

    try:
        # Поиск по названию параметр images=True передан в метод search_rezka, он дополнительно вернет ссылку на обложку контента. Если обложка не нужна установите images=False.
        title, link, image_url = await scraper.search_rezka("Лицо со шрамом", images=True)
        if title:
            print(f"Найдено: {title} - {link}\nОбложка: {image_url}\n")
        else:
            print("Ничего не найдено по запросу.\n")
    except Exception as e:
        print(f"Ошибка при поиске по названию: {e}\n")

    try:
        # Поиск аниме с пагинацией (по умолчанию первая страница)
        anime_results = await scraper.search_anime(page=1)
        print("Аниме на первой странице:")
        for title, link in anime_results:
            print(f"{title} - {link}\n")
    except Exception as e:
        print(f"Ошибка при поиске аниме: {e}\n")

    try:
        # Поиск фильмов с пагинацией (по умолчанию первая страница)
        movies_results = await scraper.search_movies(page=1)
        print("Фильмы на первой странице:")
        for title, link in movies_results:
            print(f"{title} - {link}\n")
    except Exception as e:
        print(f"Ошибка при поиске фильмов: {e}\n")

    try:
        # Поиск сериалов с пагинацией (по умолчанию первая страница)
        series_results = await scraper.search_series(page=1)
        print("Сериалы на первой странице:")
        for title, link in series_results:
            print(f"{title} - {link}\n")
    except Exception as e:
        print(f"Ошибка при поиске сериалов: {e}\n")

    try:
        # Поиск мультфильмов с пагинацией (по умолчанию первая страница)
        cartoons_results = await scraper.search_cartoons(page=1)
        print("Мультфильмы на первой странице:")
        for title, link in cartoons_results:
            print(f"{title} - {link}\n")
    except Exception as e:
        print(f"Ошибка при поиске мультфильмов: {e}\n")

asyncio.run(main())
```

## Методы:

| Метод              | Описание                                              |
|---------------------|------------------------------------------------------|
| `search_rezka`     | Поиск контента по названию.                           |
| `search_anime`     | Поиск аниме с пагинацией (по умолчанию первая страница). |
| `search_movies`    | Поиск фильмов с пагинацией (по умолчанию первая страница). |
| `search_series`    | Поиск сериалов с пагинацией (по умолчанию первая страница). |
| `search_cartoons`  | Поиск мультфильмов с пагинацией (по умолчанию первая страница). |

## Примечания:
1. **Асинхронный подход:** Для работы требуется поддержка асинхронного выполнения (asyncio).
2. **Зависимости:** Библиотека использует [aiohttp](https://pypi.org/project/aiohttp/) для HTTP-запросов и [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) для парсинга HTML и [fake-useragent](https://pypi.org/project/fake-useragent/) для создания ненастоящего User-Agent.
3. **Стабильное подключение:** Для успешной работы требуется стабильный доступ к интернету.
4. **Возможные ограничения:** Сайт [Rezka.ag](https://Rezka.ag) может быть недоступен в некоторых регионах. В этом случае вам может понадобиться использование VPN.

## Как связаться со мной:
[![Telegram Badge](https://img.shields.io/badge/Contact-blue?style=flat&logo=telegram&logoColor=white)](https://t.me/OFFpolice2077) [![Twitter Badge](https://img.shields.io/twitter/follow/:OFFpolice2077)](https://x.com/OFFpolice2077) [![Instagram Badge](https://img.shields.io/badge/-Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/offpolice2077)

## Лицензия:
Этот проект лицензируется по лицензии «MIT License» - более подробную информацию смотрите в файле [LICENSE](LICENSE).