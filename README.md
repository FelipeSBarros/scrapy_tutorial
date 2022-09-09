# Estudando Scrapy like a Pro  

Reposiótio criado inicialmente para seguir o tutorial da [documentação do scrapy](https://docs.scrapy.org/en/latest/intro/tutorial.html), mas que evoluiu para um estudo mais aprofundado envolvendo, além de [outros tutoriais sobre scrapy](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0), módulos importantes do python diretamente ou indiretamente relacionados ao processo de raspagem de dados.

Não considere este artigo/repositório como um **tutorial**, mas sim como um caderno de anotações a ser consultado no processo de desenvolvimento de um sistema de raspagem de dados. Se tiver interesse, a seguir listo os tutoriais que usei neste estudo. E como a ideia não foi ter um tutorial que consolide os demais, mas sim, um "caderno" de anotações, não vou apresentar o desenvolvimento de nenhuma solução de qualquer sorte, ainda que apresente alguns "retalhos de códigos" (*code snippet*);  

De qualquer forma, você é bem-vindo a usar os códigos do projeto para estudar, ainda que nem tudo exposto neste README/artigo tenha sido implementado neste projeto. Veja [como executar a raspagem deste projeto](#Como-executar-a-raspagem-deste-projeto).

ìndice:
1. [Sobre esse cadernos e os tutoriais estudados](#Sobre-esse-cadernos-e-os-tutoriais-estudados)
1. [Sobre Scrapy](#Sobre-Scrapy)
   1. [Scrapy Items & Workflow](#Scrapy-Items-e-workflow)
   1. [Item Pipeline](#Item-Pipeline)
1. [ORM SQLAlchemy](#ORM-SQLAlchemy)
   1. [SQLAlchemy & scrapy Itempipeline](#sqlalchemy--scrapy-itempipeline)
1. [Sobre algumas configurações do Scrapy](#Sobre-algumas-configurações-do-Scrapy) 
   1. [`autothrottle`](#autothrottle) 
1. [`Logging`](#Logging) 
1. [Scrapy Stats Collection](#Scrapy-Stats-Collection) 
1. [scrapy Errback](#scrapy-Errback) 
1. [Spidermon](#Spidermon) 
   1. [#Spidermon Monitor](#Spidermon-Monitor) 
   1. [Spidermon Item validation](#Spidermon-Item-validation) 
   1. [Spidermon notificações](#Spidermon-notificações) 
1. [Scrapy Faker user-agent](#Scrapy-Faker-user-agent) 
1. [Como executar a raspagem deste projeto](#Como-executar-a-raspagem-deste-projeto) 
1. [`Scrapy` e `selenium`: executar raspagem dinâmica](#Scrapy-e-selenium:-executar-raspagem-dinâmica) 
1. [`Scrapyd`](#scrapyd)  
1. [`Scrapyd-client`](#scrapyd-client)  


## Sobre esse caderno e os tutoriais estudados  

Após o tutorial do scrapy disponível na [documentação do mesmo](https://docs.scrapy.org/en/latest/intro/tutorial.html) (veja a seção [Sobre Scrapy](#Sobre-Scrapy) para conhecer essa *framework*), busquei mais conhecimentos sobre incorporação das raspagens a um banco de dados com SQLAlchemy, usando o tutorial ["a minimalist end to end scrapy tutorial" disponível na *towardsdatascience*](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0), já que a minha ideia era persistir os dados aproveitando o máximo do poder do python e sem sujar as minhas mãos de SQL :). Este último inclui validação de dados e uso de SQLAlchemy.  

:warning: Alguns spiders criados para um tutorial poderão deixar de fazer sentido. No presente projeto, todos os *spiders* estão consolidados em apenas um (`quotes_spider.py`).  

Com relação ao processo de "gestão do log" da ferramenta, [segui este tutorial](https://www.tutorialspoint.com/scrapy/scrapy_logging.htm) e [o tutorial original do módulo `logging`](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) do python. Nem pre3ciso dizer, né?! O [@dunosauro](https://twitter.com/dunossauro) tem uma [live só sobre logging](https://www.youtube.com/watch?v=PGAOqAWuwC0) que é muito boa.  

Não posso deixar de mencionar o artigo [demystifying scrapy item loaders](https://towardsdatascience.com/demystifying-scrapy-item-loaders-ffbc119d592a), um ótimo tutorial que mostra como validar e, de fato, desmistificar o [`ItemLoader`](https://docs.scrapy.org/en/latest/topics/loaders.html#module-scrapy.loader) do *scrapy*.  

Para um nível mais avançado, quando além de raspar os dados a garantia de qualidade dos processos passam ser fundamentais, é recomendável usar o [`spidermon`](https://spidermon.readthedocs.io/en/latest/) que possui um tutorial para monitoramento dos scraps. O mesmo foi usado para o estudo apresentado aqui.

Além do já mencionado, os seguintes *links* e tutoriais foram fonte importante de informações e conhecimentos:
* [`Sobre seletores css`](https://www.w3schools.com/cssref/css_selectors.asp)  
* [5 Useful Tips While Working With Python Scrapy](https://jerrynsh.com/5-useful-tips-while-working-with-python-scrapy/)  
* [How to crawl the web politely with Scrapy](https://www.zyte.com/blog/how-to-crawl-the-web-politely-with-scrapy/)  
* [Reaproveitando ItemLoaders](https://www.geeksforgeeks.org/scrapy-item-loaders/)  
* [Scrapy e SQLAlchemy](https://www.andrewvillazon.com/move-data-to-db-with-sqlalchemy/)  
* [scrapy scrapyd guide](https://scrapeops.io/python-scrapy-playbook/extensions/scrapy-scrapyd-guide/)  


## Sobre Scrapy  

**Scrapy e BeautifulSoup**
[*Beatiful Soup*](https://beautiful-soup-4.readthedocs.io/en/latest/) é um módulo python para analisar (`parse`) HTML e XML, já o Scrapy é um framework de raspagem de dados *web* (`scraping`). Em resumo, você deve aprender a usar o Scrapy se quiser fazer uma raspagem sistemática.  
> BeautifulSoup is a library for parsing HTML and XML and Scrapy is a web scraping framework. [...]   
> **In short, you should learn Scrapy if you want to do serious and systematic web scraping.**
> *[a minimalist end to end scrapy tutorial](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0)*

**Scrapy:** 
Scrapy é asíncrono e está baseado em [`twisted`](https://twistedmatrix.com/trac/):
> Twisted is an event-driven networking engine written in Python


### Scrapy *Items* e *workflow*:   

Os dados raspados pelo scrapy fundamentam-se no conceito de `itens`. Ou seja, os dados são raspados sendo instanciados em classe [`scrapy.item.Items`](https://docs.scrapy.org/en/latest/topics/items.html): um objeto python que define pares de chave-valor. Logo, scrapy suporta e possui várias classes de itens [1](https://docs.scrapy.org/en/latest/topics/items.html#item-types) [2](https://docs.scrapy.org/en/latest/topics/items.html#supporting-item-types);  
> In other words, Field objects are plain-old Python dicts.  

Esses dados, agora instância de `Items` são submetidos ao *Item Pipeline* para processamentos futuros. Considere ler os pontos-chave que justificam o uso do `Items`, no tutorial da [towards data science](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-ii-b917509b73f7).  

Fluxo de processmento do scrapy:  

![](https://docs.scrapy.org/en/latest/_images/scrapy_architecture_02.png)  

Ao usar classes Items e uma base de dados relacional é possível que se pergunte se deve-se consolidar todos os dados raspados em apenas uma classeItem ou em várias. **Sim, é possível, mas não é recomendado, já que os dados serão raspados assíncronamente** e isso demandará a incorporação de uma lógica para associar os dados na base, ao passo que, em apenas uma classItem, isso é resolvido pelo scrapy.  

Além disso, pode-se usar o [`ItemLoader`](https://docs.scrapy.org/en/latest/topics/loaders.html), que é a forma mais conveniente de incorporar os dados instanciando como Items, permitindo pré e pós-processamento dos mesmos (como limpeza, conversão, etc.) num código a parte. Há funções já criadas, mas o usuário pode criar os seus próprios *processors*:  

> The only condition is that the processor function’s first argument must be an iterable.  


### *ItemLoaders*  

O `ItemLoader` o atribui os valores passados a uma lista, independente da quantidade de elementos. Quando tivermos um campo ao qual esperamos receber apenas um valor, podemos usar o `TakeFirst`.  

Neste caso, vamos adicionar, além de outras, uma função em `items.py` a ser aplicada usando o [`MapCompose`](https://docs.scrapy.org/en/2.4/_modules/itemloaders/processors.html), que é um [`loader.processors`](https://docs.scrapy.org/en/latest/topics/loaders.html#input-and-output-processors) removendo as áspas unicode que vem da citação.  

Como após o parse inicial de "quotes", queremos que os dados sejam persistidos ao `parse_author`, podemos passá-los como parâmetro `meta` do [`scrapy.Request.follow`](https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=follow#scrapy.http.Request).  


### Item Pipeline  

Cada iten retornado do scrapy é enviado para um [`Item Pipeline`](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) para processamentos adicionais como salvar os dados numa base de dados, validação, remoção de duplicatas, etc. Os mesmos são classes definidas em `pipelines.py` e é necessário habilitar os *pipelines* no `settings.py`. Cada *pipeline* habilitada tem um valor inteiro associado, variando de 0 a 1000, que indica a ordem de execução. Valores mais baixos são executados primeiro.  

Em `ItemPipeline`, recebemos todos os itens raspados, então será nele onde definiremos a qual tablela/campo cada um será salva, bem como lógicas para evitar registros duplicados. É preciso, ainda, habilitá-los no `settings.py`.  

```
ITEM_PIPELINES = {
   # 'scrapy_tutorial.pipelines.ScrapyTutorialPipeline': 300,
   'scrapy_tutorial.pipelines.SaveQuotesPipeline': 200,
   'scrapy_tutorial.pipelines.DuplicatesPipeline': 100,
}
```  


## ORM SQLAlchemy  

Vamos usar o [`ORM SQLAlchemy`](https://www.sqlalchemy.org/) para salvar os dados num SQLite por isso, precisaremos criar um arquivo chamado `models.py`, dentro da pasta `spider`. Nele vamos definir uma classe para conexão ao banco `db_connect()`. Vamos usar alguns parâmetros definidos no `settings.py` do projeto, usando o `get_project_settings()`. Neste caso, nos interessa a constante `CONNECTION_STRING` (`get_project_settings().get("CONNECTION_STRING")`).  

O método `create_table()` criará as tabelas, na primeira execução. A definição das tabelas seguem no mesmo arquivo. Apenas a tabela auxiliar (M-to-M) não é um método.  

### SQLAlchemy & scrapy `Itempipeline`:  

Tendo criado o modelo das entidades a serem persistidas na base de dados, bem como as configurações mínimas necessárias para o mesmo, será no `Itempipeline` que acessaremos os dados raspados e já tratados pelo `ItemLoaders` (lembre-se que os mesmos, não como dicionário python) e os instanciaremos nas respectivas classes do ORM SQLAlchemy.  

Aproveitando que `Itempipeline` são classes, podemos adicionar ao método de inicialização da classe (`__init__`) os parâmetros de inicialização e criação da seção com o banco de dados. E, no método [`process_item`](https://docs.scrapy.org/en/latest/topics/item-pipeline.html#process_item) desenvolver a lógica de instanciação dos dados no modelo do banco. É interessante entender, também que, seguindo o fluxo de trabalho do scrapy, o *pipeline* será executado a cada iten raspado e após o seu processamento com [`Itemprocessors`](https://docs.scrapy.org/en/latest/topics/loaders.html#input-and-output-processors).  

Exemplo:

```
class SaveQuotesPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        quote = Quote()
        author = Author()
        tag = Tag()
        author.name = item["author_name"]
        author.bornlocation = item["author_bornlocation"][0] # aqui estava retornando uma lista e or isso dava erro
        author.bio = item["author_bio"]
        author.birthday = item["author_birthday"]
        quote.quote_content = item["quote_content"]
```


## Sobre algumas configurações do Scrapy  

### [**`autothrottle`**](https://doc.scrapy.org/en/latest/topics/autothrottle.html#autothrottle-extension):  

Por padrão a velocidade de espera para *download* do `scrapy` é de 0 que, quando somado ao fato de o `scrapy` submeter várias requisições simultaneamente, podem fazer com que alguns servidores sejam sobre carregados. Essa configuração, em conjunto com outras podem ser alteradas conforme a conveniência do projeto. Contudo, cada página *web* pode ter uma resposta diferente e, ao definir valores mais elevados de espera, pode-se estar perdendo a chance de otimizar o processo de raspagem. É aí que o `autothrottle` entra: essa extensão serve para ajustar automaticamente e dinâmicamente o *delay* do processo de raspagem beseando-se na velocidade de carga de ambos: o servidor onde se encontra o raspador e a págin *web* sendo raspada.  

> The main idea is the following: if a server needs latency seconds to respond, a client should send a request each latency/N seconds to have N requests processed in parallel.

O interessante é que erros de HTTP, como 404, podem ser retornados mais rápidos que respostas regulares, fazendo com que valores reduzidos de *download delay* e de *concurrency limit* do raspador envie requisições mais rápidos quando servidor retornar erros. Contudo, essa prática seria equivocada já que, em caso de erros, os mesmos podem estar sendo criados pela alta carga de requisições.  

Com a extensão `AutoThrottle` o ajuste do *delay* de *download* basea-se nas seguintes regras:  
* Os `spiders` sempre iniciam com um *delay* definido pela configuração `AUTOTHROTTLE_START_DELAY` (default = 5);  
* Quando a resposta é recebida, o *download delay* é calculado como `latencia / N`, onde `latencia` é a latencia da resposta e `N` é definido por `AUTOTHROTTLE_TARGET_CONCURRENCY` (default = 1.0);  
* O *download delay* para as próximas requisições são, então configuradas considerando a média dos *download delay* anteriores;  
* :warning: A latência de respostas com erros "non-200" não são autorizadas a aumentar o *delay*;  
* O *download delay* não pode ser menor que o definido em `DOWNLOAD_DELAY` ou maior que `AUTOTHROTTLE_MAX_DELAY`;  


## Logging  

*Logging* é uma forma de acompanhar os eventos que ocorrem enquanto um *software* é executado. As chamadas de log são adicionadas sempre que eventos específicos occorrem sendo acompanhados por uma mensagem descritiva, podendo conter um dado a partir de uma variável. A importância dos eventos podem ser chamados por `level` ou `severity`.  

Algumas formas de acompanhar eventos de um *softwares* (com ou sem `logging`):  
* print(): Usado para apresentar no console a saida de um *script* ou programa;  
* `logg.info()`: Informa eventos que ocorrem numa operação normal (e.g. estatus da execução ou uma investigação padrão);  
* Também pode ser usado `logging.debug()` para um detalhamento maior da saida, caso seja necessário;  
* `warnings.warn()`: Apresenta um aviso **warning** de um evento; **Usado caso o aviso seja ignorável** e a aplicação deva ser modificada para eliminar o warning;  
* `logging.warning()` Caso não haja nada que a aplicação cliente possa fazer para mudar dita situação, ainda que o evento deva ser notado e notificado;  
* Raise an exception: Para reportar um erro relacionado a um evento particular no runtime;  
* `logging.error()`, `logging.exception()` ou `logging.critical()`:
Reportam error **sem** levantar uma exception;  
	
Ao usar o módulo `logging` do python, podemos adicionar o registro de log da nossa execução que serão registradas junto aos logs de outros módulos que estejamos usando.  

O nível padrão de registro de logging é o `warning`. Ou seja, apenas os logs identificados como `warning` ou de nível superior serão registrados/apresentados no console. Isso poder ser alterado na configuração de log. No caso do `logging`: [`logging.basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig), ao qual poderá ser informado em `level`, qual o nível padrão de registro, `format` o formato a ser usado, inclusive se necessário informar data e hora, por exemplo...  

Algumas provas:  

```
logging.basicConfig(level=logging.INFO)
logger.info("Teste mensagem de info")
# INFO:root:Teste mensagem de info
```

Quando estamos executando um processamento com multiplas funções pode ser interessante usar múltiplos `loggers`. Para isso, podemos definir um [`logger`](https://docs.python.org/3/library/logging.html#logging.getLogger) para cada função, por exemplo, para que as mensagens sejam facilmente identificadas:  

```
import loggging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Teste")
logger.info("Teste mensagem de info")
# INFO:Teste:Teste mensagem de info
```

Essa definição de `logger` pode ser facilmente customizada para cad módulo com o `__name__`:  

```
logger = logging.getLogger(__name__)
logger.info("Teste mensagem de info")
INFO:__main__:Teste mensagem de info
```


### Logging & Scrapy

O `scrapy` usa o módulo `logging` na gestão dos logs. Logo, conhecendo o mulo `logging`, já temos o mínimo necessário para fazer as configurações e ajustes necessários.

Ainda que possamos usar o `logging.basicConfig()`para confirgurar os logs, o scrapy possui o [`configure_logging`](https://docs.scrapy.org/en/latest/topics/logging.html#scrapy.utils.log.configure_logging) para definir as configurações de log em geral.

> Another option when running custom scripts is to manually configure the logging. To do this you can use logging.basicConfig() to set a basic root handler.  

No caso do `Scrapy`, `Loggers` são habilitados para apresentar mensagens enviadas por eles mesmos. Então é necessário usar [`handlers`](https://docs.python.org/3/library/logging.handlers.html) para apresentação dos mesmos e para redirecionamento das mensagens aos seus destinos, como arquivos, endereços eletrónicos, outras saídas padrão.

`scrapy.utils.log.configure_logging(settings = None, install_root_handler = True)`
`install_root_handler` definido como `True` para habilitar o processo de registro de log.


## Scrapy Stats Collection

O [Stats Collection](https://docs.scrapy.org/en/latest/topics/stats.html) é outra forma do `scrapy` apresentar um resumo do que foi processado. O mesmo está baseado na estrutura de dicionário `chave/valor` e podem ser acessados pelo atributo [`stats`](https://docs.scrapy.org/en/latest/topics/api.html#scrapy.crawler.Crawler.stats) do [Crawller](https://docs.scrapy.org/en/latest/topics/api.html#topics-api-crawler).  

Este último é uma instância da classe [`StatsCollector`](https://docs.scrapy.org/en/latest/topics/api.html#scrapy.statscollectors.StatsCollector), podendo ser alterado conforme a necessidade do projeto.  

Num projeto pessoal tive a necessidade de persistir os resumos estatísticos das raspagens e, para isso, sobreescrevi o método `_persist_stats` da classe `StatsCollector`. Veja o [exemplo no arquivo `stats.py`](scrapy_tutorial/stats.py).  

Posteriormente, foi necessário informar essa classe criada no `settings.py` do projeto: `STATS_CLASS = "project_name.stats.SpidersStats"`


## scrapy Errback  

Como é comum termos muitas `URLs` para raspar, é importante saber além das estatísticas gerais do *spider*, **o que não poder ser raspado**. Parra isso o scrapy fornece nos possibilita criar uma função a ser usada quando o request retorna algum erro. Essa função deve ser informada no parâmtero `errback` da função de [Request](https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Request).  

> errback (collections.abc.Callable): a function that will be called if any exception was raised while processing the request. This includes pages that failed with 404 HTTP errors and such. It receives a Failure as first parameter. For more information, see [Using errbacks to catch exceptions in request processing](https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-errbacks) below.

Ao implementar um parse para `errback` me premitiu identificar as `URLs` e os erros encontrados no processo de request. Com isso, pudo criar um `ItemLoader` e `ItemPipeline` para persistir dita informação no banco de dados.


## Spidermon  

`spidermon` é um módulo criado para facilitar o processo de monitoramento e validação das raspasgens realizadas usando scrapy. Segundo os desenovledores, os monitores são similares a *test case*, com um conjunto de métodos que serão executados em um momento bem definido com a lógica do monitoramento.  

Instalação:  

```commandline
pip install "spidermon[monitoring,validation]"
```

Para desenvolvimento tanto de monitores, como de validação. Caso contrário pode-se escolher um em detrimento de outro.  

**Habilitando `spidermon`**:  

Tendo um projeto `Scrapy`, basta adicionar ao `setting.py`:  

```python
SPIDERMON_ENABLED = True

EXTENSIONS = {
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}
```


### Spidermon Monitor  

Os monitores deverão ser agrupados em *monitor suítes*, uma lista a ser executada com as ações a serem realizadas antes e/ou depois do *spider*.  

Podemos criar um monitor para checar que ao menos X itens sejam retornados após a execução do `spider`, usando dado presente nas estatísticas do `spider`.  

Os monitores deverão estar num arquivo [`monitors.py`](/scrapy_tutorial/monitors.py) que armazenará a definição e configuração dos monitores.  

No tutorial do [`Spidermon` há um exemplo ilustrativo](https://spidermon.readthedocs.io/en/latest/getting-started.html#our-first-monitor).  

Após a definição dos monitores, é preciso incluí-los ao `MonitorSuite`, para serem executados.  

:warning: Um `Monitor` herda do Python unittest.TestCase. Logo, pode-se usar todos os `assertions` existentes no Monitor.  

> As spidermon.core.monitors.Monitor inherits from Python unittest.TestCase, you can use all existing assertion methods in your monitors.  

É preciso informar no `settings.py`:  

```
SPIDERMON_SPIDER_CLOSE_MONITORS = (
    'scrapy_tutorial.monitors.SpiderCloseMonitorSuite',
)
```

**Mais sobre `Monitor`:**  

Uma instância Monitor define a lógica de monitoramento e tem as seguintes proporidades, que podem ser usadas:  

- `data.stats` Objeto tipo dicionário contendo as estatísticas do `spider` executado.  
- `data.crawler` Instancia do `Crawler` usado.  
- `data.spider` Instancia do `spider` usado.  

**Sobre `MonitorSuite`**:  

O `MonitorSuite` agrupa um conjunto de classes `Monitor` e permite específicar quais ações deverão ser executadas em momentos específicos da execução do `Spider`.  

Os mesmos deverão ser habilitados no [`settings`](https://spidermon.readthedocs.io/en/latest/monitors.html#monitor-suites) do projeto/spider.  

### Spidermon Item validation  

O `Item validator` permite confirmar se os itens retornados são de um tipo predeterminada, garantindo que todos os campos contenham dados no formato esperado. Para isso, se pode usar [`schematics`](https://schematics.readthedocs.io/en/latest/) ou [`JSON Schema`](https://json-schema.org/).  

:warning: É necessário estar usando [`Scrapy items`](#L26).  

As validações deverão ser criadas em [`validators.py`](scrapy_tutorial/validators.py) e, habilitadas no `settings.py`: tanto em [`pipeline`](scrapy_tutorial/settings.py#L83) como em [`SPIDERMON_VALIDATION_MODELS`](scrapy_tutorial/settings.py#L72).  

Toda a vez que o `spider` for executado um novo conjunto de estatística será apresentado no log com as informações sobre o resultado das validações:  
- `spidermon/validation/items`: Quantidade de **itens** validados na raspagem; 
- `spidermon/validation/fields`: Quantidade de **campos** validados na raspagem;  
- `spidermon/validation/validators`: Quantidade de validadores usados na raspagem em questão;  
- `spidermon/validation/fields/errors/`: Quantidade de campos que apresentaram erro de validação;  
- `spidermon/validation/items/errors`: Quantidade de itens raspados que apresentaram erro;  

E a partir disso, pode-se criar um monitor específico para avisar sempre que a estatística indicar um padrão inadequado/erro de validação.  

Seria possível, também configurar o *pipeline* para incluir o erro de validação como um campo no iten. Por padrão, será inserido `_validation` como uma nova chave ao iten quando o mesmo não corresponder ao esquema, ao usar a constante `SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS` como `True` em `settings.py`.  

```python
SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS = True
```

Exemplo de resultado:  
```
{
    '_validation': defaultdict(
        <class 'list'>, {'author_url': ['Invalid URL']}),
     'author': 'Mark Twain',
     'author_url': 'not_a_valid_url',
     'quote': 'Never tell the truth to people who are not worthy of it.',
     'tags': ['truth']
}
```  

### Spidermon notificações  

`spidermon` tem algumas ferramentas para facilitar o processo de notificação resultante dos monitores. Tais notificações poderão ser enviadas para [slack](https://spidermon.readthedocs.io/en/latest/getting-started.html#slack-notifications) ou [telegram](https://spidermon.readthedocs.io/en/latest/getting-started.html#telegram-notifications).

## Scrapy Faker user-agent

*User-agent* é uma *string* enviada a cada requisição HTTP que os navegadores usam para identificar a si mesmos na rede.  

No caso do `scrapy`, o mesmo está definido no `settings.py`, da seguinte forma:  

```python
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scraper (+http://www.yourdomain.com)'
```

Isso é importante, pois os servidores podem ser configurados para responder de acordo com um determinado *user agent*. Por exemplo, uma requisição de celular pode ser diracionado a um conteúdo específico.  

E nessa lógica, alguns servidores são configurados para bloquear o processo de *crawl* e *scrap*. Para evitar isso, deve-se mudar o *user agent* para cada request.  

E é aí que entra o [`scrapy-faker-useragent`](https://github.com/alecxe/scrapy-fake-useragent). Trata-se de um `middleware` baseado no `fake-useragent` que, entre outras possibilidades, seleciona um *user agent* (UA) de acordo com estatísticas sobre os UAs mais usados.  

Com o `scrapy-faker-useragent`, um novo UA é usado a cada *Request* e, caso haja falha no mesmo, a falha recebe outro UA aleatório.  

**Instalação**:  

```commandline
pip install scrapy-fake-useragent
```

O mesmo deve ser adcionado ao [`downloader middleware`](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#downloader-middleware) no `settings.py`, desabilitando os *pipelines* usados por padrão:  

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
}
```

Um ponto fundamental é definir os provedores de UA, informando de onde "pegar" novos UA. Pode-se informar mais de um *provider*, para caso um falhe. Os mesmos serão usandnos em ordem de apresentação:  

```python
FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',
    'scrapy_fake_useragent.providers.FakerProvider',
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',
]
```

É interessante infromar um `FAKEUSERAGENT_FALLBACK`, a ser usado caso haja algum erro na busca de UA aleatórios.  

```python
FAKEUSERAGENT_FALLBACK = 'Mozilla/5.0 (Android; Mobile; rv:40.0)'
```

## Como executar a raspagem deste projeto  

1. Faça o [fork](https://docs.github.com/es/enterprise-cloud@latest/get-started/quickstart/fork-a-repo) do repositório [original](https://github.com/FelipeSBarros/scrapy_tutorial);  
2. [Clone](https://git-scm.com/docs/git-clone) para seu computador;  
```commandline
git clone git@github.com:Your_User_HERE/scrapy_tutorial.git
cd scrapy_tutorial
```

3. Crie um ambiente virtual;

```commandline
python3 -m venv .venv
```

6. Instale os módulos necessários;  
```commandline
pip install -r requirements.txt
```

7. Raspe os dados;  
```commandline
srapy crawl quotes
```

## `Scrapy` e `selenium`: executar raspagem dinâmica

Em projeto de raspagem de dados, é comum encontrar páginas que antes de podermos raspar algo, tenhamos que logarnos, ou até navegar pela página para que os dados sejam carregados, o demanda uma outra estratgégia de raspagemd iferente da implementada até o momento. Para essas situações, uma alternativa é usar [`Selenium`](https://www.selenium.dev/) para simular as ações reais de um usuário, controlando o navegador para acessar os dados. Seguirei brevemente a quinta parte do [tutorial "a minimalist end to end scrapy tutorial"](https://harrywang.medium.com/a-minimalist-end-to-end-scrapy-tutorial-part-v-e7743ee9a8ef). A qual usará página https://dribbble.com/designers como fonte de dados.

Instalando `Selenium`:  

`pip install selenium`

Além do `Selenium`, teremos que ter um navegador instaldado. Neste tutorial usaremos o [Chrome](https://chromedriver.chromium.org/downloads). Assegure-se de estar usando a versão mais atualizada(Menu → Chrome → About Google Chrome).

O driver deverá ser salvo na raiz do projeto de raspagem.

O [`spider dribble](./scrapy_tutorial/spiders/dribble_spider.py) faz o seguinte:

Ao acessar a página, use `last_height = driver.execute_script(“return document.body.scrollHeight”)` para ter a altura atual da página;  
Em seguida, `driver.execute_script(“window.scrollTo(0, document.body.scrollHeight);”)` é usado para descer pela ágina e acessar o conteúdo atualizado da página;  
Pausa por 5 segundos e repete o procedimento anterior até o máximo de rolagens (10).

Há ainda, um trecho de código usado para acessar a caixa de texto e inserir uma localização;

```python
search_location = driver.find_element_by_css_selector('#location-selectized').send_keys('New York')
sleep(1)
search_button = driver.find_element_by_css_selector('input[type="submit"]')
search_button.click()
sleep(5)
```

Como eu tive alguns problemas com o webdriver, acabei adotando a solução proposta [aqui](https://stackoverflow.com/a/61412036), adicionando a [instalação do driver](./scrapy_tutorial/spiders/dribble_spider.py#l41) no processo de raspagem. A mesma é feita apenas uma vez.


## Scrapyd

[`Scrapyd`](https://scrapyd.readthedocs.io/en/stable/) é uma ferramenta para executar os `spiders` em produção em servidores remotos. Ele é usado, basicamente, para `deploy` e agendamento/acompanhamento dos spiders em execução (usando JSON API), podendo rodar diferentes processos em paralelo.

`Scrapyd` geralmente é executado no backgound `daemon` "escutando" as requisições de execução dos `spiders`, disparando o camando de execução: `scrapy crawl myspider`

Além disso, permite:
* Run Scrapy jobs.  
* Pause & Cancel Scrapy jobs.  
* Manage Scrapy project/spider versions.  
* Access Scrapy logs remotely.  

Com relação ao versionamento, uma convenção importante a ser usada é nomear as versões com números. O `scrapyd` usa o `distutils` algoritmo para diferenciar, por exemplo, a versão r10 (como maio que) r9.


**Instalação**

```
pip install scrapyd
# for deploy
pip install scrapyd-client 
```

**Execução**

`Scrapyd` possui uma interface web mínima para monitoramento dos processos em execução, logs e etc. O mesmo fica disponível em `http://localhost:6800/` após a execução do comando: `scrapyd`

Existem diferentes dashboards/admins disponíveis para o `scrapyd`: 
* [ScrapeOps](https://scrapeops.io/)  
* [ScrapydWeb](https://github.com/my8100/scrapydweb)  
* [SpiderKeeper](https://github.com/DormyMo/SpiderKeeper)  

Criando uma tarefa de raspagem:  
`curl http://localhost:6800/schedule.json -d project=default -d spider=quotes`

### API

Ver [documentação](https://scrapyd.readthedocs.io/en/stable/api.html) para mais especificações da API.  

E a [parte de configuração](https://scrapyd.readthedocs.io/en/stable/config.html).  

### Deploy com `scrpyd`

O processo de `deploy` envolve um processo de encapsulamento (*eggfying*) para que o mesmo seja enviado ao `Scrapyd server`. Pode-se fazer isso manualmente, mas a maneira mais fácil de fazê-lo seria usando a ferramenta `scrapyd-deploy` do [`scrapyd-client`](https://github.com/scrapy/scrapyd-client), que faz tudo por você.

## [Scrapyd-client](https://github.com/scrapy/scrapyd-client)

`Scrapyd-client` é um pacote que provê:

* [`scrapyd-deploy`](#Deploy) para realizar o *deploy* de um projeto a um Scrapyd server;  
* [`scrapyd-client`]() para interagir com o projeto, uma vez feito o deploy.

Uma vez instalado, abra o [`scrapyd.cfg`](./scrapyd.cfg) que fica localizado na mesma pasta do projet a ser colocado em produção. Neste arquivo, temos o `endpoint` ao qual o projeto deve ser usar em produção. Para habilitá-lo, devemos descomentar a variável `url`: `url = http://localhost:6800/`

Em caso de produção, deveria ser informado o endpoint ao qual o mesmo seria enviado.

Tendo feita essa configuração, basta executar a ferramenta de [deploy](#deploy):

```commandline
scrapyd-deploy default
#Packing version 1662750751
#Deploying to project "scrapy_tutorial" in http://localhost:6800/addversion.json
#Server response (200):
#{"node_name": "felipe-Inspiron-7560", "status": "ok", "project": "scrapy_tutorial", "version": "1662750751", "spiders": 3}
```

:warning: O servidor precisa estar rodando o `scrapyd`... Logo, não deixe de, antes de usar o `scrapyd-deploy`, executar `scrapyd`.

Tendo o código bem-sucedido, isso fará o encapsulamento (eggfying) do projeto e o deploy do mesmo ao servidor local. Logo, existirá uma pasta nova `eggs` com uma subpasta com o nome do projeto e interno a ela o `.egg` criado com a versão do mesmo.

O `scrapy-client` permite definirmos no `scrapy.cfg` diferentes `endpoints` de deploy, como "local" e "production":

```commandline
## scrapy.cfg

[settings]
default = demo.settings  

[deploy:local]
url = http://localhost:6800/
project = demo 

[deploy:production]
url = <MY_IP_ADDRESS>
project = demo 
```

Assim podemos criar o encapsulamento e deploy especificando o servidor desejado:
```commandline
## Deploy locally
scrapyd-deploy local

## Deploy to production
scrapyd-deploy production
```

#### Deploy
Como já mencionado antes, o processo de deploy envolve dois passos:  
* [*Eggifying*](http://peak.telecommunity.com/DevCenter/PythonEggs) (encapsulamento em um `*.egg`) do projeto. Para isso será necessário instalar o [`setuptools`](https://pypi.org/project/setuptools/).  
* Uploading do arquivo `*.egg` a um Scrapyd server através de um endpoint [addversion.json](https://scrapyd.readthedocs.io/en/latest/api.html#addversion-json).  

> Add a version to a project, creating the project if it doesn’t exist.
  
O processo de deploy automatiza ambos passos: construção de um `*.egg` e a publicação em um Scrapyd server.

### Controlando spiders pelo `Scrapyd`

Tendo feito o deploy, teremos três opções para controlar os `spiders`:  

* [Scrapyd JSON API](https://scrapyd.readthedocs.io/en/stable/api.html);  
* [Python-Scrapyd-API Library](https://github.com/djm/python-scrapyd-api);  
* [Scrapyd Dashboard (scrapeops)](https://scrapeops.io/python-scrapy-playbook/extensions/scrapy-scrapyd-guide/#integrating-scrapyd-with-scrapeops);  