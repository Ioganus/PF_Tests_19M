from app import PetFriends
from settings import valid_email, valid_password
import os
import string
import random

#  генератор букв в разном регистре с цифрами, param(k= длина строки)
ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=256))

#  генератор случайных чисел, param: range(кол-во чисел)
sequence = int(''.join(random.choice('0123456789') for _ in range(1000)))


pf = PetFriends()

def test_get_api_key_for_invalid_user(email: str = 'zharov@gmail.com', password: str = valid_password):
    """Тест с невалидным email и валидным password. Тест на наличие ключа в ответе"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует'


def test_get_api_key_for_invalid_password(email: str = valid_email, password: str = 'Qwertyuiop123'):
    """Тест с невалидным password и валидным email. Тест на наличие ключа в ответе"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует'


def test_update_self_pet_invalid_name_str(name: str = ran, animal_type: str = 'Cat', age: int = 5):
    """Негативный сценарий. Поле имя не должно принимать больше 255 символов"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert len(result['name']) <= 255, 'Длинна строки не должна превышать 255 символов'
    else:
        raise Exception("Питомцы отсутствуют")


def test_update_self_pet_invalid_name_int(name: int = 4, animal_type: str = 'Dog', age: int = 10):
    """Негативный сценарий. Поле имя не должно принимать цифры"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'].isalpha(), 'Введите корректное имя, имя не должно содержать цифры.'
    else:
        raise Exception("Питомцы отсутствуют")


def test_update_self_pet_invalid_animal_type(name: str = 'Какис', animal_type: str = ran, age: int = 5):
    """Негативный сценарий. Поле порода не должно принимать на ввод более 255 символов"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert len(result['animal_type']) <= 255, 'Допустимая длина строки 255 символов'
    else:
        raise Exception("Питомцы отсутствуют")


def test_update_self_pet_invalid_age(name: str = 'Бегемот', animal_type: str = 'Ацелот', age: int = 100):
    """Негативный сценарий. Поле возраст не должно принимать более двух цифр в возрасте питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert len(result['age']) < 3, 'Возраст животного не должен быть трехзначным'
    else:
        raise Exception("Питомцы отсутствуют")


def test_update_self_pet_photo_jpeg(pet_photo: str = 'images/001.jpg'):
    """Обновление фотографии в карточке питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception("Питомцы отсутствуют")


def test_update_self_pet_photo_png(pet_photo: str = 'images/003.png'):
    """Обновление фото питомца в формате png"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200, 'Формат png не доступен для загрузки'
    else:
        raise Exception("Питомцы отсутствуют")


def test_update_self_pet_invalid_animal_type_int(name: str = 'Джонатан', animal_type: int = 5, age: int = 5):
    """Негативный сценарий. Поле порода не должно принимать цифры"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['animal_type'].isalpha(), 'Поле порода не должно содержвть цифры'
    else:
        raise Exception("Питомцы отсутствуют")


def test_update_self_pet_empty_data(name: any = '', animal_type: any = '', age: any = ''):
    """Негативный сценарий. Созадание карточки питомца без данных"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] != '', 'Поле имя не должно быть пустым'
    assert result['animal_type'] != '', 'Поле порода не должно быть пустым'
    assert result['age'] != '', 'Поле возраст не должно быть пустым'