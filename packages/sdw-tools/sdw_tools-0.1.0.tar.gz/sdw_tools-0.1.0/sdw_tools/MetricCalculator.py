import os
from utils import read_list_from_file
from duplicate_work import calculate_duplicate_work
from ffr import get_balance_graph, get_graph_data
from pdi import get_pdi
from stale_forks import get_stale_forks
from backlog_inversion import get_inversion
from datetime import datetime
from dateutil.relativedelta import relativedelta

class MetricCalculator:
    def __init__(self, owners, repos, bug_labels=None, feature_labels=None, high_labels=None, mid_labels=None, low_labels=None):
        if type(owners) is str:
            owners = [owners]
        if type(repos) is str:
            repos = [repos]
        self._owners = owners
        self._repos = repos
        self.set_prefix_names()
        self.create_label_map(bug_labels, feature_labels)
        self.create_priority_map(high_labels, mid_labels, low_labels)
        self._metrics = None
        self._map = {
            "stale_forks": calculate_duplicate_work,
            "pdi": get_pdi,
            "graph": get_graph_data,
            "duplicate_work": calculate_duplicate_work,
            "backlog_inversion": get_inversion
        }

    @property
    def owners(self):
        if(len(self._owners) == 1):
            return self._owners[0]
        return self._owners
    
    @owners.setter
    def owners(self, owners):
        if type(owners) is str:
            owners = [owners]
        self._owners = owners
    
    @property
    def repos(self):
        if(len(self._repos) == 1):
            return self._repos[0]
        return self._repos

    @repos.setter
    def repos(self, repos):
        if type(repos) is str:
            repos = [repos]
        self._repos = repos

    @property
    def prefix_names(self):
        if(len(self._prefix_names) == 1):
            return self._prefix_names[0]
        return self._prefix_names
    
    @prefix_names.setter
    def prefix_names(self, prefix_names):
        print("Cannot set prefix names directly")

    def set_prefix_names(self):
        self._prefix_names = []
        for owner, repo in zip(self._owners, self._repos):
            owner = ''.join(e for e in owner if e.isalnum())
            repo = ''.join(e for e in repo if e.isalnum())
            self._prefix_names.append(f"{owner}_{repo}")
    
    def create_label_map(self, bug_labels, feature_labels):
        self._bug_labels = {}
        self._feature_labels = {}
        if bug_labels is None or feature_labels is None:
            for repo in self._repos:
                self._bug_labels[repo] = None
                self._feature_labels[repo] = None
            return
        for repo, bug_label, feature_label in zip(self._repos, bug_labels, feature_labels):
            if bug_label.lower()=="none" or bug_label=="":
                bug_label=None
            self._bug_labels[repo] = bug_label
            if feature_label.lower()=="none" or feature_label=="":
                feature_label=None
            self._feature_labels[repo] = feature_label
    
    def create_priority_map(self, high_labels, mid_labels, low_labels):
        self._high_labels = {}
        self._mid_labels = {}
        self._low_labels = {}
        if high_labels is None or mid_labels is None or low_labels is None:
            for repo in self._repos:
                self._high_labels[repo] = None
                self._mid_labels[repo] = None
                self._low_labels[repo] = None
            return
        for repo, high_label, mid_label, low_label in zip(self._repos, high_labels, mid_labels, low_labels):
            if high_label.lower()=="none" or high_label=="":
                high_label=None
            self._high_labels[repo] = high_label
            if mid_label.lower()=="none" or mid_label=="":
                mid_label=None
            self._mid_labels[repo] = mid_label
            if low_label.lower()=="none" or low_label=="":
                low_label=None
            self._low_labels[repo] = low_label

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        if metrics is None:
            self._metrics = None
        else:
            print("Cannot set metrics directly")

    def add_for_calculation(self, to_calculate):
        if type(to_calculate) is str:
            to_calculate = [to_calculate]
        # Check if the user wants to calculate all metrics
        if "all" in to_calculate:
            self._metrics = list(self._map.keys())
            return

        # Check if the values are valid
        for metric in to_calculate:
            if metric not in self._map.keys():
                print(f"\033[31m{metric} is not a valid metric to calculate\033[0m")
                return
        
        # Check if metric is already in the list, otherwise add
        if self._metrics is None:
            self._metrics = []
        for metric in to_calculate:
            if metric not in self._metrics:
                self._metrics.append(metric)
            else:
                print(f"\033[31m{metric} is already in the list\033[0m")
    
    def calc_stale_forks(self, repo, forks, pushed_at, path):
        print(f"\033[32mCalculating stale forks for {repo}\033[0m")
        active, potential, stale, backup = get_stale_forks(forks, pushed_at[self._repos.index(repo)][:10])
        with open(f"{path}/stale_forks.txt", 'w') as file:
            file.write(f"Active: {len(active)}\n")
            file.write(f"Potential: {len(potential)}\n")
            file.write(f"Stale: {len(stale)}\n")
            file.write(f"Backup: {len(backup)}\n")
    
    def calc_pdi(self, repo, open_pulls, closed_pulls, forks, pushed_at, path):
        print(f"\033[32mCalculating PDI for {repo}\033[0m")
        pull_requests = []
        pull_requests.extend(open_pulls)
        pull_requests.extend(closed_pulls)
        contrinuting, independent, pdi = get_pdi(forks, pull_requests, pushed_at[self._repos.index(repo)][:10])
        with open(f"{path}/pdi.txt", 'w') as file:
            file.write(f"Contributing: {contrinuting}\n")
            file.write(f"Independent: {independent}\n")
            file.write(f"PDI: {pdi}\n")
    
    def calc_graph(self, repo, open_issues, closed_issues, current_date, path):
        print(f"\033[32mCalculating graph data for {repo}\033[0m")
        get_graph_data(closed_issues, self._bug_labels[repo], self._feature_labels[repo], path + "/images")
        issues = []
        issues.extend(open_issues)
        issues.extend(closed_issues)
        print(f"\033[32mCalculating balance graph for {repo}\033[0m")
        get_balance_graph(issues, 60, current_date, self._bug_labels[repo], self._feature_labels[repo], path + "/images")

    def calc_duplicate_work(self, repo, closed_pulls, base_date, path):
        print(f"\033[32mCalculating duplicate work for {repo}\033[0m")
        unmerged, merged, duplicate = calculate_duplicate_work(closed_pulls, base_date=base_date)
        with open(f"{path}/duplicate_work.txt", 'w') as file:
            file.write(f"Unmerged: {unmerged}\n")
            file.write(f"Merged: {merged}\n")
            file.write(f"Duplicate: {duplicate}\n")
    
    def calc_backlog_inversion(self, repo, open_issues, closed_issues, path):
        print(f"\033[32mCalculating backlog inversion for {repo}\033[0m")
        all_issues = []
        all_issues.extend(open_issues)
        all_issues.extend(closed_issues)
        hl, hm, ml = get_inversion(all_issues, self._high_labels[repo], self._mid_labels[repo], self._low_labels[repo])
        with open(f"{path}/backlog_inversion.txt", 'w') as file:
            file.write(f"High-to-Low Inversion: {hl}\n")
            file.write(f"High-to-Mid Inversion: {hm}\n")
            file.write(f"Mid-to-Low Inversion: {ml}\n")
    
    def calculate(self):
        repo_details = read_list_from_file('./data/repo_details.txt')
        pushed_at = [repo['pushed_at'] for repo in repo_details]

        for owner, repo, name in zip(self._owners, self._repos, self._prefix_names):
            print(f"Calculating for {owner}/{repo}")
            path = f"./results/{name}"
            os.makedirs(path, exist_ok=True)

            current_date = datetime.now()
            base_date = current_date - relativedelta(years=1)
            base_date = base_date.strftime("%Y-%m-%d")
            current_date = current_date.strftime("%Y-%m-%d")

            forks = None
            open_issues = None
            closed_issues = None
            open_pulls = None
            closed_pulls = None

            if self._metrics is None:
                print("Nothing set to calculate so instead calculating all metrics")
                self._metrics = list(self._map.keys())

            if "stale_forks" in self._metrics:
                if forks is None:
                    forks = read_list_from_file(f'./data/forks/{name}_forks.txt')
                self.calc_stale_forks(repo, forks, pushed_at, path) 

            if "pdi" in self._metrics:
                if open_pulls is None:
                    open_pulls = read_list_from_file(f'./data/open_PRs/{name}_open_PRs.txt')
                if closed_pulls is None:
                    closed_pulls = read_list_from_file(f'./data/closed_PRs/{name}_closed_PRs.txt')
                self.calc_pdi(repo, open_pulls, closed_pulls, forks, pushed_at, path)

            if "graph" in self._metrics:
                if self._bug_labels[repo] is None or self._feature_labels[repo] is None:
                    print("Cannot calculate graph data without bug and feature labels")
                else:
                    if open_issues is None:
                        open_issues = read_list_from_file(f'./data/open_issues/{name}_open_issues.txt')
                    if closed_issues is None:
                        closed_issues = read_list_from_file(f'./data/closed_issues/{name}_closed_issues.txt')
                    self.calc_graph(repo, open_issues, closed_issues, current_date, path)
            
            if "duplicate_work" in self._metrics:
                if closed_pulls is None:
                    closed_pulls = read_list_from_file(f'./data/closed_PRs/{name}_closed_PRs.txt')
                self.calc_duplicate_work(repo, closed_pulls, base_date, path)
            
            if "backlog_inversion" in self._metrics:
                if self._high_labels[repo] is None or self._mid_labels[repo] is None or self._low_labels[repo] is None:
                    print("Cannot calculate backlog inversion without high, mid and low labels")
                else:
                    if open_issues is None:
                        open_issues = read_list_from_file(f'./data/open_issues/{name}_open_issues.txt')
                    if closed_issues is None:
                        closed_issues = read_list_from_file(f'./data/closed_issues/{name}_closed_issues.txt')
                    self.calc_backlog_inversion(repo, open_issues, closed_issues, path)      

        print("Finished calculating metrics. Outputs are stored in the results folder")