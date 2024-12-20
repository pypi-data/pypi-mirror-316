from datetime import datetime, timedelta
import numpy as np

def get_sorted_issues(issues, high_label, mid_label, low_label):
    high = []
    mid = []
    low = []
    for issue in issues:
        label = None
        for label in issue['labels']:
            if label['name'] == high_label:
                high.append(issue)
                break
            elif label['name'] == mid_label:
                mid.append(issue)
                break
            elif label['name'] == low_label:
                low.append(issue)
                break
    return high, mid, low
    
def get_inversion(issues, high_label, mid_label, low_label):
    high, mid, low = get_sorted_issues(issues, high_label, mid_label, low_label)
    hl_inversion = 0
    hm_inversion = 0
    ml_inversion = 0
    for low_issue in low:
        for mid_issue in mid:
            if low_issue['closed_at'] is not None:
                low_issue_closed_at = datetime.fromisoformat(low_issue['closed_at'][:-1])
                if mid_issue['created_at'] is not None:
                    mid_issue_created_at = datetime.fromisoformat(mid_issue['created_at'][:-1])
                else:
                    print("Bad for model")
                    continue
                if mid_issue_created_at < low_issue_closed_at:
                    if mid_issue['closed_at'] is None:
                        ml_inversion += 1
                        continue
                    mid_issue_closed_at = datetime.fromisoformat(mid_issue['closed_at'][:-1])
                    if mid_issue_closed_at > low_issue_closed_at:
                        ml_inversion += 1
    
    for low_issue in low:
        for high_issue in high:
            if low_issue['closed_at'] is not None:
                low_issue_closed_at = datetime.fromisoformat(low_issue['closed_at'][:-1])
                if high_issue['created_at'] is not None:
                    high_issue_created_at = datetime.fromisoformat(high_issue['created_at'][:-1])
                else:
                    print("Bad for model")
                    continue
                if high_issue_created_at < low_issue_closed_at:
                    if high_issue['closed_at'] is None:
                        hl_inversion += 1
                        continue
                    high_issue_closed_at = datetime.fromisoformat(high_issue['closed_at'][:-1])
                    if high_issue_closed_at > low_issue_closed_at:
                        hl_inversion += 1
    
    for mid_issue in mid:
        for high_issue in high:
            if mid_issue['closed_at'] is not None:
                mid_issue_closed_at = datetime.fromisoformat(mid_issue['closed_at'][:-1])
                if high_issue['created_at'] is not None:
                    high_issue_created_at = datetime.fromisoformat(high_issue['created_at'][:-1])
                else:
                    print("Bad for model")
                    continue
                if high_issue_created_at < mid_issue_closed_at:
                    if high_issue['closed_at'] is None:
                        hm_inversion += 1
                        continue
                    high_issue_closed_at = datetime.fromisoformat(high_issue['closed_at'][:-1])
                    if high_issue_closed_at > mid_issue_closed_at:
                        hm_inversion += 1
    
    return hl_inversion, hm_inversion, ml_inversion
        
        