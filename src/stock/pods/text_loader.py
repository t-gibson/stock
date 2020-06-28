from jina.executors.crafters import BaseDocCrafter

from stock import download


class TextExtractor(BaseDocCrafter):
    """
    Given a [SEP]-separated row of '_,_,url,image-description',
    send the image description into the `text` protobuf field.
    """
    def craft(self, text: str, *args, **kwargs) -> dict:
        self.logger.debug(f"Attempting to unpack {text}")
        try:
            _, _, url, description = text.split(download.SEP)
            return dict(weight=1., text=description, meta_info=url.encode())
        except ValueError as e:
            self.logger.error(f"Failure in splitting text={text}")
            raise e
