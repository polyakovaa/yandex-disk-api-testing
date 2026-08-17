class Headers:
    AUTHORIZATION = "Authorization"
    OAUTH_PREFIX = "OAuth"

    @classmethod
    def default(cls, oauth_token: str) -> dict:
        return {
            cls.AUTHORIZATION: f"{cls.OAUTH_PREFIX} {oauth_token}",
        }
