import jwt


class EncodeDecodeToken:

    @staticmethod
    def encode_token(payload):
        jwt_encoded = jwt.encode({"id": payload},
                                 "secret",
                                 algorithm="HS256"
                                 )
        return jwt_encoded

    @staticmethod
    def decode_token(token):
        decoded_token = jwt.decode(
            token,
            "secret",
            algorithms=["HS256"]
        )

        # print(decoded_token)
        return decoded_token
