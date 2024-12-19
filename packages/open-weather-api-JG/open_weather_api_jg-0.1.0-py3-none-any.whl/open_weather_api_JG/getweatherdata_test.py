from types import NoneType
import pytest
from getweatherdata import get_weather_data
from owm_key import owm_api_key


def test_without_key():
    assert get_weather_data("Moscow") is None, \
        " Для получения данных необходимо задать значение для api_key "


def test_in_riga():
    assert get_weather_data("Riga",
                            api_key=owm_api_key) is not None, \
        " Type of response is not none while using the key "


def test_type_of_res():
    assert type(get_weather_data("Riga",
                                 api_key=owm_api_key)) is str, \
        " Type of response is not none while using the key "


def test_args_error():
    assert get_weather_data('') is None, \
        " There should be one positional argument: 'place' and one keyword argument 'api_key'"


def test_pos_arg_error():
    assert get_weather_data('', api_key=owm_api_key) is None, \
        " There should be one positional argument: 'place' "


def test_temp_type():
    import json
    assert type(json.loads(get_weather_data('Riga', api_key=owm_api_key)).get(
        'feels_like')) is NoneType, \
        " Error with type of feels_like attribute "


inp_params_1 = "place, owm_api_key, expected_country"
exp_params_countries = [("Chicago", owm_api_key, 'US'),
                        ("Saint Petersburg", owm_api_key, 'RU'), ("Dakka", owm_api_key, 'BD')]


@pytest.mark.parametrize(inp_params_1, exp_params_countries)
def test_countries(place, owm_api_key, expected_country):
    import json
    assert json.loads(get_weather_data(place, api_key=owm_api_key)).get('country', 'NoValue') == expected_country, \
        " Error with country code "


if __name__ == "__main__":
    pass