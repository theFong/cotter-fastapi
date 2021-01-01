import os
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
import fastapi

api_key = os.getenv("COTTER_API_KEY")
if api_key is None:
    raise RuntimeError("COTTER_API_KEY env var not set")

oauth_config = {
    "additionalQueryStringParams": {
        "type": "EMAIL",
        "api_key": api_key,
        "redirect_url": "http://localhost:8000/docs/oauth2-redirect"
    },
    "usePkceWithAuthorizationCodeGrant": True,  # PKCE
    "clientId": api_key,
}

app = fastapi.FastAPI(swagger_ui_init_oauth=oauth_config)

auth_code = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://js.cotter.app/app",
    tokenUrl="https://www.cotter.app/api/v0/verify/get_identity",
    refreshUrl=f"https://www.cotter.app/api/v0/token/{api_key}",
)


@app.get("/hello")
def hello(token: str = Depends(auth_code)):
    print(token)
    return "hello"