from fastapi import FastAPI, Request
import httpx
app = FastAPI()

SERVICE_URLS = {
    'user': 'http://user-service:8000',
    'post': 'http://post-service:8000',
    'queue': 'http://queue-service:8000',
    'networks': 'http://networks-service:8000',
    'template': 'http://template-service:8000',
    'api_posting': 'http://api-service:8000',
}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, service: str, path: str):
    if service not in SERVICE_URLS:
        return {"error": "Service not found"}

    async with httpx.AsyncClient() as client:
        url = f"{SERVICE_URLS[service]}/{path}"
        headers = {key: value for key, value in request.headers.items()}
        body = await request.body()
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body
        )
        return response.json()