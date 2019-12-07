import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
loglevel = 'info'
accesslog = '-'
bind = '0.0.0.0:8080'
