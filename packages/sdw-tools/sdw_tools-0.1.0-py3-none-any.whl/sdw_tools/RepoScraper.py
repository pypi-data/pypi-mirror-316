"""
This module contains the class RepoScraper which is used to scrape repositories from GitHub.
"""
import requests
from utils import write_list_to_file
import os

class RepoScraper:
    """
    Class to scrape repositories from GitHub
    __init__ method initializes the RepoScraper object with the following parameters:
    owners: list of owners of the repositories to scrape
    repos: list of repositories to scrape
    primary_token: GitHub token to use for scraping
    backup_token: GitHub token to use if the primary token is rate limited (default=None)
    """
    def __init__(self, owners, repos, primary_token, backup_token=None):
        if type(owners) is str:
            owners = [owners]
        if type(repos) is str:
            repos = [repos]
        if primary_token is None:
            raise ValueError("\033[31mPrimary token can not be None\033[0m")
        self._owners = owners
        self._repos = repos
        self._primary_token = primary_token
        self._backup_token = backup_token
        self._what_to_scrape = None
        self._map = {
            "open_issues": self.get_open_issues_PRs,
            "closed_issues": self.get_closed_issues_PRs,
            "forks": self.get_all_forks,
            "open_PRs": self.get_open_PRs,
            "closed_PRs": self.get_closed_PRs
        }
        self._prefix_names = []
        self.set_prefix_names()
    
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
        self.set_prefix_names()

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
        self.set_prefix_names()

    @property
    def primary_token(self):
        print("Can not return primary_token due to security reasons")
    
    @primary_token.setter
    def primary_token(self, primary_token):
        try: 
            if primary_token is None:
                raise ValueError("Primary token can not be None")
            self._primary_token = primary_token
        except ValueError as e:
            print(f"\033[31m{e}\033[0m")
    
    @property
    def backup_token(self):
        print("Can not return backup_token due to security reasons")

    @backup_token.setter
    def backup_token(self, backup_token):
        self._backup_token = backup_token
    
    @property
    def what_to_scrape(self):
        return self._what_to_scrape
    @what_to_scrape.setter
    def what_to_scrape(self, what_to_scrape):
        if what_to_scrape is None:
            self._what_to_scrape = None
        else:
            print("Can not set what_to_scrape directly to a value other than None")
        
    @property
    def map(self):
        print("Can not get map")
    
    @map.setter
    def map(self, map):
        print("Can not set map")
    
    @property
    def prefix_names(self):
        if(len(self._prefix_names) == 1):
            return self._prefix_names[0]
        return self._prefix_names

    @prefix_names.setter
    def prefix_names(self, prefix_names):
        print("Can not set prefix_names directly")

    def set_prefix_names(self):
        self._prefix_names = []
        for owner, repo in zip(self._owners, self._repos):
            owner = ''.join(e for e in owner if e.isalnum())
            repo = ''.join(e for e in repo if e.isalnum())
            self._prefix_names.append(f"{owner}_{repo}")
    
    def add_for_scraping(self, to_scrape):
        if type(to_scrape) is str:
            to_scrape = [to_scrape]
        # Check if the user wants to scrape everything
        if "all" in to_scrape:
            self._what_to_scrape = list(self._map.keys())
            return
        
        # Check whether the values in to_scrape are valid
        for item in to_scrape:
            if item not in self._map.keys():
                print(f"\033[31m{item} is not a valid value to scrape\033[0m")
                return
        
        # Check if the values in to_scrape are already in the list and add them if they are not
        if self._what_to_scrape is None:
            self._what_to_scrape = []
        for item in to_scrape:
            if item not in self._what_to_scrape:
                self._what_to_scrape.append(item)
            else:
                print(f"\033[31m{item} is already in the list\033[0m")

    def get_open_issues_PRs(self, owner, repo):
        base_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self._primary_token:
            headers["Authorization"] = f"Bearer {self._primary_token}"
        params = {
            "state": "open",
            "per_page": 100,  # Adjust as needed
        }
        open_issues = []
        url = base_url
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                issues = response.json()
                open_issues.extend(issues)
                url = response.links.get("next", {}).get("url")
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                break
        return open_issues
    
    def get_closed_issues_PRs(self, owner, repo):
        base_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self._primary_token:
            headers["Authorization"] = f"Bearer {self._primary_token}"
        params = {
            "state": "closed",
            "per_page": 100,  # Adjust as needed
        }
        closed_issues = []
        url = base_url
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                closed = response.json()
                closed_issues.extend(closed)
                url = response.links.get("next", {}).get("url")
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                break
        return closed_issues

    def get_all_forks(self, owner, repo):
        base_url = f"https://api.github.com/repos/{owner}/{repo}/forks"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self._primary_token:
            headers["Authorization"] = f"Bearer {self._primary_token}"
        params = {
            "per_page": 100,  # Adjust as needed
        }
        all_forks = []
        url = base_url
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                forked = response.json()
                all_forks.extend(forked)
                url = response.links.get("next", {}).get("url")
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                break
        return all_forks

    def get_open_PRs(self, owner, repo):
        base_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self._primary_token:
            headers["Authorization"] = f"Bearer {self._primary_token}"
        params = {
            "state": "open",
            "per_page": 100,  # Adjust as needed
        }
        closed_issues = []
        url = base_url
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                closed = response.json()
                closed_issues.extend(closed)
                url = response.links.get("next", {}).get("url")
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                break
        return closed_issues
    
    def get_closed_PRs(self, owner, repo):
        base_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self._primary_token:
            headers["Authorization"] = f"Bearer {self._primary_token}"
        params = {
            "state": "closed",
            "per_page": 100,  # Adjust as needed
        }
        closed_issues = []
        url = base_url
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                closed = response.json()
                closed_issues.extend(closed)
                url = response.links.get("next", {}).get("url")
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                break
        return closed_issues
    
    def get_repo_data(self, owner, repo):
        base_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self._primary_token:
            headers["Authorization"] = f"Bearer {self._primary_token}"
        params = {
            "per_page": 100,  # Adjust as needed
        }
        url = base_url
        
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                repo_info = response.json()
                return repo_info
            else:
                print(f"Error: {response.status_code}")
                return None
    
    def scrape(self):
        if self._what_to_scrape is None:
            print("\033[31mNothing set for scraping so scraping everything\033[0m")
            self.add_for_scraping("all")
        print("Getting basic repo details...")
        repo_details = []
        for owner, repo, name in zip(self._owners, self._repos, self._prefix_names):
            repo_details.append(self.get_repo_data(owner, repo))
        print("Writing basic repo details to file...")            
        write_list_to_file("./data/repo_details.txt", repo_details)
        skip_all = None
        for item in self._what_to_scrape:
            print(f"\033[32mScraping {item}\033[0m")
            for owner, repo, name in zip(self._owners, self._repos, self._prefix_names):
                if(not os.path.exists(f"./data/{item}/{name}_{item}.txt")):
                    print(f"Getting {item} for {owner}/{repo}")
                    write_list_to_file(f"./data/{item}/{name}_{item}.txt", self._map[item](owner, repo))
                else:
                    if(skip_all is None):
                        print(f"\033[32m{item} for {owner}/{repo} already exist. Do you want to skip instead?\033[0m")
                        print(f"\033[32m[Y]: Yes (Skip)    [N]: No (Overwrite)    [A]: Skip all that exist    [X]: Overwrite all \033[0m")
                        skip = input()
                    elif(skip_all):
                        skip = 'y'
                    else:
                        skip = 'n'
                    if(skip.lower() == 'y' or skip.lower() == 'a'):
                        print(f"Skipping {item} for {owner}/{repo}")
                        if(skip.lower() == 'a'):
                            skip_all = True
                    else:
                        print(f"Getting {item} for {owner}/{repo}")
                        write_list_to_file(f"./data/{item}/{name}_{item}.txt", self._map[item](owner, repo))
                        if(skip.lower() == 'x'):
                            skip_all = False