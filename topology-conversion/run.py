from connexion import AsyncApp

app = AsyncApp(__name__, specification_dir="./swagger/")
# app = AsyncApp(__name__)
app.add_api(
    "swagger.yaml", arguments={"title": "OXPO API Wrapper"}, pythonic_params=True
)

if __name__ == "__main__":
    app.run()
