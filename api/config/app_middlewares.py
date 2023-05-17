from starlette.requests import Request
from starlette.responses import Response
# from edf_re_aos_api.models.blacklisted_tokens import BlacklistedTokens


def get_token(headers):
    return headers["Authorization"].replace("Bearer", "").replace("JWT", "").strip()


async def headers_middleware(request: Request, call_next):
	response = await call_next(request)
	response.headers["Cache-Control"] = "no-store"
	response.headers["Content-Security-Policy"] = "default-src 'self'"
	response.headers["X-Frame-Options"] = "deny"
	response.headers["X-Content-Type-Options"] = "nosniff"

	return response


async def jwt_middleware(request: Request, call_next):
  if "Authorization" not in request.headers or "auth" in str(request.url.path):
    return await call_next(request)
  token = get_token(request.headers)

  if BlacklistedTokens.objects(token=token).first():
    return Response("JWT Token Invalid", status_code=401)
  return await call_next(request)
