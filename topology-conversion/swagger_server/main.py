import requests
import logging
import connexion
import uvicorn
from flask import render_template
from convert_topology import ParseConvertTopology

logger = logging.getLogger(__name__)

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yaml")

# Run swagger service
def main():
    app = connexion.App(__name__, specification_dir="./swagger/")
    # app.app.json_encoder = encoder.JSONEncoder
    app.add_api("swagger.yaml", arguments={"title": "OXPO API Wrapper"}, pythonic_params=True)

        
if __name__ == "__main__":
    main()
#    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)        
