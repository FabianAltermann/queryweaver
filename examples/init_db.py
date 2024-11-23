import sqlite3


def initialize_test_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        )
    """)

    # Populate users table with sample data
    cursor.executemany(
        """
        INSERT INTO users (name, age) VALUES (?, ?)
    """,
        [
            ("Alice", 30),
            ("Bob", 24),
            ("Charlie", 29),
            ("David", 35),
            ("Eva", 22),
            ("Frank", 28),
            ("Grace", 27),
            ("Hannah", 32),
            ("Ivy", 26),
            ("Jack", 31),
        ],
    )

    # Populate products table with sample data
    cursor.executemany(
        """
        INSERT INTO products (name, price) VALUES (?, ?)
    """,
        [
            ("Product A", 9.99),
            ("Product B", 19.99),
            ("Product C", 29.99),
            ("Product D", 39.99),
            ("Product E", 49.99),
        ],
    )

    # Populate orders table with sample data
    cursor.executemany(
        """
        INSERT INTO orders (user_id, amount) VALUES (?, ?)
    """,
        [
            (1, 59.97),
            (2, 19.99),
            (3, 89.97),
            (4, 39.99),
            (5, 99.98),
        ],
    )

    # Populate order_items table with sample data
    cursor.executemany(
        """
        INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)
    """,
        [
            (1, 1, 1),  # User 1 bought 1 of Product A
            (1, 2, 2),  # User 1 bought 2 of Product B
            (2, 3, 1),  # User 2 bought 1 of Product C
            (3, 4, 3),  # User 3 bought 3 of Product D
            (4, 5, 2),  # User 4 bought 2 of Product E
            (5, 1, 2),  # User 5 bought 2 of Product A
            (5, 4, 1),  # User 5 bought 1 of Product D
        ],
    )

    conn.commit()
    conn.close()


# Initialize the test database
initialize_test_database("./example.db")

print("Test database initialized successfully.")
