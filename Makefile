
CONDA_ENV = backend_challenge-insightwise

start: 
	uvicorn app.main:app --reload

start_mongo:
	sudo systemctl start mongod

stop_mongo:
	sudo systemctl stop mongod

test:
	pytest --cov=app tests/

clean-env:
	conda env remove -n $(CONDA_ENV)

export-env: 
	conda env export > environment.yml