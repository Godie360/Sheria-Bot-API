from fastapi import APIRouter, HTTPException, WebSocket
from models.chat import ChatMessage, ChatResponse
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

@router.post("/message", response_model=ChatResponse)
async def send_message(chat_message: ChatMessage):
    try:
        response = await chat_service.process_message(
            chat_message.content,
            chat_message.session_id
        )
        return ChatResponse(
            message=response,
            session_id=chat_message.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            message = await websocket.receive_text()
            response = await chat_service.process_message(message)
            await websocket.send_text(response)
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
        await websocket.close()
