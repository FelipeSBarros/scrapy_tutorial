from schematics.models import Model
from schematics.types import StringType, ListType, DateType


class QuoteItem(Model):
    quote_content = StringType(required=True)
    tags = ListType(StringType)
    author_name = StringType(required=True)
    author_birthday = DateType(required=True)
    author_bornlocation = StringType(required=True)
    author_bio = StringType(required=True)
