# Insurance Policy Chatbot

### Install local virtual environment for 'injection' service

Install the virtual environment for the 'injection' service by running:
`python3 -m venv injection-env`.

Activate the virtual environment by running:
`source injection-env/bin/activate`.

Install the required packages by running:
`pip install -r injection/requirements.txt`.

### Build and run the Qdrant service

When you're ready, start the vector database by running:
`docker compose up qdrant -d`.


### Create the vector database collections

First, you have to create a `.env` file inside the injection directory. Follow the `raw_env.txt` file guide.
After creating the `injection/.env` file you can load the document/vectors collections, run the following files from the `injection` directory:

1. `cd injection`
2. `python A_download_pdfs.py`
3. `python B_feature_select.py`
4. `python C_grouped_feature_select.py`
5. `python D_vdb_create.py`
6. `python E_feature_content_extraction.py`
7. `python F_final_feature.py`
8. `python G_vdb_create.py`


### Verify the collection names are correctly set in the backend_ui

The collection names have the timestamp of the last created collection. 
If you want to verify the collection names, you can do so in the `...` file.


### Build and run the Chat service

First, you have to create a `.env` file inside the backend_ui directory. Follow the `raw_env.txt` file guide.
After creating the `backend_ui/.env`y, start the chat interface by running:
`docker compose up backend_ui --build `.


### Run the app

Your application will be available at http://localhost:8000.
