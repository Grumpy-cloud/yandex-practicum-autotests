import pytest
from src import sender_stand_request, data


def get_auth_token():
    res = sender_stand_request.create_new_user(data.user_body)
    return res.json()['authToken']


def get_headers_with_token():
    token = get_auth_token()
    headers = data.headers.copy()
    headers['Authorization'] = 'Bearer ' + token
    return headers


def get_kit_body(name):
    current_body = data.kit_creation_body.copy()
    current_body['name'] = name
    return current_body


def positive_assert(name):
    body = get_kit_body(name)
    headers = get_headers_with_token()
    res = sender_stand_request.create_new_kit(body, headers)

    assert res.status_code == 201
    assert res.json()['name'] == name


def negative_assert_wrong_name(name):
    body = get_kit_body(name)
    headers = get_headers_with_token()
    res = sender_stand_request.create_new_kit(body, headers)

    assert res.status_code == 400


def negative_assert_empty_body():
    body = {}
    headers = get_headers_with_token()
    res = sender_stand_request.create_new_kit(body, headers)

    assert res.status_code == 400


# Проверка №1
def test_kit_creation_1_letter_in_name():
    positive_assert('а')


# Проверка №2
def test_kit_creation_511_letters_in_name():
    positive_assert(data.max_allowed_length_name)


# Проверка №3
def test_kit_creation_0_letters_in_name():
    negative_assert_wrong_name('')


# Проверка №4
def test_kit_creation_512_letters_in_name():
    negative_assert_wrong_name(data.prohibited_length_name)


# Проверка №5
def test_kit_creation_english_letters_in_name():
    positive_assert('QWErty')


# Проверка №6
def test_kit_creation_russian_letters_in_name():
    positive_assert('Мария')


# Проверка №7
def test_kit_creation_special_symbols_in_name():
    positive_assert('"№%@",')


# Проверка №8
def test_kit_creation_spaces_in_name():
    positive_assert('Человек и КО')


# Проверка №9
def test_kit_creation_digits_in_name():
    positive_assert('123')


# Проверка №10
def test_kit_creation_empty_body():
    negative_assert_empty_body()


# Проверка №11
def test_kit_creation_non_string_value_in_name():
    negative_assert_wrong_name(123)
