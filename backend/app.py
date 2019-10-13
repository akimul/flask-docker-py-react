from flask import Flask,jsonify, request
import docker
import json
app = Flask(__name__)

client = docker.from_env()

@app.route('/')
def get_image():  
    images = client.images.list()
    res_dict, res_array = {}, []
    for image in images:
        image_obj = {
            # "attrs": image.attrs,
            "id": image.id,
            "labels": image.labels,
            "short_id": image.short_id,
            "tags": image.tags
        }
        res_array.append(image_obj)

    return jsonify(images=res_array)

@app.route('/container/run/')
def run_container():
    client = docker.from_env()
    image_id = request.args.get('image_id')
    print(image_id)
    container = client.containers.run(image_id, ports={8081:8003}, detach=True)
    return {
        "id": container.id,
        "image":container.image.id,
        "labels": container.labels,
        "short_id": container.short_id,
        "name":container.name,
        "status":container.status
    }
@app.route('/container/get/')
def get_container():
    client = docker.from_env()
    container_id = request.args.get('id')
    print(container_id)
    container = client.containers.get(container_id)
    return {
        "id": container.id,
        "image":container.image.id,
        "labels": container.labels,
        "short_id": container.short_id,
        "name":container.name,
        "status":container.status
    }

@app.route('/containers')
def get_container_list():
    client = docker.from_env()
    containers = client.containers.list()
    res_array = []
    for container in containers:
        container_obj = {
            "attrs": container.attrs,
            "id": container.id,
        "image":container.image.id,
        "labels": container.labels,
        "short_id": container.short_id,
        "name":container.name,
        "status":container.status
        }
        res_array.append(container_obj)

    return jsonify(containers=res_array)

@app.route('/container/stop/')
def stop_container():
    client = docker.from_env()
    container_id = request.args.get('id')
    print(container_id)
    container = client.containers.get(container_id)
    container.stop()
    container = client.containers.get(container_id)
    return {
        "id": container.id,
        "image":container.image.id,
        "labels": container.labels,
        "short_id": container.short_id,
        "name":container.name,
        "status":container.status
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0')