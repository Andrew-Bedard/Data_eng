""" Performance metrics script """


from locust import HttpUser, between, task

class MyWebsiteUser(HttpUser):
    wait_time = between(0.5, 5)

    @task
    def load_main(self):
        self.client.get("/")