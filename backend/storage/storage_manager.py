from pathlib import Path
import aiofiles


class StorageManager:

    @staticmethod
    async def save_file(

        file_path,

        content
    ):

        Path(file_path).parent.mkdir(

            parents=True,

            exist_ok=True
        )

        async with aiofiles.open(

            file_path,

            "wb"
        ) as f:

            await f.write(content)
            
         
    @staticmethod
    def read_file_sync(

        file_path
    ):

      with open(

             file_path,

             "rb"
         ) as f:

             return f.read()                
            

    @staticmethod
    async def read_file(

        file_path
    ):

        async with aiofiles.open(

            file_path,

            "rb"
        ) as f:

            return await f.read()