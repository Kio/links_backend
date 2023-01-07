# Links

The application allows you to find all links on a specified URL, including nested links up to a depth of 3.

It consists of a [React frontend](https://github.com/Kio/links_frontend) and a [Django backend](https://github.com/Kio/links_backend).

## Crawling pages

The app uses Celery to create a background task for crawling. Async mechanisms such as aiohttp and pyppeteer are utilized to improve the performance of the crawling operations. The crawler first attempts to use aiohttp, but if the number of links on the page is zero, it assumes that the page is a SPA (Single Page Application) and uses pyppeteer instead. Pyppeteer utilizes Chromium and creates a separate page for each link.

## Storing results

In the app, all results are stored as an array of result links. Another approach that can be implemented is to store each URL separately and create a Many-To-Many relationship between them. Alternatively, a graph database could be used.

## Communication layers

The app uses GraphQL for communication between the frontend and backend. On the backend, graphene is implemented, and on the frontend, Apollo Client is used. Apollo Client also has a built-in cache, so it can be used as a state management system for all external data. For communication with Celery, the app uses RabbitMQ.