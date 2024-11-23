from queryweaver import SQLQueryBuilder

with SQLQueryBuilder("examples/chinook.db") as db:
    customers = db.schema.customers  # type: ignore
    invoices = db.schema.invoices  # type: ignore

    query = (
        db.select(
            customers.CustomerId.alias("ID"),
            customers.FirstName.alias("First Name"),
            customers.LastName.alias("Last Name"),
            (invoices.Total.max() - invoices.Total.min()).alias("MAX - MIN"),
        )
        .from_table(customers)
        .join(invoices, on=customers.CustomerId == invoices.CustomerId)
        .group_by(customers.CustomerId)
        .order_by(invoices.Total.max() - invoices.Total.min(), ascending=False)
    )

    print(query)
