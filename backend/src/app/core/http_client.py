from typing import Annotated

import httpx
from fastapi import Depends, Request


def get_http_client(request: Request) -> httpx.AsyncClient:
    """The app-wide client opened in main.lifespan. Reusing one client keeps
    connections pooled across requests."""
    client: httpx.AsyncClient = request.app.state.http_client
    return client


# Add `client: HttpClientDep` to a route to call another service:
#     response = await client.get("https://example.com/api")
HttpClientDep = Annotated[httpx.AsyncClient, Depends(get_http_client)]
