from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    company = Column(String(255), nullable=True)
    link = Column(Text)

DATABASES = {
    'mysql': 'mysql+pymysql://user:password@localhost/dbname',
    'postgresql': 'postgresql+psycopg2://user:password@localhost/dbname',
    'mongodb': 'mongodb://localhost:27017/'
}

def get_engine(db_type: str):
    if db_type in ['mysql', 'postgresql']:
        return create_engine(DATABASES[db_type])
    elif db_type == 'mongodb':
        return MongoClient(DATABASES[db_type])
    else:
        raise ValueError("Unsupported database type")

def create_tables(engine):
    if hasattr(engine, 'table_names'):
        Base.metadata.create_all(engine)

def save_to_mysql_postgresql(engine, vacancies: list):
    Session = sessionmaker(bind=engine)
    session = Session()
    for vacancy in vacancies:
        new_vacancy = Vacancy(
            title=vacancy['title'],
            company=vacancy.get('company'),
            link=vacancy['link']
        )
        session.add(new_vacancy)
    session.commit()
    session.close()

def save_to_mongodb(engine, db_name: str, collection_name: str, vacancies: list):
    db = engine[db_name]
    collection = db[collection_name]
    collection.insert_many(vacancies)