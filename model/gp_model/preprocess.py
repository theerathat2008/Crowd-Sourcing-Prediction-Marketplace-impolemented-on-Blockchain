import pandas as pd
import csv
import numpy as np
import dask.dataframe as dd

import datetime as dt

# Example of data
ENERGY_DATASET = 'src/dataset/Power-Networks-LCL-June2015(withAcornGps)v2.csv'
USER = 'MAC000002'
columns = ['id', 'rate', 'dateTime', 'usage', 'Acorn', 'Acorn_grouped']
to_drop = ['rate', 'Acorn', 'Acorn_grouped']

date_format = "%Y-%m-%d %H:%M:%S.%f"

#use date as key, if data is null or doesn't exist, use average usage of the other users on the same day
#count the number of users who has data for each day

def convert_float(u):
    try:
        return float(u)
    except ValueError:
        return 0.0


def create_all_agg_demands():
    dataset = dd.read_csv(ENERGY_DATASET, names=columns, header=0,
                          converters={'KWH/hh (per half hour)': convert_float},
                          low_memory=False)
    dataset = dataset.drop(columns = to_drop)
    dataset = dataset.get_partition(0)

    trainset, predset = generate_trainset(dataset)
    trainset_array = trainset.values
    predset_array = predset.values
    print(trainset_array)

    my_demands = dataset[dataset['id'] == USER][['dateTime', 'usage']]
    my_demands_array = my_demands.values.compute()

    params = []
    adjust = None
    idx = 0
    start, end = 0, 0

    for i, d in enumerate(trainset_array):
        print(d)
        d = d[0]
        print(d)
        if idx != len(trainset_array):
            date = dt.datetime.strptime(d, date_format)
            my_date, my_demand = my_demands_array[idx]
            my_demand = convert_float(my_demand)
            if not adjust:
                adjust = date.timestamp()
            my_dt = my_date.timestamp() - adjust
            new_dt = date.timestamp() - adjust
            if new_dt == my_dt:
                if idx == 0:
                    start = i
                idx += 1
                params.append([my_dt, my_demand])
        else:
            end = i

    aggs = []
    for demand, _ in trainset_array[start:end]:
        demand = sum(map(float, demand.split()))
        aggs.append(demand)

    return params, aggs
#
def generate_trainset(dataset):
    demands = dataset[['dateTime', 'usage']].groupby('dateTime')
    agg_demands = demands.sum().reset_index().compute()

    group_size = len(agg_demands.index) // 10
    first = True

    for i in range(group_size):
        pop = agg_demands[(i * group_size):((i+1) * group_size)]
        sample_size = int(0.8 * group_size)
        sample = agg_demands.sample(sample_size)
        pop.replace(sample.index, np.nan)
        if not first:
            trainset.append(sample)
            predset.append(pop)
        else:
            first = False
            trainset = sample
            predset = pop

    trainset = trainset.set_index('dateTime')
    predset = predset.set_index('dateTime')

    return trainset, predset
