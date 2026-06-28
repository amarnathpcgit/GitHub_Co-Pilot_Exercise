from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_from_activity():
    activity_name = "Chess Club"
    email = "unregister-test@mergington.edu"
    encoded_name = quote(activity_name)

    signup_response = client.post(f"/activities/{encoded_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.post(f"/activities/{encoded_name}/unregister?email={email}")
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200

    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]
