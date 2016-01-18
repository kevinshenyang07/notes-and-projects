from pyspark.mllib.recommendation import ALS

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_counts_and_averages(id_ratings):

    # input is a tuple like (movie_id, ratings_iterable)
    n_ratings = len(id_ratings[1])
    avg_ratings = sum(x for x in id_ratings[1]) / float(n_ratings)

    return id_ratings[0], (n_ratings, avg_ratings)


class PredictionEngine:

    def __init__(self, sc, ratingsRDD, moviesRDD, titlesRDD):

        self.sc = sc
        self.ratingsRDD = ratingsRDD
        self.moviesRDD = moviesRDD
        self.titlesRDD = titlesRDD
        self.__count_and_average_ratings()

        self.rank = 8
        self.seed = 5L
        self.iterations = 10
        self.regularization_parameter = 0.1
        self.__train_model()

    def __train_model(self):

        logger.info("Training the ALS model...")
        self.model = ALS.train(self.ratingsRDD, self.rank, seed=self.seed,
                               iterations=self.iterations,
                               lambda_=self.regularization_parameter)
        logger.info("ALS model built!")

    def __count_and_average_ratings(self):

        # updates the movies ratings counts from self.ratingsRDD
        logger.info("Counting movie ratings...")
        movieidRatingsRDD = self.ratingsRDD.map(lambda x: (x[1], x[2]))\
                                          .groupByKey()
        movieidAvgRatingsRDD = movieidRatingsRDD.map(get_counts_and_averages)
        self.moviesRatingCountsRDD = movieidAvgRatingsRDD\
                                         .map(lambda x: (x[0], x[1][0]))

    def __predict_ratings(self, userMovieRDD):

        # get predictions for a given (userID, movieID) formatted ratingsRDD
        # return a (movie_title, movie_rating, num_rating) formatted RDD
        predictedRDD = self.model.predictAll(userMovieRDD)
        predictedRatingRDD = predictedRDD.map(lambda x: (x.product, x.rating))
        ratingTitleCountRDD = predictedRatingRDD.join(self.titlesRDD)\
                                                .join(self.moviesRatingCountsRDD)
        resultRDD = ratingTitleCountRDD.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))

        return resultRDD



    def add_ratings(self, ratings):

        # additive ratings formatted as (user_id, movie_id, rating)
        newRatingsRDD = self.sc.parallelize(ratings)
        self.ratingsRDD = self.ratingsRDD.union(newRatingsRDD)

        # recompute count, avg ratings and re-train the model
        self.__count_and_average_ratings()
        self.__train_model()

        return ratings

    def get_ratings_for_movieid(self, user_id, movie_ids):

        # input: user_id and list of movie ids
        requestedRDD = self.sc.parallelize(movie_ids)\
                              .map(lambda x: (user_id, x))
        # get predicted ratings
        ratings = self.__predict_ratings(requestedRDD).collect()

        return ratings

    def get_top_ratings(self, user_id, n):

        # recommends top n unrated movies to user_id
        # first get pairs of (user_id, movie_id) for user_id unrated movies
        unratedMoviesRDD = self.moviesRDD.filter(lambda rating: not rating[1]==user_id)\
                                         .map(lambda x: (user_id, x[0]))
        # get predicted ratings
        ratings = self.__predict_ratings(unratedMoviesRDD)\
                           .filter(lambda r: r[2]>=25)\
                           .takeOrdered(n, key=lambda x: -x[1])
        return ratings
