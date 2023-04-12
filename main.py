from typing import List

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.routing import APIRoute
from fastapi.security import (
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
import jwt
from pydantic import BaseModel
from starlette.responses import PlainTextResponse, JSONResponse
from fastapi.openapi.utils import get_openapi

# Creating an instance of Fastapi
app = FastAPI()


async def hello_world_testing(request):
    print(dir(app))
    # print(app.host())
    # print(app.state)
    # print(app.routes)
    # print(app.redoc_url)
    # print(app.servers)
    # print(app.mount)
    print(app.extra)
    return PlainTextResponse("Hello, world!")


# dummy data dict that holds the value
class Address(BaseModel):
    city: str
    state: str
    zipcode: int


class User(BaseModel):
    name: str
    email: str
    password: str
    address: Address


class User2(BaseModel):
    name: str
    email_address: str

    class Config:
        fields = {"email_address": "email"}


class User3(BaseModel):
    id: int
    name: str
    age: int = None


security = HTTPBearer()

user_validate_dict = {"user1": "123"}
items = {1: {"id": 1, "name": "testing_name"}}


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float


def get_item(id: int):
    return items.get(id, None)


# we can use union as well if value is of different type
@app.get("/get_endpoint", response_model=dict)
async def test_get(key: str = ""):
    print(dir(app))

    # print(dir(app))
    # print(">>")
    # cred: HTTPAuthorizationCredentials = Depends(security)
    # token = cred.credentials
    # return {"message": "token decoded"}
    # if not user_validate_dict.get(cred, None):
    #     raise HTTPException(status_code=403, detail="User Not Found")
    # else:
    #     password = user_validate_dict.get(cred.username)
    #     if password != cred.password:
    #         raise HTTPException(status_code=403, detail="Passowrd wrong")
    # value = data_dict.get(key, "")
    # if value:
    #     return {
    #         "data": value
    #     }
    #
    # raise HTTPException(status_code=400, detail="Item key not found")
    return {}


@app.post("/post_endpoint", response_model=dict)
async def test_post(data: dict):
    return {}


@app.post("/token_generate", response_model=dict)
async def test_post(payload: dict):
    encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256")
    # jwt.ExpiredSignatureError
    return {"data": encoded_jwt}


@app.on_event("startup")
async def test_startup_event():
    print("Startup Event is executed")


@app.on_event("shutdown")
async def test_shutdown_event():
    print("Shutdown Event is Executed")


# @app.on_event("startup_complete")
# async def test_startup_complete_event():
#     print("Shutdown Event is Executed")
#
#
# @app.on_event("shutdown_complete")
# async def test_shutdown_complete_event():
#     print("Shutdown Event is Executed")
@app.api_route("/test_api_route", methods=["GET", "POST"])
async def testing_api_route():
    print("kuch nhi")


@app.api_route(
    "/items/{item_id}",
    responses={
        200: {"description": "Successful Response", "model": Item},
        404: {"description": "Item not found1"},
    },
    operation_id="getting_the_item",
)
async def read_item(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404)
    return item


@app.get("/items/", response_model=List[Item], response_model_include={"name", "price"})
async def read_items():
    items = [
        Item(id=2, name="Foo", description="The pretender", price=42.0),
        Item(id=3, name="Bar", description="The bartender", price=24.0),
    ]
    return items


#
# @app.api_route("/users/{user_id}", response_model=User, response_model_exclude={"address": {"zipcode"}})
# async def get_user(user_id: int) -> User:
#     address = Address(city="New York", state="NY", zipcode="12345")
#     user = User(name="John Doe", email="john.doe@example.com", password="secret", address=address)
#     return user


# @app.get("/users/{user_id}", response_model=User2, response_model_by_alias=True)
# async def get_user(user_id: int):
#     return {"name": "John Doe", "email": "john.doe@example.com"}

# @app.get("/users/{user_id}")
# async def read_user(user_id: int):
#     return {"id": user_id, "name": "John Doe", "age": None}

# Here all attribute is applicable that is applicable for api_route
# app.add_api_route("/", my_handler, response_class=JSONResponse)


@app.get("/users/{user_id}", response_model_exclude_unset=True)
async def read_user(user_id: int):
    return {"id": user_id, "name": "John Doe"}


@app.get("/hello", response_class=PlainTextResponse)
async def hello_world():
    return "Hello, world!"


# custom_route = APIRoute("/route_add", endpoint=hello_world, methods=["GET"])
# print(**custom_route.__dict__)
app.add_route("/test_route", hello_world_testing)


# app = FastAPI(
#     title="My API",
#     openapi_tags=[
#         {
#             "name": "users",
#             "description": "Operations related to users",
#             "externalDocs": {
#                 "description": "Find more info here",
#                 "url": "https://example.com",
#             },
#             "servers": [
#                 {
#                     "url": "http://localhost:8000",
#                     "description": "Local server",
#                 },
#                 {
#                     "url": "https://api.example.com/v1",
#                     "description": "Production server",
#                 },
#             ],
#         }
#     ]
# )
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Custom title",
#         version="2.5.0",
#         description="This is a custom description",
#         routes=app.routes,
#     )
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# mount the Starlette application under the "/starlette" path
# app.mount("/starlette", starlette_app)
