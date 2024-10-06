import docker 

client = docker.from_env()
print(client)

print(client.images.list())