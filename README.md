# Insurance Policy Chatbot

### Install local virtual environment for 'injection' service

Create the virtual environment for the 'injection' service by running:

`python3 -m venv injection-env`

Activate the virtual environment by running:

`source injection-env/bin/activate`

Install the required packages by running:

`pip install -r injection/requirements.txt`

Install the spacy model for spanish language by running:

`python -m spacy download es_core_news_sm`

### Build and run the Qdrant service

When you're ready, start the vector database by running:

`docker compose up qdrant --build -d`


### Create the vector database collections

First, you have to create a `.env` file inside the injection directory. Follow the `raw_env.txt` guide.
After creating the `injection/.env` file you can load the document/vectors collections, run the following files from the `injection` directory:

1. `cd injection`
2.  `python main.py`


### Build and run the Chat service

First, you have to create a `.env` file inside the backend_ui directory. Follow the `raw_env.txt` guide.
After creating the `backend_ui/.env` file you can deploy the service container by running:

`docker compose up backend_ui --build -d`



### Run the app

Your application will be available at http://localhost:8000.
