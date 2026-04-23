from fastapi import APIRouter, HTTPException
from Services.Quiz._bl import QuizService, QuizValidator

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])


@router.post("/start")
async def start_quiz(user_id: int, quiz_id: int = 1):
    error = QuizValidator.validate_start_data(user_id, quiz_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    result = QuizService.start_quiz(user_id, quiz_id)
    if result.get('error'):
        raise HTTPException(status_code=404, detail=result['error'])
    
    return result


@router.post("/answer")
async def submit_answer(session_id: str, question_id: int, answer_id: int):
    result = QuizService.submit_answer(session_id, question_id, answer_id)
    if result.get('error'):
        raise HTTPException(status_code=400, detail=result['error'])
    
    return result


@router.get("/result/{session_id}")
async def get_result(session_id: str):
    result = QuizService.get_result(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return result