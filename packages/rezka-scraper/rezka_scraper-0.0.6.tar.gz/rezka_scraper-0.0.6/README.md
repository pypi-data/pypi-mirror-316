# RezkaScraper

RezkaScraper — это мини библиотека на Python для асинхронного поиска контента (аниме, фильмов, сериалов и мультфильмов) на сайте [Rezka.ag](https://Rezka.ag).

## Возможности:
- Поиск по названию: Выполняет поиск по ключевому слову и возвращает первое совпадение.
- Поиск по категориям: Поддержка категорий аниме, фильмы, сериалы, мультфильмы с пагинацией.

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
        # Поиск по названию
        title, link = await scraper.search_rezka("Лицо со шрамом")
        if title:
            print(f"Найдено: {title} - {link}\n")
        else:
            print("Ничего не найдено по запросу.\n")
    except Exception as e:
        print(f"Ошибка при поиске по названию: {e}\n")

    try:
        # Поиск аниме с пагинацией
        anime_results = await scraper.search_anime(page=1)
        print("Аниме на первой странице:")
        for title, link in anime_results:
            print(f"{title} - {link}\n")
    except Exception as e:
        print(f"Ошибка при поиске аниме: {e}\n")

    try:
        # Поиск фильмов с пагинацией
        movies_results = await scraper.search_movies(page=1)
        print("Фильмы на первой странице:")
        for title, link in movies_results:
            print(f"{title} - {link}\n")
    except Exception as e:
        print(f"Ошибка при поиске фильмов: {e}\n")

    try:
        # Поиск сериалов с пагинацией
        series_results = await scraper.search_series(page=1)
        print("Сериалы на первой странице:")
        for title, link in series_results:
            print(f"{title} - {link}\n")
    except Exception as e:
        print(f"Ошибка при поиске сериалов: {e}\n")

    try:
        # Поиск мультфильмов с пагинацией
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
Для работы необходим стабильный интернет для выполнения запросов к сайту [Rezka.ag](https://Rezka.ag).

Библиотека использует aiohttp для асинхронных HTTP-запросов и BeautifulSoup для парсинга HTML-контента.

## Как связаться со мной:
[![Telegram Badge](https://img.shields.io/badge/Contact-blue?style=flat&logo=telegram&logoColor=white)](https://t.me/OFFpolice2077) [![Twitter Badge](https://img.shields.io/twitter/follow/:OFFpolice2077)](https://x.com/OFFpolice2077) [![Instagram Badge](https://img.shields.io/badge/-Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/offpolice2077)

## Лицензия:
Этот проект лицензируется по лицензии «MIT License» - более подробную информацию смотрите в файле [LICENSE](LICENSE).