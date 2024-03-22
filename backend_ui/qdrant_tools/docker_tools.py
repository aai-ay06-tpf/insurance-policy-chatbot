import json
import http.client

from utils.config import QDRANT_HOST, QDRANT_PORT


def obtain_collections(host: str = QDRANT_HOST, port: str = QDRANT_PORT) -> list:
    try:
        # Create a connection to your Qdrant instance
        conn = http.client.HTTPConnection(host, port)

        # Make a GET request to the Qdrant API
        conn.request("GET", "/collections")

        # Get the response
        response = conn.getresponse()

        # If the request was successful, decode the response and extract the collection names
        if response.status == 200:
            # Decode the response to text
            response_text = response.read().decode()

            # Convert the text to a dictionary
            response_dict = json.loads(response_text)

            # Extract the collections from the dictionary
            collections = response_dict["result"]["collections"]

            # Return the collection names
            return [collection["name"] for collection in collections]
        else:
            return None

    except Exception as e:
        print(
            f"Error obtaining collections from Qdrant in {__name__}.obtain_collections()"
        )
        print(e)
        return None
