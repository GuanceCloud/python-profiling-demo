import datetime
import functools
import gzip
import json
import os
import re
import time
from typing import List, Optional, TypeVar, Callable
from ddtrace import tracer
import logging
from ddtrace import patch

patch(logging=True)

from flask import Flask, request, jsonify

import ddtrace.profiling.auto

I = TypeVar('I')
O = TypeVar('O')

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.DEBUG


def convert_or_none(v: Optional[I], converter: Callable[[I], O]) -> Optional[O]:
    if v is None:
        return v

    return converter(v)


class Movie:
    def __init__(self, d: dict):
        self.__d = d

    @property
    def title(self) -> Optional[str]:
        return convert_or_none(self.__d.get("title"), str)

    @property
    def rating(self) -> Optional[float]:
        return convert_or_none(self.__d.get("vote_average"), float)

    @property
    def release_date(self) -> Optional[str]:
        return convert_or_none(self.__d.get("release_date"), str)

    def to_dict(self):
        return {
            "title": self.title,
            "rating": self.rating,
            "release_date": self.release_date,
        }


SERVER_DIR = os.path.dirname(os.path.realpath(__file__))
CACHED_MOVIES: Optional[List[Movie]] = None

app = Flask(__name__)


def main():
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)


@app.route('/movies')
@tracer.wrap()
def movies():
    log.info("/movies receive request")

    query: str = request.args.get("q", request.args.get("query"))

    movies_list = get_movies()

    fib = fibonacci(43)
    log.info("fibonacci(43) = %d", fib)

    # Problem: We are sorting over the entire list but might be filtering most of it out later.
    # Solution: Sort after filtering
    movies_list = sort_desc_release_date(movies_list)

    if query:
        movies_list = [m for m in movies_list if re.search(query.upper(), m.title.upper())]

    return jsonify([m.to_dict() for m in movies_list])


def fibonacci(num: int):
    if num <= 2:
        return 1
    return fibonacci(num-1) + fibonacci(num-2)


def sort_desc_release_date(movies_list: List[Movie]) -> List[Movie]:
    # Problem: We are parsing a datetime for each comparison during sort
    # Example Solution:
    #   Since date is in isoformat (yyyy-mm-dd) already, that one sorts nicely with normal string sorting
    #   `return sorted(movies, key=lambda m: m.release_date, reverse=True)`
    def sorting_cmp(m1: Movie, m2: Movie) -> int:
        try:
            m1_dt = datetime.date.fromisoformat(m1.release_date)
        except Exception:
            m1_dt = datetime.date.min
        try:
            m2_dt = datetime.date.fromisoformat(m2.release_date)
        except Exception:
            m2_dt = datetime.date.min
        return int((m1_dt - m2_dt).total_seconds())

    return sorted(movies_list, key=functools.cmp_to_key(sorting_cmp), reverse=True)


def get_movies() -> List[Movie]:
    global CACHED_MOVIES

    if CACHED_MOVIES:
        return CACHED_MOVIES

    return load_movies()


def load_movies():
    global CACHED_MOVIES
    with gzip.open(os.path.join(SERVER_DIR, "./movies5000.json.gz")) as f:
        CACHED_MOVIES = [Movie(d) for d in json.load(f)]
        return CACHED_MOVIES


if __name__ == '__main__':
    main()
