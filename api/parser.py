from rest_framework.parsers import BaseParser

class PlainTextParser(BaseParser):
    """
    Custom parser that converts raw text/plain body into a dictionary
    so it works with existing DRF serializers.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        data = stream.read().decode('utf-8')
        return {'text': data}
