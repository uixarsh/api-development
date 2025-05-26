from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def get_pwd_hash(password : str):
    return pwd_context.hash(password)