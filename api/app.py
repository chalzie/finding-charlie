from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get('/api/v1')
async def root():
    return {'message': 'Hello World!'}


@app.get('/api/v1/outposts')
async def get_outposts():
    return {'outposts': ''}


@app.get('/api/v1/outposts/{outpost_id}')
async def get_outpost(outpost_id: str, q: Union[str, None]):
    return {'id': id, 'q': q}
