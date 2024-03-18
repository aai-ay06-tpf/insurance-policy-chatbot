# Insurance Policy Chatbot

### Install local virtual environment for 'injection' service

Install the virtual environment for the 'injection' service by running:
`python3 -m venv injection-env`.

Activate the virtual environment by running:
`source injection-env/bin/activate`.

Install the required packages by running:
`pip install -r injection/requirements.txt`.

### Building and running the application

When you're ready, start your application by running:
`docker compose up --build`.


### Create the vector database

To create the vector database, run the following files from the `injection` directory:
1. `python A_download_pdfs.py`
2. `python B_feature_select.py`
3. `python C_grouped_feature_select.py`
4. `python D_vdb_create.py`
5. `python feature_content_extraction.py`
6. `python feature_content.py`
7. `python vdb_create.py`


### Verify the collection names are correctly set in the backend_ui

The collection names have the timestamp of the last created collection. 
If you want to verify the collection names, you can do so in the `...` file.

### Run the app

Your application will be available at http://localhost:8000.
