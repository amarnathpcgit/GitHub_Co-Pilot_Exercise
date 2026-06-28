from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert expected_activity in json_data
    assert json_data[expected_activity]["description"] == activities[expected_activity]["description"]


def test_signup_for_existing_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "test-signup@mergington.edu"
    encoded_name = quote(activity_name)

    # Act
    response = client.post(f"/activities/{encoded_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "missing@mergington.edu"
    encoded_name = quote(activity_name)

    # Act
    response = client.post(f"/activities/{encoded_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
