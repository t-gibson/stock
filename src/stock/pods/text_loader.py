from jina.executors.crafters import BaseDocCrafter

from stock import download


class TextExtractor(BaseDocCrafter):
    """
    Given a [SEP]-separated row of '_,_,url,image-description',
    send the image description into the `text` protobuf field.
    """
    def craft(self, text: str, *args, **kwargs) -> dict:
        _, _, url, description = text.split(download.SEP)
        return dict(weight=1., text=description, meta_info=url.encode())
