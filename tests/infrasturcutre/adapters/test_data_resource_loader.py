import pytest

from src.domain.value_objects.uri import URI
from src.infrastructure.adapters.data_resource_loader import DataResourceLoader

data_loader = DataResourceLoader()


@pytest.mark.parametrize(
    "input_text, data, error",
    [
        (
            "Привет, мир!",
            "data:text/plain;charset=utf-8,%D0%9F%D1%80%D0%B8%D0%B2%D0%B5%D1%82%2C%20%D0%BC%D0%B8%D1%80%21",
            None,
        ),
        (
            "Привет, мир!",
            "data:text/plain;charset=windows-1251,%CF%F0%E8%E2%E5%F2%2C%20%EC%E8%F0%21",
            None,
        ),
        ("Café", "data:text/plain;charset=iso-8859-1,Caf%E9", None),
        (
            "こんにちは",
            "data:text/plain;charset=shift_jis,%82%B1%82%F1%82%C9%82%BF%82%CD",
            None,
        ),
        ("test", "data:,test#foo", None),
        ("test £ pound sign", "data:,test%20%a3%20pound%20sign", UnicodeDecodeError),
    ],
)
def test_data_load_data(input_text: str, data: str, error: Exception):
    uri = URI.parse(data)
    response = data_loader.load(uri)

    if error is not None:
        with pytest.raises(error):
            response.body.decode(response.charset)
        return

    assert response.body.decode(response.charset) == input_text
