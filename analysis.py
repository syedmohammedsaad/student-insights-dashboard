"""Generate a sample student-performance dataset, clean it with pandas, and export insights."""
import json
import numpy as np
import pandas as pd


def make_data(n=300, seed=7):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "branch": rng.choice(["CSE-DS", "CSE", "ISE", "ECE", "ME"], n),
        "study_hours": rng.normal(14, 5, n).round(1),
        "attendance": rng.normal(82, 10, n).round(1),
    })
    df["score"] = (35 + 2.2 * df.study_hours + 0.25 * df.attendance + rng.normal(0, 6, n)).round(1)
    # add a few dirty rows on purpose so the cleaning step is real
    df.loc[rng.choice(n, 8, replace=False), "score"] = np.nan
    df.loc[rng.choice(n, 4, replace=False), "attendance"] = 140
    return df


def clean(df):
    df = df.dropna(subset=["score"]).copy()
    df = df[(df.attendance.between(0, 100)) & (df.study_hours >= 0)]
    df["score"] = df.score.clip(0, 100)
    return df.reset_index(drop=True)


def summarize(df):
    by_branch = df.groupby("branch").score.mean().round(1).sort_values(ascending=False)
    hist, edges = np.histogram(df.score, bins=[0, 40, 50, 60, 70, 80, 90, 100])
    return {
        "rows": int(len(df)),
        "avg_score": round(float(df.score.mean()), 1),
        "corr_study_score": round(float(df.study_hours.corr(df.score)), 2),
        "corr_attendance_score": round(float(df.attendance.corr(df.score)), 2),
        "by_branch": {k: float(v) for k, v in by_branch.items()},
        "distribution": {f"{int(a)}-{int(b)}": int(c) for a, b, c in zip(edges[:-1], edges[1:], hist)},
    }


if __name__ == "__main__":
    raw = make_data(); df = clean(raw)
    s = summarize(df); s["dropped_rows"] = int(len(raw) - len(df))
    json.dump(s, open("data.json", "w"), indent=2)
    html = open("template.html", encoding="utf-8").read().replace("__DATA__", json.dumps(s))
    open("dashboard.html", "w", encoding="utf-8").write(html)
    print("rows kept:", s["rows"], "dropped:", s["dropped_rows"])
