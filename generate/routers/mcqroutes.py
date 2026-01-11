from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from genques.mcqgenerate import generate_mcq
from genques.export_word import export_quiz_to_word

router = APIRouter()

class MCQRequest(BaseModel):
    text: str

class ExportRequest(BaseModel):
    quiz: dict

@router.post("/mcq")
async def mcq_route(req: MCQRequest):
    return {"ok": True}

@router.post("/export-word")
async def export_word_route(req: ExportRequest):
    """Export quiz to Word document"""
    word_file = export_quiz_to_word(req.quiz)
    
    return StreamingResponse(
        word_file,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": "attachment; filename=quiz.docx"
        }
    )
