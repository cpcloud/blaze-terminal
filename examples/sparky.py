import string
from itertools import cycle
from multiprocessing import cpu_count

import numpy as np
import pandas as pd
import psutil

from cytoolz import take
from pyspark import SparkContext, HiveContext, SparkConf
from blaze import Server, Data


def get_conf():
    ncores = cpu_count()
    conf = SparkConf()
    bytes_per_core = psutil.avail_phymem() / ncores
    gb_per_core = int(round(bytes_per_core / 1e9))
    conf.set('spark.task.cpus', ncores)
    conf.set('spark.executor.memory', '%dg' % gb_per_core)
    conf.set('spark.driver.memory', '%dg' % gb_per_core)


if __name__ == '__main__':
    sc = SparkContext('local[*]', 'app', conf=get_conf())
    sql = HiveContext(sc)

    n = 1000000
    df = pd.DataFrame({'a': np.random.randn(n),
                       'b': np.random.randint(10, size=n),
                       'c': list(take(n, cycle(string.ascii_uppercase)))})
    sdf = sql.createDataFrame(df)
    sql.registerDataFrameAsTable(sdf, 'df')
    sql.cacheTable('df')
    Server(Data(sql)).run()
