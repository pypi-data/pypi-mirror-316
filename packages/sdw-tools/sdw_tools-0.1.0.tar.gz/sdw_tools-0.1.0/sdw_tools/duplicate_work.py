from datetime import datetime

def calculate_duplicate_work(closed_prs, base_date = None):
    unmerged_prs = []
    merged_prs = []
    if base_date is not None:
        base_date = datetime.strptime(base_date, "%Y-%m-%d")
    for closed_pr in closed_prs:
        closed_at = closed_pr['closed_at'][:10]
        closed_at = datetime.strptime(closed_at, "%Y-%m-%d")
        if base_date is None or base_date <= closed_at:
            if closed_pr['merged_at'] is not None:
                merged_prs.append(closed_pr)
            else:
                unmerged_prs.append(closed_pr)
    duplicate_work = len(unmerged_prs) / len(merged_prs)
    return len(unmerged_prs), len(merged_prs), duplicate_work

