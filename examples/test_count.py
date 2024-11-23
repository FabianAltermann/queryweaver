from queryweaver import SQLQueryBuilder

with SQLQueryBuilder("examples/chinook.db") as db:
    albums = db.schema.albums  # type: ignore
    artists = db.schema.artists  # type: ignore

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

    print(query)
    print(query.to_pandas())
