import string
from itertools import cycle
from multiprocessing import cpu_count
from argparse import ArgumentParser

import numpy as np
import pandas as pd
import psutil

from cytoolz import take
from pyspark import SparkContext, HiveContext, SparkConf


def get_conf():
    ncores = cpu_count()
    conf = SparkConf()
    bytes_per_core = psutil.avail_phymem() / ncores
    gb_per_core = int(round(bytes_per_core / 1e9))
    conf.set('spark.task.cpus', ncores)
    conf.set('spark.executor.memory', '%dg' % gb_per_core)
    conf.set('spark.driver.memory', '%dg' % gb_per_core)


def create_and_register(sql, df, name):
    sdf = sql.createDataFrame(df)
    sql.registerDataFrameAsTable(sdf, name)
    sql.cacheTable(name)


def main(args):
    from blaze import Server
    sc = SparkContext('local[*]', 'app', conf=get_conf())
    sql = HiveContext(sc)

    n = args.nrows
    df = pd.DataFrame({'a': np.random.randn(n),
                       'b': np.random.randint(10, size=n),
                       'c': list(take(n, cycle(string.ascii_uppercase)))})
    df2 = pd.DataFrame({'A': np.random.randn(n),
                        'B': np.random.randint(10, size=n),
                        'C': list(take(n, cycle(string.ascii_uppercase)))})

    # do hive things
    create_and_register(sql, df, 'foo')
    create_and_register(sql, df2, 'bar')

    # run blaze server
    Server(sql).run()


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('nrows', type=int,
                   help='Number of rows of a fake dataset to create')
    main(p.parse_args())
