""" This module is using to create useful prometheus metrics
"""
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
from prometheus_client.exposition import choose_encoder
import logging
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')



def StartPrometheusServer(port : int =9000):
    logging.log(0, f'Starting Prometheus server. Listening on {port}')
    start_http_server(port)