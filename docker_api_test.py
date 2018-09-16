import docker

client = docker.from_env()
try:
    #print(client.containers.run("alpine", ["echo", "hello", "world"]))
    container = client.containers.run("bfirsh/reticulate-splines", detach=True)
    print(container.id)
except docker.errors.ContainerError as e:
    print("1")
except docker.errors.ImageNotFound as e:
    print("2")
except docker.errors.APIError as e:
    print("3")
except docker.errors.DockerException as e:
    print(e)
else:
    print("dsadsadsa")
