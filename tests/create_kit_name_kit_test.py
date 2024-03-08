import pytest
from src import sender_stand_request, data


@pytest.fixture(scope='function')
def auth_token():
    res = sender_stand_request.create_new_user(data.user_body)
    return res.json()['authToken']


@pytest.fixture(scope='function')
def auth_headers(auth_token):
    headers = data.headers.copy()
    headers['Authorization'] = 'Bearer ' + auth_token
    return headers


def get_kit_body(name):
    current_body = data.kit_creation_body.copy()
    current_body['name'] = name
    return current_body


def positive_assert(name, headers):
    body = get_kit_body(name)
    res = sender_stand_request.create_new_kit(body, headers)

    assert res.status_code == 201
    assert res.json()['name'] == name


def negative_assert_wrong_name(name, headers):
    body = get_kit_body(name)
    res = sender_stand_request.create_new_kit(body, headers)

    assert res.status_code == 400


def negative_assert_empty_body(headers):
    body = {}
    res = sender_stand_request.create_new_kit(body, headers)

    assert res.status_code == 400


# Проверка №1
def test_kit_creation_1_letter_in_name(auth_headers):
    positive_assert('а', auth_headers)


# Проверка №2
def test_kit_creation_511_letters_in_name(auth_headers):
    positive_assert(data.max_allowed_length_name, auth_headers)


# Проверка №3
def test_kit_creation_0_letters_in_name(auth_headers):
    negative_assert_wrong_name('', auth_headers)


# Проверка №4
def test_kit_creation_512_letters_in_name(auth_headers):
    negative_assert_wrong_name(data.prohibited_length_name, auth_headers)


# Проверка №5
def test_kit_creation_english_letters_in_name(auth_headers):
    positive_assert('QWErty', auth_headers)


# Проверка №6
def test_kit_creation_russian_letters_in_name(auth_headers):
    positive_assert('Мария', auth_headers)


# Проверка №7
def test_kit_creation_special_symbols_in_name(auth_headers):
    positive_assert('"№%@",', auth_headers)


# Проверка №8
def test_kit_creation_spaces_in_name(auth_headers):
    positive_assert('Человек и КО', auth_headers)


# Проверка №9
def test_kit_creation_digits_in_name(auth_headers):
    positive_assert('123', auth_headers)


# Проверка №10
def test_kit_creation_empty_body(auth_headers):
    negative_assert_empty_body(auth_headers)


# Проверка №11
def test_kit_creation_non_string_value_in_name(auth_headers):
    negative_assert_wrong_name(123, auth_headers)
