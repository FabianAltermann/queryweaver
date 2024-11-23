from queryweaver import SQLQueryBuilder

with SQLQueryBuilder("examples/chinook.db") as db:
    # # Access the 'id' column of the 'users' table using dot notation
    employees = db.schema.employees  # type: ignore

    query = (
        db.select(
            employees.EmployeeId.alias("ID"),
            employees.FirstName.alias("First Name"),
            employees.LastName.alias("Last Name"),
            employees.Title.alias("Title"),
            employees.BirthDate.alias("Birth Date"),
        )
        .from_table(employees)
        .where(employees.Title.like("%IT%"))
        .order_by(employees.BirthDate, ascending=False)
    )

    print(query)
