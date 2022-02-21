import logging


logging.warning("Essa é uma mensagem de warning")

logging.info("Loging INFO") # o og de info não é apresentado no console pq o nivel padrão de registro é warning ou maior. Info está com nivel menos e por isso não será apresentado.


# A ser executado em um ambiente novo
import logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
