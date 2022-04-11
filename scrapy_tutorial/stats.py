import pytz
from scrapy.statscollectors import StatsCollector
from sqlalchemy.orm import sessionmaker

from scrapy_tutorial.models import db_connect, create_table, SpidersLog


class SpidersStats(StatsCollector):
    def __init__(self, _persist_stat):
        super().__init__(_persist_stat)
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def _persist_stats(self, stats, spider):
        stats["spider_name"] = spider.name
        stats["start_time"] = (
            pytz.timezone("UTC")
            .localize(stats.get("start_time"))
            .astimezone(pytz.timezone("Brazil/East"))
            .strftime("%Y-%m-%d %H:%M")
        )
        stats["finish_time"] = (
            pytz.timezone("UTC")
            .localize(stats.get("finish_time"))
            .astimezone(pytz.timezone("Brazil/East"))
            .strftime("%Y-%m-%d %H:%M")
        )

        log_agendas = SpidersLog()
        log_agendas.log = stats
        try:
            self.session.add(log_agendas)
            self.session.commit()

        except:
            self.session.rollback()
            raise

        finally:
            self.session.close()
