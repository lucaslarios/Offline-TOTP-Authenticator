import pytest

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.CryptControl import CryptControl

@pytest.fixture
def cryptoControl():
    return CryptControl()


def testgenerate_salt_not_null(cryptoControl):
    salt =cryptoControl.generate_salt()
    print(f"Salt gerado:{salt}")

    assert salt is not None

def testgenerate_salt_size(cryptoControl):
    salt = cryptoControl.generate_salt()
    print(f"Salt gerado:{salt}")
    assert len(salt) == 16

def testgenerate_salt_unique(cryptoControl):
    salt1 = cryptoControl.generate_salt()
    print(f"Salt gerado 1:{salt1}")
    salt2 = cryptoControl.generate_salt()
    print(f"Salt gerado 2:{salt2}")
    assert salt1 != salt2

@pytest.fixture
def passwd():
    return "euSouUmTesteNaoMtElaboradoFeitoComSono123$$"

def test_derive_key_same_password_and_salt(cryptoControl,passwd):
    salt = cryptoControl.generate_salt()
    key1 = cryptoControl.derive_key_from_passwd(passwd=passwd,salt=salt)
    key2 = cryptoControl.derive_key_from_passwd(passwd=passwd,salt=salt)
    assert key1 == key2, "key must be the same"

@pytest.fixture
def salt_forencrypt_anddecrypt(cryptoControl):
    return cryptoControl.generate_salt()

def testencrypt(cryptoControl,passwd,salt_forencrypt_anddecrypt):
    key = cryptoControl.derive_key_from_passwd(passwd=passwd,salt=salt_forencrypt_anddecrypt)
    plainText = "this is a test"
    crypto_text,iv= cryptoControl.encrypt(plainText,key)
    print(f"PlainText:{plainText}")
    print(f"cryptText:{crypto_text}")
    print(f"IV:{iv}")
    assert plainText != crypto_text,"plain text and crypt text most be different"

def test_padding(cryptoControl):
    a = "teste"
    b = cryptoControl._padding(a)
    print(f"Sem padding:{a}\nPadding:f{b}")
    assert a != b

def test_unpadding(cryptoControl):
    string_test = "arroz"
    padded_text = cryptoControl._padding(string_test)
    unpadded_text = cryptoControl._unpadding(padded_text)
    print(f"string:{string_test} e unpadded_string:{unpadded_text}")
    assert unpadded_text == string_test, "texto tem que ser igual" 


def test_descrypt(cryptoControl,salt_forencrypt_anddecrypt,passwd):
    key = cryptoControl.derive_key_from_passwd(passwd=passwd,salt=salt_forencrypt_anddecrypt)
    plainText = "this is a encryptdecrypt test"
    crypto_text,iv = cryptoControl.encrypt(plainText,key)
    print(f"PlainText:{plainText}")
    print(f"cryptText:{crypto_text}")
    decrypted_text = cryptoControl.decrypt(crypto_text,key,iv)
    print(f"DecryptText:{decrypted_text}")
    assert plainText == decrypted_text, "Textos tem que ser iguais"


def test_base64_data_authenticity(cryptoControl,salt_forencrypt_anddecrypt):
    binary_salt = salt_forencrypt_anddecrypt
    base64_str = cryptoControl.base64_encode(binary_salt)
    data_binary = cryptoControl.base64_decode(base64_str)
    print(f"base_64_str:{base64_str}")
    assert data_binary == binary_salt
    

def test_passwd_storage_verify_not_authorized(cryptoControl,salt_forencrypt_anddecrypt):
    
    passwd_storaged = cryptoControl.passwd_storage_creator(salt=salt_forencrypt_anddecrypt,passwd="1234")

    b = cryptoControl.passwd_storage_verify(salt=salt_forencrypt_anddecrypt,passwd="9955",password_storaged=passwd_storaged)
    assert b == 0

def test_passwd_storage_verify_authorized(cryptoControl,salt_forencrypt_anddecrypt):
    
    passwd_storaged = cryptoControl.passwd_storage_creator(salt=salt_forencrypt_anddecrypt,passwd="1234")

    b = cryptoControl.passwd_storage_verify(salt=salt_forencrypt_anddecrypt,passwd="1234",password_storaged=passwd_storaged)
    assert b == 1


 