import uuid
import hashlib

def check_password(password_db_string, password):
    _password_db_string = password_db_string.split("$")
    salt = _password_db_string[1]
    new_password = hash_password(password, salt)
    db_password = _password_db_string[-1]
    new_password = new_password.split("$")[-1]
    print(db_password)
    print(new_password)
    return (db_password != new_password)

def hash_password(password, salt=uuid.uuid4().hex):
    algorithm = 'sha512'
    
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string