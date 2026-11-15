
import os
from uuid import uuid4

from locust import HttpUser, task, between
from locust.exception import StopUser


class WorkFlowUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        username = os.getenv("WORKFLOW_USERNAME")
        password = os.getenv("WORKFLOW_PASSWORD")

        if not username or not password:
            print("Login failed: missing WORKFLOW_USERNAME or WORKFLOW_PASSWORD")
            raise StopUser()

        response = self.client.post(
            "/users/login/",
            data={
                "username": username,
                "password": password,
            },
            name="/users/login/",
        )

        if response.status_code != 200:
            print(
                "Login failed:",
                response.status_code,
                response.text,
            )
            raise StopUser()

        access_token = response.json().get("access_token")

        if not access_token:
            print("Login failed: access_token missing from response")
            raise StopUser()

        self.client.headers.update(
            {"Authorization": f"Bearer {access_token}"}
        )
        print("Locust user authenticated successfully")

        self.project_id = None

    @task(4)
    def check_projects(self):
        self.client.get("/projects/")

    @task(2)
    def create_project(self):
        response = self.client.post(
            "/projects/",
            json={
                "name": f"Load Test Project {uuid4().hex[:8]}",
                "description": "Project created during Locust load testing",
            },
            name="/projects/",
        )

        if response.status_code in (200, 201):
            self.project_id = response.json().get("id")
        else:
            print(
                "Project creation failed:",
                response.status_code,
                response.text,
            )

    @task(3)
    def create_task(self):
        if self.project_id is None:
            return

        response = self.client.post(
            f"/projects/{self.project_id}/tasks/",
            json={
                "title": f"Load Test Task {uuid4().hex[:8]}",
                "description": "Task created during Locust load testing",
                "assigned_to": 1,
                "status": "todo",
                "priority": "medium",
                "estimated_hours": 1,
            },
            name="/projects/[project_id]/tasks/",
        )

        if response.status_code not in (200, 201):
            print(
                "Task creation failed:",
                response.status_code,
                response.text,
            )

    @task(3)
    def get_tasks(self):
        if self.project_id is None:
            return

        self.client.get(
            f"/projects/{self.project_id}/tasks/",
            name="/projects/[project_id]/tasks/",
        )
