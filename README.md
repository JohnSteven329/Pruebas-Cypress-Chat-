Pruebas-Cypress-Chat

Una aplicación de chat grupal en tiempo real desarrollada con Next.js (Frontend) y FastAPI (Backend), complementada con Firebase para la mensajería y pruebas automatizadas E2E con Cypress.

🚀 Descripción

Este proyecto demuestra la integración completa de una aplicación web moderna con arquitectura cliente-servidor, conectando un frontend interactivo con un backend en Python, y añadiendo un flujo automatizado de pruebas de extremo a extremo con Cypress para garantizar la calidad del sistema.

⚙️ Tecnologías Utilizadas
🧭 Frontend (Next.js + TypeScript)

Next.js 14 → Framework React para SSR y SPA.

TypeScript → Tipado estático para mayor robustez.

Tailwind CSS → Estilos utilitarios para diseño responsivo.

Socket.IO Client → Comunicación en tiempo real.

Lucide React → Librería de íconos moderna.

🧩 Backend (FastAPI + Firebase)

FastAPI → Framework de alto rendimiento para APIs REST.

Socket.IO → Comunicación bidireccional cliente-servidor.

Firebase Admin SDK → Integración con Firestore y Cloud Messaging.

🧠 Testing Automatizado

Cypress → Pruebas End-to-End (E2E) que validan la funcionalidad del chat:

Pantalla de inicio.

Inicio de sesión en el chat.

Escritura de mensajes sin enviarlos.

Capturas automáticas durante el flujo.

🧰 Instalación y Configuración
🔹 1. Clonar el repositorio
git clone https://github.com/JohnSteven329/Pruebas-Cypress-Chat-.git
cd Pruebas-Cypress-Chat-

🔹 2. Configurar el Backend
cd backend
python -m venv venv
venv\Scripts\activate  # En Windows
# o
source venv/bin/activate  # En macOS/Linux

pip install -r requirements.txt


Crear el archivo .env con tus credenciales de Firebase:

FIREBASE_PROJECT_ID=tu-proyecto-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-...@tu-proyecto.iam.gserviceaccount.com


Ejecutar el servidor:

python main.py


Backend disponible en 👉 http://localhost:8000

🔹 3. Configurar el Frontend
cd ../frontend
npm install
npm run dev


Frontend disponible en 👉 http://localhost:3000

💬 Uso de la Aplicación

Accede a http://localhost:3000

Ingresa tu nombre en el formulario inicial

Haz clic en “Entrar al Chat”

Escribe y envía mensajes en tiempo real

Observa usuarios conectados en la barra lateral

🧪 Pruebas Automatizadas con Cypress

El flujo E2E del chat SmartTalk se valida mediante el archivo:

frontend/cypress/e2e/chat-tests/chat-flow-e2e.cy.js

Escenarios Probados:

✅ Validar la pantalla de inicio del chat

✅ Ingreso con nombre

✅ Escribir mensaje en el área de texto

✅ Generar capturas automáticas en cada paso

Ejecución:
cd frontend
npx cypress open

Cypress abrirá su interfaz para seleccionar el test y visualizarlo en tiempo real.
Las capturas se almacenan en:frontend/cypress/screenshots/
