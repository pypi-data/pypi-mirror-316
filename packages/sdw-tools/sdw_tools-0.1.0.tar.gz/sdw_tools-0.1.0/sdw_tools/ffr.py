from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

closure_bug = {}
closure_feature = {}

def find_dictionary(closed_issues, bug_label, feature_label):
    for issue in closed_issues:
        created_time = issue['created_at']
        closed_time = issue['closed_at']
        labels = issue['labels']
        try:
            created_time = datetime.fromisoformat(created_time[:-1])
            closed_time = datetime.fromisoformat(closed_time[:-1])
        except:
            continue
        closure_time = (closed_time - created_time).days
        for label in labels:
            if(label['name'] == bug_label):
                if(closure_bug.get(closure_time, None) is None):
                    closure_bug[closure_time] = 1
                else:
                    closure_bug[closure_time] += 1
            elif(label['name'] == feature_label):
                if(closure_feature.get(closure_time, None) is None):
                    closure_feature[closure_time] = 1
                else:
                    closure_feature[closure_time] += 1
    return closure_bug, closure_feature

def get_graph(dict, min_limit, max_limit):
    x_values = [i for i in range(min_limit, max_limit+1)]
    y_values = []
    for x in x_values:
        if(dict.get(x, None) is None):
            y_values.append(0)
        else:
            y_values.append(dict[x])
    return x_values, y_values

def get_graph_data(closed_issues, bug_label, feature_label, path=None):
    # print("Bug Label: ", bug_label)
    # print("Feature Label: ", feature_label)
    closure_bug, closure_feature = find_dictionary(closed_issues, bug_label, feature_label)
    # print("Length of closure bug: ", len(closure_bug))
    # print("Length of closure feature: ", len(closure_feature))
    min_limits = [0, 5, 30, 90]
    max_limits = [5, 30, 90, 180]
    for i in range(4):
        x_values, y_values = get_graph(closure_bug, min_limit=min_limits[i], max_limit=max_limits[i])
        total_y = sum(y_values)
        if(total_y != 0):
            y_values = [y/total_y for y in y_values]
        plt.plot(x_values, y_values, label='Bug', color='blue')
        x_values2, y_values2 = get_graph(closure_feature, min_limit=min_limits[i], max_limit=max_limits[i])
        total_y = sum(y_values2)
        if(total_y != 0):
            y_values2 = [y/total_y for y in y_values2]
        plt.plot(x_values2, y_values2, label='Feature', color='red')
        # y_values3 = [(y_values[i] + y_values2[i])/2 for i in range(len(y_values))]
        # plt.plot(x_values, y_values3, label='Average', color='green', linestyle='dashed')
        plt.xlabel('Days to close')
        plt.ylabel('Normalized frequency')
        plt.title('Frequency of closing issues')
        plt.legend()
        if(path is not None):
            os.makedirs(path, exist_ok=True)
            plt.savefig(path + "/frequency_" + str(i) + ".png")
        plt.clf()

def get_balance_ratio(issues, target_label, sprint_count, base_date):
    spill_over = []
    issues_opened = []
    issues_closed = []
    base_date = datetime.strptime(base_date, "%Y-%m-%d")
    base_date = base_date - timedelta(days=14*sprint_count)
    sprint_start_date = base_date
    sprint_end_date = sprint_start_date + timedelta(days=14)

    for sprint_num in range(sprint_count):
        issues_opened.append(0)
        issues_closed.append(0)
        for issue in issues:
            created_at = issue['created_at'][:10]
            closed_at = issue['closed_at']
            if(closed_at is not None):
                closed_at = closed_at[:10]
            labels = issue['labels']
            flag = False
            for label in labels:
                if(label['name'] == target_label):
                    flag = True
                    break
            if(flag == False):
                continue
            created_at = datetime.strptime(created_at, "%Y-%m-%d")
            if sprint_start_date <= created_at <= sprint_end_date:
                issues_opened[sprint_num] += 1
                spill_over.append(issue)
        spill_over_copy = spill_over.copy()
        for issue in spill_over_copy:
            closed_at = issue['closed_at']
            if(closed_at is not None):
                closed_at = closed_at[:10]
            created_at = issue['created_at'][:10]
            if closed_at is not None:
                closed_at = datetime.strptime(closed_at, "%Y-%m-%d")
                if sprint_start_date <= closed_at <= sprint_end_date:
                    issues_closed[sprint_num] += 1
                    spill_over.remove(issue)
        sprint_start_date = sprint_end_date
        sprint_end_date = sprint_start_date + timedelta(days=14)
    balance = [(val1/val2 if val2 != 0 else 1) for val1, val2 in zip(issues_closed, issues_opened)]
    return balance

def get_balance_graph(issues, sprint_count, base_date, bug_label, feature_label, path=None):
    bug_balance = get_balance_ratio(issues, bug_label, sprint_count, base_date)
    feature_balance = get_balance_ratio(issues, feature_label, sprint_count, base_date)
    x_values = [i for i in range(1, sprint_count+1)]
    plt.plot(x_values, bug_balance, label='Bug', color='blue')
    plt.plot(x_values, feature_balance, label='Feature', color='red')
    plt.axhline(y=1, color='black', linestyle='dashed', label='Balanced')
    plt.xlabel('Sprint number')
    plt.ylabel('Balance ratio')
    plt.title('Balance ratio of issues')
    plt.legend()
    if(path is not None):
        os.makedirs(path, exist_ok=True)
        plt.savefig(path + "/balance_ratio.png")
    plt.clf()