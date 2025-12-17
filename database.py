from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Имя сервера и БД — подставляем твой сервер
SERVER_NAME = r"WIN-8OSA8I3T0IE"
DATABASE_NAME = "AttendanceDB"  # можешь назвать как хочешь или существующую БД

SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    fast_executemany=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
