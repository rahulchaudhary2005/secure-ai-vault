import random

class OTPManager:

    @staticmethod
    def generate_otp():

        otp = random.randint(
            100000,
            999999
        )

        return str(otp)