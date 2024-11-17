# Example

This examles work with a SQL sample database called `Chinook` that can be for example [here](https://www.sqlitetutorial.net/sqlite-sample-database/).

This database consists of the following tables:

```mermaid
---
Chinook Database
---
erDiagram
    tracks {
        TrackID INTEGER PK
        Name NVARCHAR(200)
        AlbumId INTEGER FK
        MedaiTypeId INTEGER FK
        GenreId INTEGER FK
        Composer NVARCHAR(220)
        Milliseconds INTEGER
        Bytes INTEGER
        UnitPrice NUMERIC
    }
    tracks ||--o{  media_types : ""
    media_types {
        MediaTypeId INTEGER PK
        Name NVARCHAR(120)
    }
    genre |o--o{ tracks : ""
    genre {
        GenreID INTEGER PK
        Name NVARCHAR(120)
    }
    playlist_track |o--|| tracks : ""
    playlist_track {
        PlaylistId INTEGER
        TrackId INTEGER
    }
    playlist ||--o| playlist_track : ""
    playlist {
        PlaylistId INTEGER
        Name NVARCHAR(120)
    }
    albums }o--|| artists : ""
    albums |o--o{ tracks : ""
    albums {
        AlbumID INTEGER
        Title NVARCHAR(160)
        ArtistId INTEGER
    }
    artists {
        ArtistId INTEGER
        Name NVARCHAR(120)
    }
    invoice_items }o--|| tracks : ""
    invoice_items {
        InvoiceItemID INTEGER PK
        InvoiceID INTEGER FK
        TrackId INTEGER FK
        UnitPrice NUMERIC
        Quantity INTEGER
    }
    invoice ||--o{ invoice_items : ""
    invoice {
        InvoiceID INTEGER PK
        CustomerId INTEGER FK
        InvoiceDate DATETIME
        BillingAddress NVARCHAR
        BillingCity NVARCHAR
    }
    customers ||--o{ invoice : ""
    customers {
        CustomerID INTEGER PK
        FirstName NVARCHAR(40)
        LastName NVARCHAR(20)
        Company NVARCHAR(20)
        Address NVARCHAR(70)
        City NVARCHAR(40)
        State NVARCHAR(40)
        Country NVARCHAR(40)
        PostalCode NVARCHAR(10)
        Phone NVARCHAR(24)
        Fax NVARCHAR(24)
        Email NVARCHAR(60)
        SupportRepId INTEGER FK
    }
    employees |o--o{ customers : ""
    employees }o--o| employees : ""
    employees {
        EmployeeId INTEGER PK
        LastName NVARCHAR(20)
        FirstName NVARCHAR(20)
        Title NVARCHAR(30)
        ReportsTo INTEGER FK
        BirthDate DATETIME
        HireDate DATETIME
        Address NVARCHAR(70)
    }

```

## Basic Comparison between Raw SQL and `QueryWeaver`'s Query

The following comparison shows a raw SQL query and a corresponding python query made with `QueryWeaver`

=== "Raw SQL Query"

    ```sql
    SELECT
        artists.ArtistId AS 'ID',
        artists.Name AS 'Bandname',
        COUNT(albums.AlbumId) AS '# Albums'
    FROM artists
    INNER JOIN albums
        ON (artists.ArtistId = albums.ArtistId)
    GROUP BY artists.ArtistId
    HAVING (COUNT(albums.AlbumId) >= 10)
    ORDER BY COUNT(albums.AlbumId) DESC
    LIMIT 5
    ```

=== "QueryWeaver"

    ```py
    from queryweaver import SQLQueryBuilder

    with SQLQueryBuilder("examples/chinook.db") as db:
        albums = db.schema.albums
        artists = db.schema.artists

        query = (
            db.select(
                artists.ArtistId.alias("ID"),
                artists.Name.alias("Bandname"),
                albums.AlbumId.count().alias("# Albums"),
            )
            .from_table(artists)
            .join(albums, on=artists.ArtistId == albums.ArtistId)
            .group_by(artists.ArtistId)
            .having(albums.AlbumId.count() >= 10)
            .order_by(albums.AlbumId.count(), ascending=False)
            .limit(5)
        )

        print(query.to_pandas())
    ```

## Output

| ID  | Bandname     | # Albums |
| --- | ------------ | -------- |
| 90  | Iron Maiden  | 21       |
| 22  | Led Zeppelin | 14       |
| 58  | Deep Purple  | 11       |
| 50  | Metallica    | 10       |
| 150 | U2           | 10       |
