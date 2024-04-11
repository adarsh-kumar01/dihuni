from flask import Flask, render_template, request
import docker

#client = docker.from_env()

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    deep_learning_framework = request.form['deep_learning_framework']
    os_version = request.form['os_version']
    interface = request.form['interface']

    # Mapping user selections to Docker image names
    docker_image_map = {
        ('pytorch', '22.04', 'jupyter_lab'): 'pytorch-22.04-jupyter',
        ('pytorch', '22.04', 'vscode'): 'pytorch-22.04-vscode',
        ('pytorch', '20.04', 'jupyter_lab'): 'pytorch-20.04-jupyter',
        ('pytorch', '20.04', 'vscode'): 'pytorch-20.04-vscode',
        ('tensorflow', '22.04', 'jupyter_lab'): 'tensorflow-22.04-jupyter',
        ('tensorflow', '22.04', 'vscode'): 'tensorflow-22.04-vscode',
        ('tensorflow', '20.04', 'jupyter_lab'): 'tensorflow-20.04-jupyter',
        ('tensorflow', '20.04', 'vscode'): 'tensorflow-20.04-vscode',
    }

    docker_image = docker_image_map.get((deep_learning_framework, os_version, interface))

    if docker_image:
        try:
            # Pull Docker image from Docker Hub
            client.images.pull('your_docker_hub_username/' + docker_image)
            return f'Success: Docker image "{docker_image}" pulled successfully.'
        except docker.errors.APIError as e:
            return f'Error: Failed to pull Docker image "{docker_image}": {e}'
    else:
        return 'Error: No matching Docker image found for the selected options.'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8888",debug=True)
