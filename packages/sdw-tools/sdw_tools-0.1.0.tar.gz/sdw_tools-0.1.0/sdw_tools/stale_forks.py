from datetime import datetime, timedelta
from sklearn.cluster import KMeans
import numpy as np

def get_fork_day_difference(fork_date, base_date):
    fork_date = datetime.strptime(fork_date, "%Y-%m-%d")
    base_date = datetime.strptime(base_date, "%Y-%m-%d")
    return (base_date - fork_date).days

def get_stale_forks(forks, base_date):
    backup_forks = []
    active_forks = []
    stale1 = []
    stale2 = []
    keys, values = [], []
    diff_list = []
    for fork in forks:
        fork_create_date = datetime.fromisoformat(fork['created_at'][:-1])
        fork_push_date = datetime.fromisoformat(fork['pushed_at'][:-1])
        if(fork_push_date < fork_create_date):
            backup_forks.append(fork)
            continue
        diff = get_fork_day_difference(fork['pushed_at'][:10], base_date)
        diff_list.append(diff)
    diff_list = np.array(diff_list)
    mean_diff = np.mean(diff_list)
    std = np.std(diff_list)
    for fork in forks:
        fork_create_date = datetime.fromisoformat(fork['created_at'][:-1])
        fork_push_date = datetime.fromisoformat(fork['pushed_at'][:-1])
        if(fork_push_date < fork_create_date):
            backup_forks.append(fork)
            continue
        diff = get_fork_day_difference(fork['pushed_at'][:10], base_date)
        # print(diff)
        if(diff <= mean_diff - std):
            active_forks.append(fork)
        else:
            keys.append(fork)
            values.append(diff)
    np_values = np.array(values)
    np_values = np_values.reshape(-1, 1)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(np_values)
    min1, min2 = 10000000000000, 10000000000000
    for i in range(len(kmeans.labels_)):
        if(kmeans.labels_[i] == 0):
            min1 = min(min1, values[i])
            stale1.append(keys[i])
        else:
            min2 = min(min2, values[i])
            stale2.append(keys[i])
    if(min1 > min2):
        return active_forks, stale2, stale1, backup_forks
    else:
        return active_forks, stale1, stale2, backup_forks