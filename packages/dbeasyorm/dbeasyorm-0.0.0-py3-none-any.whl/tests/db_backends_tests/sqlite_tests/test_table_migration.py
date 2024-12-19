from faker import Faker
import random

from tests.models_tests.CustomeTestModel import init_custome_test_model, init_post_test_model_related_to


fake = Faker()


def test_migration_query_sqlite(testing_db):
    CustomeTestModel = init_custome_test_model()

    CustomeTestModel.migrate()
    expected_sql = """CREATE TABLE IF NOT EXISTS CUSTOMETESTMODEL (_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, is_admin INTEGER, age INTEGER NOT NULL, salary REAL);"""

    normalized_actual = " ".join(CustomeTestModel.query_creator.sql.split())
    normalized_expected = " ".join(expected_sql.split())
    assert normalized_actual == normalized_expected


def test_migration_query_with_foreign_key_sqlite(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)
    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    PostTestModel.migrate()

    expected_sql = """CREATE TABLE IF NOT EXISTS POSTTESTMODEL (_id INTEGER PRIMARY KEY AUTOINCREMENT,
        is_read INTEGER, id_autor INTEGER , content TEXT, FOREIGN KEY (id_autor) REFERENCES CUSTOMETESTMODEL (_id) ON DELETE CASCADE);"""

    normalized_actual = " ".join(PostTestModel.query_creator.sql.split())
    normalized_expected = " ".join(expected_sql.split())
    assert normalized_actual == normalized_expected


def test_using_model_after_migration_query_with_foreign_key_sqlite(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    PostTestModel.migrate().backend.execute(query=PostTestModel.query_creator.sql)

    assert CustomeTestModel.query_creator.create(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).execute() == 1

    assert PostTestModel.query_creator.create(
        is_read=0,
        id_autor=1,
        content=fake.text()
    ).execute() == 1


def test_using_model_after_migration_query(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    assert CustomeTestModel.query_creator.create(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).execute() == 1

    assert CustomeTestModel.query_creator.create(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).execute() == 2

    queryset = CustomeTestModel.query_creator.all().execute()

    assert len(queryset) == 2
    assert isinstance(queryset[0], CustomeTestModel) is True
    assert isinstance(queryset[1], CustomeTestModel) is True


def test_get_table_schemas(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    PostTestModel.migrate().backend.execute(query=PostTestModel.query_creator.sql)

    expected_schemas = {
        'CUSTOMETESTMODEL': {
            '_id': 'INTEGER',
            'name': 'TEXT',
            'age': 'INTEGER',
            'email': 'TEXT',
            'is_admin': 'INTEGER',
            'salary': 'REAL'
        },
        'POSTTESTMODEL': {
            '_id': 'INTEGER',
            'content': 'TEXT',
            'id_autor': 'INTEGER',
            'is_read': 'INTEGER'
        }
    }

    assert CustomeTestModel.migrate().backend.get_database_schemas() == expected_schemas
