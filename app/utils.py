from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify_password(received_password,real_password):
    return pwd_context.verify(received_password,real_password)
    