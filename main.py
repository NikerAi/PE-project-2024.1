from fastapi import FastAPI, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from code import main


app = FastAPI(title="English articles processing")


@app.get("/availability check")
async def app_running():
	return {"Status": "200 OK"}


@app.post("/pdf process")
async def get_user_pdf(file: UploadFile = File(...)):
	if file.filename[-3:] != "pdf":
		raise HTTPException(415, detail="Unsupported Media Type. Please upload pdf file")
	else:
		pdf_path = f"Uploaded files/{file.filename}"
		with open(pdf_path, "wb") as f:
			content = await file.read()
			f.write(content)
		docx_path = main(pdf_path)
		return FileResponse(path=docx_path, filename=file.filename.split(".")[0]+".docx",
		                    media_type ="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
