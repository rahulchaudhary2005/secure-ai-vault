from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from typing import List

from api.controllers.upload_controller import (
    UploadController
)

router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload_files(

    files: List[UploadFile] = File(...)
):

    return await UploadController.upload_documents(
        files
    )

@router.get("/files")
async def get_uploaded_files():

    return await UploadController.list_uploaded_files()