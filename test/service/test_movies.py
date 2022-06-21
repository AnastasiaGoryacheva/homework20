from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def test_movie_dao():
    movie_dao = MovieDAO(None)

    m1 = Movie(id=1, title="Железный человек", description="Гений, миллиардер, плейбой, филантроп", trailer="ссылка",
               year=2002, rating=9.6, genre_id=1, director_id=1)
    m2 = Movie(id=2, title="Железный человек 2", description="Тони Старк - Железный человек", trailer="ссылка",
               year=2005, rating=9.7, genre_id=1, director_id=1)
    m3 = Movie(id=3, title="Железный человек 3", description="А я так просто Железный человек!", trailer="ссылка",
               year=2008, rating=9.8, genre_id=1, director_id=1)

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=[m1, m2, m3])
    movie_dao.create = MagicMock(return_value=Movie(id=2))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    movie_dao.partially_update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "id": 1,
            "title": "Мстители",
            "description": "Не смогли смириться с поражением. И куда вас это привело, снова ко мне.",
            "trailer": "ссылка",
            "year": 2020,
            "rating": 10.0,
            "genre_id": 1,
            "director_id": 1
        }
        movie = self.movie_service.create(movie_d)

        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "id": 2,
            "title": "Мстители. Финал.",
            "description": "В бой",
            "trailer": "ссылка на трейлер",
            "year": 2021,
            "rating": 9.9,
            "genre_id": 2,
            "director_id": 2
        }

        self.movie_service.update(movie_d)

    def test_partially_update(self):
        movie_d = {
            "id": 1,
            "year": 2007
        }

        self.movie_service.update(movie_d)
