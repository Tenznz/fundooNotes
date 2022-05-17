import jwt


class EncodeDecodeToken:
    """ Encode and decode jwt token """
    @staticmethod
    def encode_token(payload):
        """
         this method is use for encode to jwt token
        :param payload:
        :return:response
        """
        jwt_encoded = jwt.encode({"id": payload},
                                 "secret",
                                 algorithm="HS256"
                                 )
        # encoded_token = jwt_encoded.decode('UTF-8')
        return jwt_encoded

    @staticmethod
    def decode_token(token):
        """
         this method is use for decode jwt token
        :param token:
        :return:response
        """
        decoded_token = jwt.decode(
            token,
            "secret",
            algorithms=["HS256"]
        )

        # print(decoded_token)
        return decoded_token
