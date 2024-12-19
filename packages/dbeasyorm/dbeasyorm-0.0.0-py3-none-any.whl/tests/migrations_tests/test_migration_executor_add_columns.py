import pytest
from faker import Faker
import random

from tests.models_tests.CustomeTestModel import init_custome_test_model


fake = Faker()


def test_execute_few_columns_to_add_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    # Try creating a model with non-existent fields
    FAKE_BIO = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    FAKE_EXPERIANCE = 23
    assert CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3),
        bio=FAKE_BIO,
        professional_experience=FAKE_EXPERIANCE
    ).save().execute() == 1
    created_model = CustomeTestModel.query_creator.all().execute()[0]

    # try to get this fields
    with pytest.raises(AttributeError):
        assert created_model.professional_experience == FAKE_EXPERIANCE
    with pytest.raises(AttributeError):
        assert created_model.bio == FAKE_BIO

    from dbeasyorm.migrations import MigrationExecutor
    from dbeasyorm import fields
    from dbeasyorm.models.model import Model

    # 1. Add this fields into model
    class CustomeTestModel(Model):
        name = fields.TextField()
        email = fields.TextField(unique=True)
        is_admin = fields.BooleanField(null=True)
        age = fields.IntegerField()
        salary = fields.FloatField(null=True)
        bio = fields.TextField(null=True)
        professional_experience = fields.IntegerField(null=True)

    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)

    # Add these fields to your creation fields
    # NOTE: If we are going to use sqlite, we only really need the model
    # because we will create a new one based on this model.
    # But the interface requires passing all fields to be created for compatibility with other backends
    db_schemas = migration_exec.db_backend.get_database_schemas()
    detected_migrations = {
        "create_tables": [],
        "add_columns": [
            (
                CustomeTestModel.query_creator.get_table_name(),
                fields.TextField(field_name="bio", null=True),
                CustomeTestModel,
                db_schemas[CustomeTestModel.query_creator.get_table_name()]
            ),
            (
                CustomeTestModel.query_creator.get_table_name(),
                fields.IntegerField(field_name="professional_experience", null=True),
                CustomeTestModel,
                db_schemas[CustomeTestModel.query_creator.get_table_name()]
            )],
        "drop_tables": [],
        "remove_columns": []
    }

    migration_exec.execute_detected_migration(detected_migration=detected_migrations)

    # now we can insert model and get this fileds
    assert CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3),
        bio=FAKE_BIO,
        professional_experience=FAKE_EXPERIANCE
    ).save().execute() == 2

    created_model_with_new_fileds = CustomeTestModel.query_creator.all().execute()[1]

    # try to get this fields
    assert created_model_with_new_fileds.professional_experience == FAKE_EXPERIANCE
    assert created_model_with_new_fileds.bio == FAKE_BIO


def test_execute_few_columns_to_add_with_foreigth_key_detected(testing_db):
    from dbeasyorm import fields
    from dbeasyorm.models.model import Model
    from dbeasyorm.migrations import MigrationExecutor

    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.query_creator.backend.connect()
    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)

    # 1. create Profile Model
    class Profile(Model):
        bio = fields.TextField(null=True)
        professional_experience = fields.IntegerField(null=True)

    detected_migrations = {
        "create_tables": [Profile],
        "add_columns": [],
        "drop_tables": [],
        "remove_columns": []
    }
    migration_exec.execute_detected_migration(detected_migration=detected_migrations)

    # 2. Add new Foreign key to CustomeTestModel
    class Profile(Model):
        bio = fields.TextField(null=True)
        professional_experience = fields.IntegerField(null=True)
        autor = fields.ForeignKey(related_model=CustomeTestModel)

    # 3. Add CustomeTestModel to create_tables, and fied with Foreign key
    db_schemas = migration_exec.db_backend.get_database_schemas()
    detected_migrations = {
        "create_tables": [CustomeTestModel],
        "add_columns": [
            (
                Profile.query_creator.get_table_name(),
                fields.ForeignKey(field_name='autor', related_model=CustomeTestModel),
                Profile,
                db_schemas[Profile.query_creator.get_table_name()]
            )
        ],
        "drop_tables": [],
        "remove_columns": []
    }
    migration_exec.execute_detected_migration(detected_migration=detected_migrations)

    assert CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3),
    ).save().execute() == 1
    user = CustomeTestModel.query_creator.get_one(_id=1).execute()
    assert Profile(bio=fake.text(), professional_experience=23, autor=user).save().execute() == 1
    profile = Profile.query_creator.get_one(_id=1).execute()
    assert profile.autor.name == user.name
