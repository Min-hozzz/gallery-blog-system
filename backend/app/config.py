from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "52d6bfec29b5efde4b09bf122cf2c2b33e39970e5c4167148eaf85bbec04057c"  # 生产环境应从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
