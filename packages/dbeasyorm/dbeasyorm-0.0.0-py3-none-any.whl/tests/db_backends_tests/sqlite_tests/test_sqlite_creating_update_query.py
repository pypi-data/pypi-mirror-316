def test_corrected_creating_update_query(sqlite_backend):
    assert sqlite_backend.generate_update_sql("USER", ('name', 'age'), ('id',)) == \
        "UPDATE USER SET name=?, age=? WHERE id=?"

    assert sqlite_backend.generate_update_sql("USER", ('name', 'age'), ('id', 'is_admin')) == \
        "UPDATE USER SET name=?, age=? WHERE id=? AND is_admin=?"
