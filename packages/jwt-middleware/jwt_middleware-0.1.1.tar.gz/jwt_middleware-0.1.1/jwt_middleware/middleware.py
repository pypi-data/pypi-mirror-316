from fastapi import Request, HTTPException
import jwt

class JWTMiddleware:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def __call__(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing token")
        try:
            # Decode the JWT token
            decoded_token = jwt.decode(token.split(" ")[1], self.secret_key, algorithms=[self.algorithm])
            
            # Extract user_id from the token payload
            user_id = decoded_token.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: user_id not found")
            
            # Attach user_id to the request state for downstream usage
            request.state.user_id = user_id

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        response = await call_next(request)
        return response