def test_corrected_creating_select_query(sqlite_backend):
    assert sqlite_backend.generate_select_sql(
        "USER", ('username', "age", "is_admin"), where_clause=dict(name='John', age=30)
    ) == "SELECT username, age, is_admin FROM USER WHERE name = 'John' AND age = 30"

    assert sqlite_backend.generate_select_sql(
        "USER", ('*'), dict(_id=30), limit=5, offset=10
    ) == "SELECT * FROM USER WHERE _id = 30 LIMIT 5 OFFSET 10"
