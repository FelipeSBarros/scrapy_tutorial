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
   1. [SQLAlchemy & scrapy Itempipeline](#SQLAlchemy-&-scrapy-Itempipeline)
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


## Sobre esse cadernos e os tutoriais estudados  

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
