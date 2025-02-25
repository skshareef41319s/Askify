from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from rag import ChatService
from sqlalchemy.orm import Session
from database import SessionLocal, Document
from pathlib import Path
import logging
from typing import Dict
import asyncio
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


# Store active connections
class ConnectionManager :
    def __init__(self) :
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str) :
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected. Active connections: {len(self.active_connections)}")

    async def disconnect(self, client_id: str) :
        if client_id in self.active_connections :
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected. Active connections: {len(self.active_connections)}")

    async def send_message(self, client_id: str, message: str) :
        if client_id in self.active_connections :
            await self.active_connections[client_id].send_text(message)


manager = ConnectionManager()


def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


@router.websocket("/ws/question_answer/{document_id}")
async def question_answer_ws(
        websocket: WebSocket,
        document_id: str,
        db: Session = Depends(get_db)
) :
    """
    WebSocket endpoint for real-time question answering based on PDF documents.

    Args:
        websocket: The WebSocket connection
        document_id: The ID of the document to query
        db: Database session
    """
    client_id = f"{document_id}_{datetime.utcnow().timestamp()}"
    chat_service = None

    try :
        # Verify document exists in database
        document = db.query(Document).filter(Document.pdf_id == document_id).first()
        if not document :
            await websocket.accept()
            await websocket.send_text(f"Error: Document with ID {document_id} not found in database.")
            await websocket.close()
            return

        # Build and verify PDF path
        upload_dir = Path("C:/Users/HP/OneDrive/Desktop/Askify-main/Askify-main/upload")
        pdf_path = upload_dir / f"{document_id}.pdf"

        if not pdf_path.exists() :
            await websocket.accept()
            await websocket.send_text(f"Error: PDF file not found at {pdf_path}")
            await websocket.close()
            logger.error(f"PDF file not found: {pdf_path}")
            return

        # Initialize chat service
        try :
            chat_service = ChatService(str(pdf_path))
            logger.info(f"Chat service initialized for document: {document_id}")
        except Exception as e :
            await websocket.accept()
            error_message = f"Error initializing chat service: {str(e)}"
            await websocket.send_text(error_message)
            await websocket.close()
            logger.error(error_message)
            return

        # Connect to WebSocket
        await manager.connect(websocket, client_id)
        await websocket.send_text("Connected to Q&A service. You can start asking questions.")

        while True :
            try :
                # Set a timeout for receiving messages
                data = await asyncio.wait_for(websocket.receive_text(), timeout=300)  # 5 minutes timeout

                if not data.strip() :
                    await manager.send_message(client_id, "Please provide a valid question.")
                    continue

                # Log the incoming question
                logger.info(f"Question received from {client_id}: {data[:100]}...")  # Log first 100 chars

                # Get response from chat service
                response = chat_service.chat(data)

                # Send response back to client
                await manager.send_message(client_id, response)

                # Log successful response
                logger.info(f"Response sent to {client_id}: {response[:100]}...")  # Log first 100 chars

            except asyncio.TimeoutError :
                await manager.send_message(client_id, "Session timed out due to inactivity.")
                break

            except Exception as e :
                error_message = f"Error processing question: {str(e)}"
                logger.error(f"Error for client {client_id}: {error_message}")
                await manager.send_message(client_id, error_message)
                break

    except WebSocketDisconnect :
        logger.info(f"WebSocket disconnected for client {client_id}")

    except Exception as e :
        logger.error(f"Unexpected error for client {client_id}: {str(e)}")

    finally :
        # Cleanup
        await manager.disconnect(client_id)
        if chat_service :
            # Clean up chat service resources if needed
            try :
                if hasattr(chat_service, 'cleanup') :
                    chat_service.cleanup()
            except Exception as e :
                logger.error(f"Error during chat service cleanup: {str(e)}")


# Optional: Add health check endpoint
@router.get("/ws/health")
async def websocket_health() :
    """Health check endpoint for WebSocket service"""
    return {
        "status" : "active",
        "active_connections" : len(manager.active_connections),
        "timestamp" : datetime.utcnow().isoformat()
    }
