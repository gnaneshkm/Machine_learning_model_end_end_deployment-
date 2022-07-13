Install packages: `pip install -r requirements.txt`

Create/Activate an virtual environment: $ `. venv/bin/activate`

Deactivate the virtual environment: $ `. venv/bin/deactivate`

Run the flask app: $ `flask run`

Docker build command: `docker build -t docker.prediction.com:latest .`

Docker run command: `docker run -d -p 8081:5000 --name=prediction-app docker.prediction.com:latest`

Docker stop: `docker stop prediction-app`

Docker prune: `docker prune prediction-app`