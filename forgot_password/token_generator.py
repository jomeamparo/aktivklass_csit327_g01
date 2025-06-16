# filepath: z:\L12X12W18\aktivklass\aktivklass_csit327_g01\forgot_password\token_generator.py
import uuid

class SimpleTokenGenerator:
    @staticmethod
    def generate_token():
        return str(uuid.uuid4())