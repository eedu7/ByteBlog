```py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
from pydantic import BaseModel
import jwt
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/mydatabase"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(
        User.__table__.select().where(User.email == user.email)
    )
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(User.__table__.select().where(User.email == user.email))
    db_user = result.scalar()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.email}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# TEST CASES
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_TEST_URL = "postgresql+asyncpg://user:password@localhost/testdb"
test_engine = create_async_engine(DATABASE_TEST_URL, echo=True)
TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield TestSessionLocal()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register(client, test_db):
    response = await client.post("/register", json={"email": "test@example.com", "password": "test123"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

@pytest.mark.asyncio
async def test_login(client, test_db):
    await client.post("/register", json={"email": "test@example.com", "password": "test123"})
    response = await client.post("/login", json={"email": "test@example.com", "password": "test123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
```