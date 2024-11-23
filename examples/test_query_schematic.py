from queryweaver import Schematic, SQLQueryBuilder

# Define a schema from yaml
schema = Schematic.from_yaml("./examples/example.yaml")
# print(schema)


# Use the SQLQueryBuilder with a predefined schema
with SQLQueryBuilder("examples/example.db", schema=schema) as db:
    users = db.schema.users  # type: ignore
    orders = db.schema.orders  # type: ignore

    query = (
        db.select(
            users.id.alias("ID"),
            users.name.alias("First Name"),
            orders.amount.alias("Amount"),
        )
        .from_table(users)
        .join(
            orders,
            on=users.id == orders.user_id,
        )
        .order_by(orders.amount, ascending=False)
    )

    print(query.execute())
# The connection is automatically closed after the 'with' block ends.
