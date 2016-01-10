import json
from pipeline import Pipeline
from engine import PredictionEngine

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask, request
from flask import Blueprint

main = Blueprint('main', __name__)


@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User {} top ratings requested".format(user_id))
    res = prediction_engine.get_top_ratings(user_id, count)
    return json.dumps(res)


@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    logger.debug("User {} rating requested for movie {}".format(user_id, movie_id))
    res = prediction_engine.get_ratings_for_movieid(user_id, [movie_id])
    return json.dumps(res)


@main.route("/<int:user_id>/ratings", methods=["POST"])
def add_ratings(user_id):
    if request.form.keys():
        ratings_raw = request.form.keys()[0].strip().split("\n")
        ratings_list = [r.split(",") for r in ratings_raw]
        # pack each rating with user_id and movie_id
        res = []
        for l in ratings_list:
            if check_element(l):
                ele = (user_id, int(l[0]), float(l[1]))
                res.append(ele)

        prediction_engine.add_ratings(res)

        return json.dumps(res)
    else:
        pass


def create_app(spark_context, dataset_path):

    # prepare the data for prediction engine
    pipeline = Pipeline(spark_context, dataset_path)
    ratingsRDD = pipeline.reshape_ratings('ratings.csv')
    moviesRDD, titlesRDD = pipeline.reshape_movies('movies.csv')

    global prediction_engine
    prediction_engine = PredictionEngine(spark_context, ratingsRDD, moviesRDD, titlesRDD)

    app = Flask(__name__)
    app.register_blueprint(main)
    return app


def check_element(l):
    try:
        int(l[0])
        float(l[1])
    except ValueError:
        return False
    else:
        return True
