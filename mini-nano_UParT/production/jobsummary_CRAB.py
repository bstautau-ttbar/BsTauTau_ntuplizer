#!/usr/bin/env python3
"""
Usage: python jobsummary_CRAB.py <crab_projects_dir>
    -> status.csv in <crab_projects_dir>, one row per CRAB task
"""
import csv
import glob, os, sys

from CRABAPI.RawCommand import crabCommand


PENDING     = ("idle", "running", "transferring", "transferred", "cooloff")
HEADER      = ["task", "total", "finished", "failed", "unsubmitted", "in_progress", "other", "frac_finished", "frac_failed"]


def summarize(task_dir):
    j = crabCommand("status", dir=task_dir).get("jobsPerStatus", {})
    
    total       = sum(j.values())
    finished    = j.get("finished", 0)
    frac_finished = round(finished / total, 4) if total else 0.0
    failed      = j.get("failed", 0)
    frac_failed = round(failed / total, 4) if total else 0.0
    unsubmitted = j.get("unsubmitted", 0)
    in_progress = sum(j.get(k, 0) for k in PENDING)
    
    other = total - finished - failed - unsubmitted - in_progress
    if other:
        extra = {k: v for k, v in j.items() if k not in PENDING + ("finished", "failed", "unsubmitted")}
        print(f"Note: {os.path.basename(task_dir)} has {other} jobs in other states: {extra}")
    
    return [total, finished, failed, unsubmitted, in_progress, other, frac_finished, frac_failed]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    crabdir = sys.argv[1]
    if not os.path.isdir(crabdir):
        print(f"Error: {crabdir} is not a directory")
        sys.exit(1)

    task_dirs = sorted(glob.glob(os.path.join(crabdir, "crab_*")))
    if not task_dirs:
        print(f"Error: no crab_* directories found in {crabdir}")
        sys.exit(1)

    rows = []
    for d in task_dirs:
        name = os.path.basename(d)
        try:
            rows.append([name] + summarize(d))
        except Exception as e:  # keep going if one task fails
            print(f"Error: could not get status for {name}: {e}")

    out_csv = os.path.join(crabdir, "status.csv")
    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)

    print(f"\n---- summary of {len(rows)}/{len(task_dirs)} tasks written to {out_csv} ----")


if __name__ == "__main__":
    main()