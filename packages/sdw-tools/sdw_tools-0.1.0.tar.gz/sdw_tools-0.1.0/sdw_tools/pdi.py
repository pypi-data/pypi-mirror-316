from datetime import datetime, timedelta
import numpy as np

def get_fork_day_difference(fork_date, base_date):
    fork_date = datetime.strptime(fork_date, "%Y-%m-%d")
    base_date = datetime.strptime(base_date, "%Y-%m-%d")
    return (base_date - fork_date).days

def get_active_users(forks, pushed_at):
    user_map = {}

    diff_list = []
    for fork in forks:
        fork_create_date = datetime.fromisoformat(fork['created_at'][:-1])
        fork_push_date = datetime.fromisoformat(fork['pushed_at'][:-1])
        if(fork_push_date < fork_create_date):
            continue
        diff = get_fork_day_difference(fork['pushed_at'][:10], pushed_at)
        diff_list.append(diff)
    diff_list = np.array(diff_list)
    mean_diff = np.mean(diff_list)
    std = np.std(diff_list)

    for fork in forks:
        fork_created_at = datetime.fromisoformat(fork['created_at'][:-1])
        fork_pushed_at = datetime.fromisoformat(fork['pushed_at'][:-1])
        if(fork_pushed_at < fork_created_at):
            continue
        diff = get_fork_day_difference(fork['pushed_at'][:10], pushed_at)
        if(diff <= mean_diff - std):
            user_map[fork['owner']['id']] = fork_created_at
    return user_map

def get_pdi(forks, pull_requests, pushed_at):
    active_users = get_active_users(forks, pushed_at)
    pdi = 0
    for pr in pull_requests:
        if(pr['user']['id'] in active_users):
            if(pr['closed_at'] is not None):
                diff = get_fork_day_difference(pr['closed_at'][:10], pushed_at)
                if(diff <= 90):
                    del active_users[pr['user']['id']]
                    pdi += 1
    contributing = pdi
    independent= len(active_users) - pdi
    if(independent != 0):
        pdi = contributing / independent
    else:
        pdi = "Undefined"
    return contributing, independent, pdi