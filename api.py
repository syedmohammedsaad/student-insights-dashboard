"""FastAPI service that serves the cleaned insights. Run: uvicorn api:app --reload"""
from fastapi import FastAPI, HTTPException
import analysis

app = FastAPI(title="Student Insights API")
_df = analysis.clean(analysis.make_data())


@app.get("/summary")
def summary():
    return analysis.summarize(_df)


@app.get("/branch/{name}")
def branch(name: str):
    sub = _df[_df.branch.str.lower() == name.lower()]
    if sub.empty:
        raise HTTPException(404, "Unknown branch")
    return {"branch": name, "students": len(sub), "avg_score": round(float(sub.score.mean()), 1)}
