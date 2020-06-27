import hypothesis.strategies as st

from hypothesis import given
from hypothesis.provisional import urls

from stock import download


@st.composite
def photo(draw):
    photographer = draw(st.text())
    main_url = draw(urls())
    image_url = draw(urls())

    return {
        "photographer": photographer,
        "url": main_url,
        "src": {download.PHOTO_SIZE: image_url}
    }


@given(urls())
def test_decode_inverts_encode(url):
    assert download.decode_url(download.encode_url(url)) == url


@given(photo())
def test_decode_photo_object_inverts_encode(photo_obj):
    assert download.decode_photo_object(download.encode_photo_object(photo_obj)) == photo_obj
