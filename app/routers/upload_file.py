from fastapi import APIRouter,UploadFile
import uuid
import os
router = APIRouter(tags=["uploadImages"])

@router.post("/uploadfile/")
async def create_upload_file(image: UploadFile):
    allowed_extensions = ["png", "jpg","gif","webp","jpeg"]
    ext = image.filename.split(".")[-1]
    if ext not in allowed_extensions:
        return {"error": "Unsupported file type"}
    safe_filename = str(uuid.uuid4()) + "." + ext
    file_location = os.path.join('upload', safe_filename)
    try:
        # 逐块读取和写入文件
        with open(file_location, "wb+") as file_object:
            while True:
                chunk = await image.read(8192)  # 使用适当的缓冲区大小
                if not chunk:
                    break
                file_object.write(chunk)
    except OSError as e:
        return {"error": f"Failed to save file: {str(e)}"}
    return {"filename": safe_filename, "file_size": f'{ "%.2f" % (image.size/(1024**2))}MB','saved_position': file_location,'url':''}