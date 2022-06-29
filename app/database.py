from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://pilar:USALPilar2022@137.184.200.34/te_pilar_grp_1"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://1aXm44v0kk:3F0jPfi5RA@remotemysql.com:3306/1aXm44v0kk"
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://usuario:1234@tecnologias_emergentes_db_1:3306/te_pilar_grp_1"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()