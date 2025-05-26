from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def get_pwd_hash(password : str):
    return pwd_context.hash(password)

def verify_pwd (enterd_pwd, hashed_pwd):
    return pwd_context.verify(enterd_pwd, hashed_pwd)