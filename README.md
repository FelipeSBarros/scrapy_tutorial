## Scrapy tutorial

Tutorial do scrapy desponível na [documentação do mesmo](https://docs.scrapy.org/en/latest/intro/tutorial.html);  
Esse projeto foi expandido com o tutorial ["a minimalist end to end scrapy tutorial" disponível na *towardsdatascience*](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0), que inclui validação de dados e uso de SQLAlchemy.
Por isso, alguns spiders deixarão de fazer sentido, por terem sido consolidados em apenas, como por exemplo `quotes_spider_author.py`.  
Com relação ao processo de "gestão do log" da ferramenta, [ segui este tutorial](https://www.tutorialspoint.com/scrapy/scrapy_logging.htm) e [o tutorial original do móduloe `logging`](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) do python;  
Também usei como consulta o artigo [demystifying scrapy item loaders](https://towardsdatascience.com/demystifying-scrapy-item-loaders-ffbc119d592a);  

* [`spidermon`](https://spidermon.readthedocs.io/en/latest/) tutorial para monitoramento dos scraps;  
* [`Sobre seletores css`](https://www.w3schools.com/cssref/css_selectors.asp)
* [5 Useful Tips While Working With Python Scrapy](https://jerrynsh.com/5-useful-tips-while-working-with-python-scrapy/)  
* [How to crawl the web politely with Scrapy](https://www.zyte.com/blog/how-to-crawl-the-web-politely-with-scrapy/)  
* [Reaproveitando ItemLoaders](https://www.geeksforgeeks.org/scrapy-item-loaders/)  
* [Scrapy e SQLAlchemy](https://www.andrewvillazon.com/move-data-to-db-with-sqlalchemy/)  
* [How to crawl the web politely](https://www.zyte.com/blog/how-to-crawl-the-web-politely-with-scrapy/)  

## Sobre Scrapy  

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

**Ao usar classes Items e uma base de dados relacional para armazenar os dados raspados é possível que se pergunte se deve-se consolidar todos os dados em apenas uma classeItem ou em várias. Sim, é possível, mas não recomendado, já que os dados serão raspados assíncronamente e isso demandará a incorporação de uma lógica para associar os dados, ao passo que, em apenas uma classItem, isso é resolvido pelo scrapy.**

Além disso, pode-se usar o [`ItemLoader`](https://docs.scrapy.org/en/latest/topics/loaders.html), que é uma forma mais conveniente de incorporar os dados instanciando como Items, permitindo pré e pós-processamento dos mesmos (como limpeza, conversão, etc.) num código a parte. O `ItemLoader` o atribui os valores passados a uma lista, independente da quantidade de elementos. Quando tivermos um campo ao qual esperamos receber apenas um valor, podemos usar o `TakeFirst`.  

Neste caso, vamos adicionar, além de outras, uma função em `items.py` a ser aplicada usando o [`MapCompose`](https://docs.scrapy.org/en/2.4/_modules/itemloaders/processors.html), que é um [`loader.processors`](https://docs.scrapy.org/en/latest/topics/loaders.html#input-and-output-processors) removendo as áspas unicode que vem da citação.  

Como após o parse inicial de "quotes", queremos que os dados sejam persistidos ao `parse_author`, podemos passá-los como parâmetro `meta` do [`scrapy.Request.follow`](https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=follow#scrapy.http.Request).  

Cada item retornado do scrapy é enviado apra um[`Item Pipeline`](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) para processamentos adicionais como salvar os dados numa base de dados, validação, remoção de duplicatas, etc. Os mesmos são classes definidas em `pipelines.py` e é necessário habilitar os pipelines no `settings.py`. Cada pipeline habilitda tem um vaor inteiro associado, variando de 0 a 1000, que indica a ordem de execussão: Valores mais baixos são executados primeiro.  

Vamos usar o [`ORM SQLAlchemy`](https://www.sqlalchemy.org/) para salvar os dados num SQLite e, por isso, precisaremos criar um arquivo chamado `models.py`, dentro da pasta spider. Nele vamos definir uma classe para conexão ao banco `db_connect()`, que será definido no `settings.py` do projeto ( `get_project_settings().get("CONNECTION_STRING")`). O método `create_table()` criará as tabelas, na primeira execussão. A definição das tabelas seguem no mesmo arquivo. Apenas a tabela auxiliar (M-to-M) não é um método.  

Em `ItemPipeline`, recebemos todos os itens raspados, então será nele onde definiremos a qual tablela/campo cada um será salva, bem como lógicas para evitar registros duplicados. É preciso, ainda, habilitá-los no `settings.py`.  

```
ITEM_PIPELINES = {
   # 'scrapy_tutorial.pipelines.ScrapyTutorialPipeline': 300,
   'scrapy_tutorial.pipelines.SaveQuotesPipeline': 200,
   'scrapy_tutorial.pipelines.DuplicatesPipeline': 100,
}
```  

### Algumas configurações  

[**`autothrottle`**](https://doc.scrapy.org/en/latest/topics/autothrottle.html#autothrottle-extension):  
Por padrão a velocidade de espera para download do `scrapy` é de 0 que, quando somado ao fato de o `scrapy` submeter várias requisições simultaneamente, podem fazer com que alguns servidores sejam sobre carregados. Cada uma dessas configurações podem ser definidas. Contudo, cada site pode ter uma resposta diferente e ao definir valores mais elevados, pode-se estar perdendo a chance de otimizar o processo de raspagem. Essa extensão serve para ajustar automaticamente e dinâmicamente o *delay* do processo de crawling beseando-se na velocidade de carga de ambos: o servidor onde se encontra o raspador e *website* sendo raspado.  

> The main idea is the following: if a server needs latency seconds to respond, a client should send a request each latency/N seconds to have N requests processed in parallel.

O interessante é que erros como 404 podem ser retornados mais rápidos que respostas regulares, fazendo com que com valore sreduzidos de *download delay* e de *concurrency limit* o raspador irá enviar requisições mais rápidos quandoo servidor retornar erros. O que é, contudo, o oposto do que um raspador deveria fazer: em caso de erros, aumentar o *delay* pois os mesmos podem estar sendo criados pela alta carga de requisições.  

Em resumo, a extensão `AutoThrottle` ajusta o *delay* de download baseando-se nas seguintes regras: 
* Os `spiders` sempre iniciam com um *delay* definido pela configuração `AUTOTHROTTLE_START_DELAY` (default = 5);
* Quando a resposta é recebida, o *download delay* é calculado como `latencia / N`, onde `latencia` é a latencia da resposta e `N` é definido por `AUTOTHROTTLE_TARGET_CONCURRENCY` (default = 1.0).
* O *download delay* para as próximas requisições são, estão configuradas considerando a média dos *download delay* anteriores;
* :warning: A latencia de respostas com erros "non-200" não são autorizadas a aumentar o *delay*; 
* O *download delay* não pode ser menor que o definido em `DOWNLOAD_DELAY` ou maior que `AUTOTHROTTLE_MAX_DELAY`;  


#### Logging  
*Logging* é uma forma de acompanhar os eventos que ocorrem enquanto um software é executado. As chamadas de log são adicionadas sempre que eventos específicos occorrem e são acompanhados por uma mensagem descritiva, podendo conter um dado a partir de uma variável. A importância dos eventos podem ser chamados por `level` ou `severity`.  
* print(): Usado para apresentar no console a saida de um script ou programa;  
* `logg.info()`: Informa eventos que ocorrem em uma opração normal (e.g. for status monitoring or fault investigation); Também pode ser usado `logging.debug()` para um detlhamento maior da saida, caso seja necessário diagnóstico detalhado;  
* `warnings.warn()`: Apresenta um aviso **warning** de um evento em específico; Usado caso o aviso seja ignorável e a aplicação deva ser modificada para eliminar o warning;  
* `logging.warning()` Caso não haja nada que a aplicação cliente possa fazer para mudar dita situação, ainda que o evento deva ser notado e notificado;  
* Raise an exception: Para reportar um erro relacionado a um evento particular no runtime;  
* `logging.error()`, `logging.exception()` ou `logging.critical()`:
Reportam error **sem** levantar uma exception;  
	
Ao usar o módulo `logging` do python, podemos adicionar o registro de log da nossa execussão que serão registradas junto aos ogs de outros módulos que estejamos usando.  
O nível padrão de registro de logging é o `warning`. Ou seja, apenas os log identificados como `warning` ou de nível superior serão registrados/apresentados no console. Isso poder ser alterado na configuração de log. No caso do `logging`: `logging.basicConfig()`, ao qual poderá ser informado em `level`, qual o nível padrão de registro, `format` o formato a ser usado, inclusive se necessário informar data e hora, por exemplo...
O `scrapy` uso o `configure_logging` para definir as configurações de log em geral, mas as configurações específicas seguem sendo definidas pelo `logging.basicConfig()`.

No caso do `Scrapy`, Loggers são então habilitados a apresentar mensagens enviadas por eles mesmos. Então é necessário usar "handlers" para apresentção dos mesmos e para redirecionamento das mensagens aos seus destinos como arquivos, emails, outras saódas padrão.

`scrapy.utils.log.configure_logging(settings = None, install_root_handler = True)`
`install_root_handler` definido como `True` para habilitar o processo de registro de log.

### Spidermon  

`spidermon` é um módulo criado para facilitar o processo de monitoramento e validação das raspasgens realizadas em um projeto. Segundo os desenovledores, os monitores são similares a *test case*, com um conjunto de method que serão executdos em um momento bem definido com a lógica do monitoramento.  

Instalação:  

```python
pip install "spidermon[monitoring,validation]"
```

Para desenvolvimento tanto de monitores, como de validação. Caso contrário pode-se escolher um em detrimento de outro.

**Habilitando `spidermon`**:  
Tendo um projeto `Scrapy`, basta adicionar ao `setting.py`
```python
SPIDERMON_ENABLED = True

EXTENSIONS = {
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}
```  


## Monitor  
Os monitores deverão ser agrupados em *monitor suites*, que definem uma lista de monitores a serem executados e as ações a serem realizadas antes e depois que a execução de todos os monitores.  

Podemos criar um monitor para checar que ao menos X items sejam retornados após a execução do `spider`.

Os monitores deverão estar em um arquivo [`monitors.py`](/scrapy_tutorial/monitors.py) que armazenará a definição e configuração dos monitores.  

Exemplo:  
```python
from spidermon import Monitor, monitors

@monitors.name('Item count')
class ItemCountMonitor(Monitor):

    @monitors.name('Minimum items extracted')
    def test_minimum_number_of_items_extracted(self):
        minimum_threshold = 100
        item_extracted = getattr(self.data.stats, 'item_scraped_count', 0)
        self.assertFalse(
            item_extracted < minimum_threshold,
            msg='Extracted less than {} items'.format(minimum_threshold)
        )
```

Após a definição dos monitores, é preciso incluir-los ao `MonitorSuite`, para que sejam executados:

```python
class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ItemCountMonitor,
    ]
```

:warning: Um `Monitor` herda do Python unittest.TestCase. Logo, pode-se usar todos os `assertions` existentes no Monitor.

> As spidermon.core.monitors.Monitor inherits from Python unittest.TestCase, you can use all existing assertion methods in your monitors.

É preciso informar no `settings.py`:  
```
SPIDERMON_SPIDER_CLOSE_MONITORS = (
    ''scrapy_tutorial.monitors.SpiderCloseMonitorSuite',',
)
```

#### Mais sobre `Monitor`
Uma instância Monitor define a lógica de monitoramento e tem as seguintes proporidades, que podem ser usadas:

- `data.stats` Objeto tipo dicionário contendo as estatísticas do `spider` executado.  
- `data.crawler` Instancia do `Crawler` usado.  
- `data.spider` Instancia do `spider` usado.  


#### Item validation  
O `Item validator` permite confirmar se os items retornados estão conforme com uma estrutura predeterminada, garantindo que todos os campos contenham dados no formato esperado.. Para isso, se pode usar [`schematics`](https://schematics.readthedocs.io/en/latest/) ou [`JSON Schema`](https://json-schema.org/).  

Para isso é necessário estar usando `Scrapy items`.

As validações deverão ser criadas em [`validators.py`](scrapy_tutorial/validators.py) e, em seguida, habilitadas no `settings.py`, tanto em como [`pipeline`](scrapy_tutorial/settings.py#L83) quanto em [`SPIDERMON_VALIDATION_MODELS`](scrapy_tutorial/settings.py#L72).  

Com isso, toa vez que o `spider` for executado um novo conjunto de estatística será apresentado no log, apresentando a informação sobre o resultado das validações.  

E a partir disso, pode-se criar um monitor específico para avisar sempre que a estatśitica indicar um padrão inadequado/erro de validação.  

Seria possível, tamém configurar o pipeline para incluir o erro de validação como um campo no item. Por padrão, será inserido `_validation` como uma nova chave ao item quando o mesmo não corresponder ao esquema, ao usar a constante `SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS` como `True` em `settings.py`.  

```python
SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS = True
```

Exemplo de resultado:  
```python
{
    '_validation': defaultdict(
        <class 'list'>, {'author_url': ['Invalid URL']}),
     'author': 'Mark Twain',
     'author_url': 'not_a_valid_url',
     'quote': 'Never tell the truth to people who are not worthy of it.',
     'tags': ['truth']
}
```  

### Sobre `MonitorSuite`  
O `MonitorSuite` agrupa um conjunto de classes `Monitor` e permite específicas quais ações deverão ser executadas em momentos específicos da execussão do `Spider`.  

Os mesmos deverão ser habilitados no [`settings`](https://spidermon.readthedocs.io/en/latest/monitors.html#monitor-suites) do projeto.

### Notificacoes  

`spidermon` tem algumas ferramentas para facilitar o processo de notificação resultante dos monitores. Tais notificações poderão ser enviadas para [slack](https://spidermon.readthedocs.io/en/latest/getting-started.html#slack-notifications) ou [telegram](https://spidermon.readthedocs.io/en/latest/getting-started.html#telegram-notifications).

