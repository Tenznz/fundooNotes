import jwt


class EncodeDecodeToken:

    @staticmethod
    def encode_token(payload):
        jwt_encoded = jwt.encode({"id": payload},
                                 "secret",
                                 algorithm="HS256"
                                 )
        encoded_token = jwt_encoded.decode('UTF-8')
        return encoded_token

    @staticmethod
    def decode_token(token):
        decoded_token = jwt.decode(
            token,
            "secret",
            algorithms=["HS256"]
        )

        # print(decoded_token)
        return decoded_token
