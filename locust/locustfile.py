
from locust import HttpUser, task, between
import os


class WorkFlowUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "/users/login/",
            data={
                "username": os.getenv("WORKFLOW_USERNAME"),
                "password": os.getenv("WORKFLOW_PASSWORD"),
            },
        )

        if response.status_code != 200:
            print("Login failed:", response.status_code, response.text)
            return

        access_token = response.json()["access_token"]
        self.client.headers.update(
            {"Authorization": f"Bearer {access_token}"}
        )

    @task
    def check_projects(self):
        self.client.get("/projects/")
