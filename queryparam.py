from enum import Enum
from typing import List, Union
from typing import Annotated

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class QueryParams(BaseModel):
    skip: int = 0
    limit: int = 10


@app.get("/testing_query_param1")
def testing_1st_way(skip: int = 0, limit: int = 10):
    """
    Query parameter and the type annotation
    :return:
    """
    print("here sis a ", skip, ",,,,", limit)
    return {"skip": skip, "limit": limit}


@app.get("/testing_query_param2")
def testing_2nd_way(skip: int = Query(0, title="query_test", alias="sk"),
                    limit: int = Query(10, title="limir query", description="Limit the number of items returned")):
    return {"skip": skip, "limit": limit}


@app.get("/testing_query_param3_required")
def testing_2nd_way(skip: int, limit: int = Query()):
    return {"skip": skip, "limit": limit}


@app.get("/testing_query_param4_list")
def testing_2nd_way(q: List[str] = Query(None)):
    return {"q": q}


@app.get("/testing_query_param5_dict")
def testing_2nd_way(q: dict = {"skip": 0, "limit": 10}):
    """
    it doesn't work for now

    """
    return {"q": q}


@app.get("/testing_query_param6_enum")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/testing_query_param6_pydantic")
async def read_items(q: QueryParams = QueryParams(), q2: QueryParams = {}):
    items = [{"item_id": f"Item {i}"} for i in range(q.skip, q.skip + q.limit)]
    return {"items": items}


@app.get("/annotated_testing")
async def annotated_testing(q: Annotated[Union[str, None], Query(max_length=5)] = None):

    return {"items": q}
