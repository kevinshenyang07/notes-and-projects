import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Pipeline:

    def __init__(self, sc, dataset_path):

        logger.info("Opening data pipeline: ")
        self.sc = sc
        self.dataset_path = dataset_path

    def __load_csv(self, file_name):

        logger.info("Loading {}...".format(file_name))
        file_path = os.path.join(self.dataset_path, file_name)
        rawRDD = self.sc.textFile(file_path)
        file_header = rawRDD.take(1)[0]
        fileRDD = rawRDD.filter(lambda l: l != file_header)\
                        .map(lambda l: l.split(","))
        return fileRDD

    def reshape_ratings(self, file_name):

        fileRDD = self.__load_csv(file_name)
        ratingsRDD = fileRDD.map(lambda x: (x[1],x[2],int(x[3])))\
                            .cache()
        return ratingsRDD

    def reshape_businesses(self, file_name):

        fileRDD = self.__load_csv(file_name)
        businessesRDD = fileRDD.map(lambda x: (int(x[0]),x[1],x[2])).cache()
        namesRDD = businessesRDD.map(lambda x: (int(x[0]),x[1])).cache()

        return businessesRDD, namesRDD


