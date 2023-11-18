import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Sale, Book, Stock, Shop

SQLsystem = 'postgresql'
login = 'postgres'
password = '123456'
host = 'localhost'
port = 5432
db_name = "2"
DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open('tests_data.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

def searching_publisher_name():
    query_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    query_publisher_name = input('Введите имя (name) издателя: ')
    query_result = query_join.filter(Publisher.publisher_name == query_publisher_name)
    for result in query_result.all():
        print(f'Издатель "{query_publisher_name}" найден в магазине "{result.name}" с идентификатором {result.id}')


def searching_publisher_id():
    query_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    query_publisher_name = input('Введите идентификатор (id) издателя: ')
    query_result = query_join.filter(Publisher.id_publisher == query_publisher_name)
    for result in query_result.all():
        print(
            f'Издатель c id: {query_publisher_name} найден в магазине "{result.name}" '
            f'с идентификатором {result.id}')


if __name__ == '__main__':
    searching_publisher_name()
    searching_publisher_id()


session.close()