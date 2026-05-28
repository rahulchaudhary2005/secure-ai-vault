import os

class SecureDelete:

    @staticmethod
    def wipe_file(file_path: str):

        if not os.path.exists(file_path):
            return False

        length = os.path.getsize(file_path)

        with open(file_path, "ba+", buffering=0) as f:

            f.seek(0)

            f.write(
                os.urandom(length)
            )

        os.remove(file_path)

        return True