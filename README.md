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

Os dados raspados pelo scrapy fundamentam-se no conceito de `itens`. Ou seja, os dados são raspados e são instanciados em classe [`scrapy.item.Items`](https://docs.scrapy.org/en/latest/topics/items.html): um objeto python que define pares de chave-valor. Logo, scrapy suporta e possui várias classes de items [1](https://docs.scrapy.org/en/latest/topics/items.html#item-types) [2](https://docs.scrapy.org/en/latest/topics/items.html#supporting-item-types);  
> In other words, Field objects are plain-old Python dicts.  

Esses dados, agora instância de `Items` são submetidos ao *Item Pipeline* para processamentos futuros. Considere ler os pontos chave que justificam o uso do `Items`, no tutorial da [towards data science](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-ii-b917509b73f7).  
Fluxo de processmento do scrapy:  
![](https://docs.scrapy.org/en/latest/_images/scrapy_architecture_02.png)  

**Ao usar classes Items e uma base de dados relacional para armazenar os dados raspados é possível que se pergunto se deve-se consolidar todos os dados em apenas uma classeItem ou em várias. Sim, é possível, mas não recomendado, já que os dados serão raspados assíncronamente e isso demandará a incorporação de uma lógica para associar os dados, ao passo que, em apenas uma classItem, isso é resolvido pelo scrapy.**

Além disso, pode-se usar o [`ItemLoader`](https://docs.scrapy.org/en/latest/topics/loaders.html), que é uma forma mais conveniente de incorporar os dados instanciando como Items, permitindo pré e pós-processamento dos mesmos (como limpeza, conversão, etc.) num código a parte. O `ItemLoader` o atribui os valores passados a uma lista, independente da quantidade de elementos. Quando tivermos um campo ao qual esperamos receber apenas um valor, podemos usar o `TakeFirst`.  

Neste caso, vamos adicionar, além de outras, uma função em `items.py` a ser aplicada usando o [`MapCompose`](https://docs.scrapy.org/en/2.4/_modules/itemloaders/processors.html), que é um [`loader.processors`](https://docs.scrapy.org/en/latest/topics/loaders.html#input-and-output-processors) removendo as áspas unicode que vem da citação.  

Como após o parse inicial de "quotes", queremos que os dados sejam persistidos ao `parse_author`, podemos passá-los como parâmetro `meta` do [`scrapy.Request.follow`](https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=follow#scrapy.http.Request).  

Cada item retornado do scrapy é enviado apra um[`Item Pipeline`](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) para processamentos adicionais como salvar os dados numa base de dados, validação, remoção de duplicatas, etc. Os mesmos são classes definidas em `pipelines.py` e é necessário habilitar os pipelines no `settings.py`. Cada pipeline habilitda tem um vaor inteiro associado, variando de 0 a 1000, que indica a ordem de execussão: Valores mais baixos são executados primeiro.  

Vamos usar o `ORM SQLAlchemy`](https://www.sqlalchemy.org/) para salvar os dados num SQLite e, por isso, precisaremos criar um arquivo chamado `models.py`, dentro da pasta spider.  

