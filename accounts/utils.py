from rest_framework.response import Response

class SetCookiesUtil:
    refresh_token_lifetime = 60 * 60 * 24

    def set_refresh_cookie(self, response: Response, refresh: str):
        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=self.refresh_token_lifetime,
            path="/api/accounts/",
        )


    def clear_refresh_cookie(self, response: Response):
        response.delete_cookie("refresh_token", path="/api/accounts/")