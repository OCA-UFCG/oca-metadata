PORT = 8501
IMAGE_NAME = ocaufcg/oca-metadata
CONTAINER_NAME = oca-metadata

run-dev:
	streamlit run ./src/app.py --server.port $(PORT) 

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run --name $(CONTAINER_NAME) -p $(PORT):$(PORT) -d $(IMAGE_NAME)
