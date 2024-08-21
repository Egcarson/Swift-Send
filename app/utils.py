from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# setting up password hashing function


def hash_password(password: str):
    return pwd_context.hash(password)

# ## password verification for login
def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)
