from fastapi.testclient import TestClient
import analysis, api

def test_clean_removes_bad_rows():
    df = analysis.clean(analysis.make_data())
    assert df.score.notna().all() and df.attendance.max() <= 100

def test_summary_endpoint():
    r = TestClient(api.app).get("/summary")
    assert r.status_code == 200 and r.json()["rows"] > 250

def test_unknown_branch_404():
    assert TestClient(api.app).get("/branch/xyz").status_code == 404
