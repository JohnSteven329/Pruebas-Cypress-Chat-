from services.firebase_service import FirebaseService
from models import User
import uuid

# Inicializar el servicio
firebase_service = FirebaseService()

# Crear usuario de prueba
test_user = User(
    id=str(uuid.uuid4()),
    name="John Test",
    room="general",
    is_online=True,
    is_active=True
)

# Guardar en Firestore
success = firebase_service.create_user(test_user)

if success:
    print("✅ Usuario de prueba creado correctamente en Firestore.")
else:
    print("❌ Error al crear el usuario.")
