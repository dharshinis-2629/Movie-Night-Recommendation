from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///movie_recommender.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def upsert_movie(db, movie_data):
    from .models import Movie

    movie = db.query(Movie).filter(Movie.movie_id == movie_data["id"]).first()
    genres = ",".join(str(genre_id) for genre_id in movie_data.get("genre_ids", []))

    if movie:
        movie.title = movie_data.get("title") or movie.title
        movie.overview = movie_data.get("overview")
        movie.poster_path = movie_data.get("poster_path")
        movie.release_date = movie_data.get("release_date")
        movie.vote_average = movie_data.get("vote_average")
        movie.genres = genres
        return movie

    movie = Movie(
        movie_id=movie_data["id"],
        title=movie_data.get("title") or "Untitled",
        overview=movie_data.get("overview"),
        poster_path=movie_data.get("poster_path"),
        release_date=movie_data.get("release_date"),
        vote_average=movie_data.get("vote_average"),
        genres=genres,
    )
    db.add(movie)
    return movie


def sync_movies(db, movies):
    synced_movies = []
    for movie_data in movies:
        if not movie_data or not movie_data.get("id"):
            continue
        synced_movies.append(upsert_movie(db, movie_data))
    db.commit()
    return synced_movies
