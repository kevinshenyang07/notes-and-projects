import os
import cherrypy
from paste.translogger import TransLogger
from pyspark import SparkContext, SparkConf
from app import create_app


def init_sc():

    conf = SparkConf().setAppName("prediction_service_demo")
    # upload other python files to spark cluster
    sc = SparkContext(conf=conf, pyFiles=['app.py', 'engine.py', 'pipeline.py'])
    return sc


def run_server(app):

    # use Paste to get the logging from WSGI service
    app_logged = TransLogger(app)

    # mount the WSGI callable object (app) on the root dir
    cherrypy.tree.graft(app_logged, '/')
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 5432,
        })

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':

    '''
    # init spark context and load libs
    import findspark
    findspark.init('/Users/apple/spark-1.5.1-bin-hadoop2.6')
    '''

    sc = init_sc()

    dataset_path = os.path.join('datasets', 'ml-latest-small')
    app = create_app(sc, dataset_path)

    run_server(app)
