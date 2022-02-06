## Scrapy tutorial

Tutorial do scrapy desponível na [documentação do mesmo](https://docs.scrapy.org/en/latest/intro/tutorial.html);  
Esse projeto foi expandido com o tutorial ["a minimalist end to end scrapy tutorial" disponível na *towardsdatascience*](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0), que inclui validação de dados e uso de SQLAlchemy.
Por isso, alguns spiders deixarão de fazer sentido, por terem sido consolidados em apenas, como por exemplo `quotes_spider_author.py`.  

* [`spidermon`](https://spidermon.readthedocs.io/en/latest/) tutorial para monitoramento dos scraps;  

## About Scrapy  

> BeautifulSoup is a library for parsing HTML and XML and Scrapy is a web scraping framework. [...]   
> **In short, you should learn Scrapy if you want to do serious and systematic web scraping.**
> *[a minimalist end to end scrapy tutorial](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0)*

Scrapy é asíncrono e está baseado em [`twisted`](https://twistedmatrix.com/trac/):
> Twisted is an event-driven networking engine written in Python

