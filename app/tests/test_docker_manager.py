import sys
sys.path.append('/home/darius/python/container_manager/')
from app.docker.docker_manager import Container

class ContainerTest():

    def __init__(self):
        self.container = Container()

    def check_docker_service(self):
        if self.container.is_docker_running() == True:
            print("Docker service is running")
        else:
            print("Docker service is not running")

    def search_docker_image(self):
        images = self.container.search_image("busybox")
        print(images)

    def pull_image(self):
        image = self.container.pull_image("busybox")

    def create_container(self):
        cont = self.container.create("busybox", "ls", "test2aaa")
        self.container.start(cont)
        print(dir(cont))

    def remove_container(self):
        cont = self.container.get("test2aaa")
        self.container.delete(cont)

if __name__ == '__main__':
    test = ContainerTest()
    test.check_docker_service()
    #test.search_docker_image()
    #test.pull_image()
    #test.create_container()
    test.remove_container()
