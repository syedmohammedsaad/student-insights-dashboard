# Student Insights Dashboard
Cleans a sample student-performance dataset with pandas, serves it through a FastAPI service, and shows the results on a static dashboard.
The data is synthetic and generated in `analysis.py` (with a few deliberately dirty rows to demonstrate cleaning).

    pip install -r requirements.txt
    python analysis.py      # rebuilds data.json and dashboard.html
    pytest
    uvicorn api:app --reload   # then open /summary or /docs

Live dashboard: https://syedmohammedsaad.github.io/student-insights-dashboard/
