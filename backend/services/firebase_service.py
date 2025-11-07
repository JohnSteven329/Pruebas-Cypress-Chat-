"""
Servicio de Firebase corregido para cargar credenciales desde el archivo .env
"""

import os
import json
import logging
from typing import List, Optional
from datetime import datetime

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, messaging
from firebase_admin.firestore import firestore as firestore_module

from models import User, Message

logger = logging.getLogger(__name__)


class FirebaseService:
    """Servicio para manejar Firebase Firestore y Cloud Messaging."""
    
    def __init__(self):
        self._app = None
        self._db = None
        self._initialized = False
        self._initialize()
    
    def _initialize(self):
        """Inicializar Firebase Admin SDK usando variables de entorno (.env)."""
        try:
            # Cargar las variables del archivo .env
            load_dotenv()

            project_id = os.getenv("FIREBASE_PROJECT_ID")
            private_key = os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n')
            client_email = os.getenv("FIREBASE_CLIENT_EMAIL")

            if not project_id or not private_key or not client_email:
                logger.error("❌ No se encontraron las variables de entorno de Firebase")
                return

            # Crear un diccionario con las credenciales
            firebase_config = {
                "type": "service_account",
                "project_id": project_id,
                "private_key": private_key,
                "client_email": client_email,
                "token_uri": "https://oauth2.googleapis.com/token"
            }

            # Crear archivo temporal de credenciales en la carpeta backend
            cred_path = os.path.join(os.getcwd(), "firebase_credentials.json")
            with open(cred_path, "w") as f:
                json.dump(firebase_config, f)

            # Inicializar Firebase (solo si no está ya inicializado)
            if firebase_admin._apps:
                self._app = firebase_admin.get_app()
            else:
                cred = credentials.Certificate(cred_path)
                self._app = firebase_admin.initialize_app(cred)

            self._db = firestore.client(app=self._app)
            self._initialized = True
            logger.info("✅ Firebase inicializado correctamente")

        except Exception as e:
            logger.error(f"❌ Error al inicializar Firebase: {e}")
            self._initialized = False

    # --------------------------------------------------------
    # MÉTODOS DE FIRESTORE
    # --------------------------------------------------------

    def create_user(self, user: User) -> bool:
        """Crear usuario en Firestore (sincrónico)."""
        try:
            if not self._initialized or not self._db:
                logger.info(f"Firebase not initialized. Would create user: {user.name}")
                return True
            
            user_data = {
                'id': user.id,
                'name': user.name,
                'room': user.room,
                'is_online': user.is_online,
                'is_active': user.is_active,
                'created_at': firestore_module.SERVER_TIMESTAMP,
                'last_seen': firestore_module.SERVER_TIMESTAMP
            }
            
            self._db.collection('users').document(user.id).set(user_data)
            logger.info(f"User {user.name} created in Firestore")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create user in Firestore: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Obtener usuario de Firestore (sincrónico)."""
        try:
            if not self._initialized or not self._db:
                return None
            
            doc = self._db.collection('users').document(user_id).get()
            if doc.exists:
                data = doc.to_dict()
                return User(
                    id=data['id'],
                    name=data['name'],
                    room=data.get('room', 'general'),
                    is_online=data.get('is_online', True),
                    is_active=data.get('is_active', True)
                )
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user from Firestore: {e}")
            return None
    
    def save_message(self, message: Message) -> bool:
        """Guardar mensaje en Firestore (sincrónico)."""
        try:
            if not self._initialized or not self._db:
                logger.info(f"Firebase not initialized. Would save message: {message.content}")
                return True
            
            message_data = {
                'id': message.id,
                'content': message.content,
                'user_id': message.user_id,
                'user_name': message.user_name,
                'room': message.room,
                'timestamp': message.timestamp,
                'message_type': message.message_type,
                'created_at': firestore_module.SERVER_TIMESTAMP
            }
            
            self._db.collection('messages').document(message.id).set(message_data)
            logger.info(f"Message {message.id} saved to Firestore")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save message to Firestore: {e}")
            return False
    
    def get_messages_by_room(self, room: str, limit: int = 50) -> List[Message]:
        """Obtener mensajes de una sala específica (sincrónico)."""
        try:
            if not self._initialized or not self._db:
                logger.info(f"Firebase not initialized. Would get messages for room: {room}")
                return []
            
            messages_ref = self._db.collection('messages')\
                .where('room', '==', room)\
                .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                .limit(limit)
            
            docs = messages_ref.stream()
            messages = []
            for doc in docs:
                data = doc.to_dict()
                message = Message(
                    id=data['id'],
                    content=data['content'],
                    user_id=data['user_id'],
                    user_name=data['user_name'],
                    room=data['room'],
                    timestamp=data['timestamp'],
                    message_type=data.get('message_type', 'text')
                )
                messages.append(message)
            
            return list(reversed(messages))
            
        except Exception as e:
            logger.error(f"Failed to get messages from Firestore: {e}")
            return []
    
    def get_users_by_room(self, room: str) -> List[User]:
        """Obtener usuarios activos de una sala específica (sincrónico)."""
        try:
            if not self._initialized or not self._db:
                logger.info(f"Firebase not initialized. Would get users for room: {room}")
                return []
            
            users_ref = self._db.collection('users')\
                .where('room', '==', room)\
                .where('is_active', '==', True)
            
            docs = users_ref.stream()
            users = []
            for doc in docs:
                data = doc.to_dict()
                user = User(
                    id=data['id'],
                    name=data['name'],
                    room=data['room'],
                    is_online=data.get('is_online', True),
                    is_active=data.get('is_active', True)
                )
                users.append(user)
            
            return users
            
        except Exception as e:
            logger.error(f"Failed to get users from Firestore: {e}")
            return []
    
    def update_user_status(self, user_id: str, is_online: bool) -> bool:
        """Actualizar estado de conexión del usuario (sincrónico)."""
        try:
            if not self._initialized or not self._db:
                logger.info(f"Firebase not initialized. Would update user {user_id} status to {is_online}")
                return True
            
            self._db.collection('users').document(user_id).update({
                'is_online': is_online,
                'last_seen': firestore_module.SERVER_TIMESTAMP
            })
            
            logger.info(f"User {user_id} status updated to {is_online}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user status: {e}")
            return False
    
    def send_notification(self, token: str, title: str, body: str, data: dict = None) -> bool:
        """Enviar notificación push usando Firebase Cloud Messaging."""
        try:
            if not self._initialized:
                logger.info(f"Firebase not initialized. Would send notification: {title}")
                return True
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=token
            )
            
            response = messaging.send(message)
            logger.info(f"Notification sent successfully: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
