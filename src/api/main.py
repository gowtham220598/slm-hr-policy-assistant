from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from src.model.inference import generate
from src.model.context import find_policy
app=FastAPI(title='HR Policy SLM Assistant',version='1.0')
class AskRequest(BaseModel):
    question:str=Field(min_length=3,max_length=500)
class AskResponse(BaseModel):
    answer:str
    latency_seconds:float
    model:str
@app.get('/health')
def health():return {'status':'ok'}
@app.post('/ask',response_model=AskResponse)
def ask(body:AskRequest):
    context=find_policy(body.question)
    if not context:return AskResponse(answer='I do not have that policy information.',latency_seconds=0,model='policy-guard')
    try:return AskResponse(**generate(body.question,context,optimized=True))
    except Exception as e:raise HTTPException(status_code=503,detail='Model unavailable; check local model installation') from e
