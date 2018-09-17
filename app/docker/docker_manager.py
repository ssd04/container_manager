import docker
import psutil


class DockerManager:

    def __init__(self):
        self.client = docker.from_env()

    def runContainer(self, container_name):
        print(client.containers.run("alpine", ["echo", "hello", "world"], name = container_name))

    def runContainerDetach(self, container_name):
        client.containers.run("alpine", ["echo", "hello", "world"], name = container_name, detach = True)


class Container:

    def __init__(self):
        self.client = docker.from_env()
        pass

    def is_docker_running(self):
        for process in psutil.process_iter():
            if "docker" in process.name():
                return True
        return False

    def create(self, image, command, container_name):
        ''' Create a container without starting it. Returns a container object. '''
        try:
            container = self.client.containers.create(image, command, name=container_name)
            return container
        except docker.errors.ImageNotFound as e:
            print("WARN: Image not found.")
        except docker.errors.APIError as e:
            print(e)

    def delete(self, container):
        try:
            container.remove()
        except docker.errors.APIError as e:
            print(e)

    def get(self, container_identifier):
        ''' Get a container by name or container_id. Returns a container object. '''
        try:
            container = self.client.containers.get(container_identifier)
            return container
        except docker.errors.NotFound as e:
            print("WARN: The specified contained does not exist.")
        except docker.errors.APIError as e:
            print(e)

    def start(self, container):
        try:
            container.start()
        except docker.errors.APIError as e:
            print(e)

    def stop(self, container):
        try:
            container.stop()
        except docker.errors.APIError as e:
            print(e)

    def search_image(self, image_name):
        ''' Search docker image by pattern. Return image name. '''
        images = self.client.images.search(image_name)
        for image in images:
            if image['is_official'] == True:
                return image['name']
        return images[0]['name']

    def pull_image(self, name):
        ''' Pull image based on given name. '''
        image_name = self.search_image(name)
        image = self.client.images.pull(image_name, tag="latest")
        return image
