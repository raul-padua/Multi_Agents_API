## **Customer Service Chatbot API** 🚀

This project is a customer service chatbot handling inquiries via specialized agents (Sales, Technical Support, Customer Support). It integrates LLMs (GPT-4), follows a hybrid policy approach (strict enforcement + RAG retrieval), and is accessible via a REST API.

## 📌 **Features** 
	•	Specialized Agents: Sales, Technical Support, and Customer Support
	•	LLM Integration: GPT-4
	•	Hybrid Policy System: Code-based + RAG retrieval (ChromaDB)
	•	REST API: FastAPI framework
	•	Docker Support: Containerized services (FastAPI + PostgreSQL)
	•	Persistence Layer: PostgreSQL (default) or in-memory storage
	•	Unit & Integration Tests: Coverage for API endpoints and policies

## 🚀 **Quickstart**

### 1️⃣ Setup & Run Locally

Install Dependencies
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

Run the API Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Option 2: Run with Docker
To run the service inside a Docker container:
```bash
docker-compose up --build -d
```
🚀 1️⃣.1️⃣ Sales Agent - Product Inquiry
```bash
curl -X POST "http://localhost:8000/conversation/sales" \
     -H "Content-Type: application/json" \
     -d '{
           "conversation_id": "demo_sales_1",
           "user_input": "What are the latest product deals?"
         }'
```
✅ Expected Response (similar meaning):
```json
{
    "conversation_id":"demo_sales_1",
    "agent":"sales",
    "agent_response":"Thank you for your inquiry. As of now, we have several exciting deals:\n\n1. A 10% discount on our annual Premium Plan subscription.\n2. A special bundle offer where if you buy two of our flagship products, you get a third one at half price.\n3. Free shipping for orders over $100.\n\nPlease note that these offers are subject to availability and may change. Is there a specific product or deal you're interested in?",
    "retrieved_policies":["No relevant policy found."],
    "history":[
        {"timestamp":"2025-02-03T15:24:15.000877","sender":"user","content":"What are the latest product deals?","id":18,"conversation_id":"demo_sales_1"},
        {"timestamp":"2025-02-03T15:24:15.010945","sender":"bot","content":"Thank you for your inquiry. As of now, we have several exciting deals:\n\n1. A 10% discount on our annual Premium Plan subscription.\n2. A special bundle offer where if you buy two of our flagship products, you get a third one at half price.\n3. Free shipping for orders over $100.\n\nPlease note that these offers are subject to availability and may change. Is there a specific product or deal you're interested in?","id":19,"conversation_id":"demo_sales_1"}]}
```
⚙️ 1️⃣.2️⃣ Tech Support - Password Reset
```bashcurl -X POST "http://localhost:8000/conversation/tech_support" \
     -H "Content-Type: application/json" \
     -d '{
           "conversation_id": "demo_tech_1",
           "user_input": "How do I reset my password?"
         }'
```
✅ Expected Response (similar meaning):
```json
{
    "conversation_id":"demo_tech_1",
    "agent":"tech_support",
    "agent_response":"❌ Authentication is required before resetting a password. Please verify your identity first.","retrieved_policies":["No relevant policy found."],
    "history":[
        {"timestamp":"2025-02-03T15:24:31.591282","sender":"user","content":"How do I reset my password?","id":20,"conversation_id":"demo_tech_1"},
        {"timestamp":"2025-02-03T15:24:31.599495","sender":"bot","content":"❌ Authentication is required before resetting a password. Please verify your identity first.","id":21,"conversation_id":"demo_tech_1"}]}
```
📦 1️⃣.3️⃣ Customer Support - Order Tracking
```bash
curl -X POST "http://localhost:8000/conversation/customer_support" \
     -H "Content-Type: application/json" \
     -d '{
           "conversation_id": "demo_support_1",
           "user_input": "Where is my order?"
         }'
```
✅ Expected Response (similar meaning):
```json
{
    "conversation_id":"demo_support_1",
    "agent":"customer_support",
    "agent_response":"I'm sorry to hear that you're having trouble with your order. Could you please provide me with your order number so I can check the status for you?",
    "retrieved_policies":["No relevant policy found."],
    "history":[
        {"timestamp":"2025-02-03T15:28:12.473238","sender":"user","content":"Where is my order?","id":22,"conversation_id":"demo_support_1"},
        {"timestamp":"2025-02-03T15:28:12.485400","sender":"bot","content":"I'm sorry to hear that you're having trouble with your order. Could you please provide me with your order number so I can check the status for you?","id":23,"conversation_id":"demo_support_1"}]}
```

### 2️⃣ Verify the API is Running
Once the server starts, you can check its status by making a request to retrieve the latest conversations:
```bash
curl -X GET "http://localhost:8000/"
```
✅ Expected Response (Example)
```json
[
    {
        "conversation_id": "test123",
        "messages": [
            {"sender": "user", "content": "Can you tell me more about the Premium Plan?"},
            {"sender": "bot", "content": "Our Premium Plan includes unlimited access to all services..."}
        ]
    }
]
```
💡 Note: This API does not have a dedicated health check. The root (/) endpoint retrieves the latest stored conversations.

## 🛠 **API Endpoints**

| Method | Endpoint                         | Description |
|--------|----------------------------------|-------------|
| **GET**  | `/conversations`                | Retrieve all conversations (supports pagination). |
| **GET**  | `/conversation/{conversationUuid}` | Get a specific conversation with all messages. |
| **POST** | `/conversation/{conversationUuid}` | Add a user message to a conversation, get agent response. |
| **POST** | `/retrieve_policy`              | Retrieve the most relevant policy based on user query. |
| **DELETE** | `/conversation/{conversation_id}` | Delete all messages from a specific conversation. |

### ✅ **Example API Response**
```json
{
    "agent_response": "I've checked the price and created your order",
    "agent": "sales",
    "functions_called": [
        {
            "name": "check_price",
            "parameters": {
                "product_name": "Premium Plan"
            },
            "response": {
                "price": 100,
                "currency": "USD",
                "in_stock": true
            }
        },
        {
            "name": "create_order",
            "parameters": {
                "product_name": "Premium Plan",
                "quantity": 1,
                "email": "user@example.com"
            },
            "response": {
                "order_number": "ORD123",
                "status": "created",
                "estimated_delivery": "2024-01-27"
            }
        }
    ]
}
```
---

### 🤖 **Agent Logic & Policies**

A **policy** is a business rule that governs how an agent behaves in specific situations. Each agent has at least **two policies** to determine when actions are allowed, restricted, or enforced.

| **Agent**           | **Functions** | **Description** |
|----------------------|--------------|-----------------|
| **📢 Sales Agent** | `check_price(product_name)` | Retrieves the price and availability of a product. |
|                    | `create_order(product_name, quantity, email)` | Creates an order for the specified product. |
| **🔧 Technical Support** | `reset_password(email)` | Initiates a password reset process. |
|                    | `schedule_technician(email, address, issue)` | Schedules a technician visit for troubleshooting. |
| **📦 Customer Support** | `track_order(order_number)` | Checks the current status of an order. |
|                    | `cancel_order(order_number)` | Cancels an order if it meets policy conditions. |

### 📌 **Example Policy Rule**
> 🚨 **Policy:** Orders can only be canceled if they **haven’t been shipped**.

### 🔄 **Example Agent Flow**
```json
User: "I need help with my internet installation"
Agent: "I'll help you schedule a technician visit. What's your email and address?"
User: "user@example.com, 123 Main St, Apt 4B, New York, NY 10001"
[Function called: `schedule_technician("user@example.com", "123 Main St, Apt 4B, New York, NY 10001", "internet installation")`]
Response: {
    "appointment_id": "TECH123",
    "scheduled_date": "2024-01-21",
    "time_slot": "09:00-11:00",
    "technician_name": "Alex Smith",
    "service_type": "installation"
}
Agent: "I've scheduled a technician for tomorrow between 9 AM and 11 AM. You'll receive a confirmation email."
```

## 📖 RAG-Based Policy Retrieval

Policies are stored in .txt files and dynamically loaded into ChromaDB for retrieval.
🔹 Example: Policy Retrieval
```bash
curl -X POST "http://localhost:8000/retrieve_policy" \
     -H "Content-Type: application/json" \
     -d '{"query": "Can I cancel my order?"}'
```
✅ Expected Response with similar meaning
```json
{
    "query": "Can I cancel my order?",
    "retrieved_policies": [
        "Orders can only be canceled if they haven’t been shipped."
    ]
}
```
## 🧪 Testing
Run All Tests
```bash
pytest --cov=app tests/
```
✅ Example Output
```bash
======================= test session starts =======================
platform darwin -- Python 3.9, pytest-8.3.4
collected 10 items

tests/test_agents.py ....✅
tests/test_policies.py ..✅
tests/test_api.py ....✅
```

## 📂**Project Structure**

The repository follows a modular structure for clarity and maintainability.
customer_service_chatbot/
│── app/                       # Core application directory
│   ├── agents/                # Specialized agents (Sales, Tech Support, Customer Support)
│   ├── api/                   # API route definitions (FastAPI)
│   ├── models/                # Database models (SQLAlchemy)
│   ├── policies/              # Policy rules (Hybrid: Code + RAG)
│   ├── services/              # Core services (LLM, RAG, Database, Conversation Management)
│   ├── tests/                 # Unit and integration tests
│   ├── init.py            # Package initializer
│   ├── main.py                # FastAPI entry point
│── chroma_db/                 # Storage for ChromaDB (RAG-based policy retrieval)
│── .dockerignore              # Ignore unnecessary files in Docker builds
│── .env                       # Environment variables configuration
│── .gitignore                 # Git ignore file for sensitive & unnecessary files
│── chatbot_db_backup.dump      # Database backup file
│── config.py                   # Configuration settings
│── docker-compose.yml          # Docker Compose for multi-container setup
│── Dockerfile                  # Docker setup for the application
│── logfile                     # Application log file
│── README.md                   # Documentation
│── requirements.txt             # Python dependencies
│── venv/                        # Python virtual environment (local development)

### 📌 **Key Directories & Files**
| **Path**                 | **Description** |
|--------------------------|----------------|
| `app/`                   | Main application folder containing all core services. |
| `app/agents/`            | Implements specialized chatbot agents (Sales, Tech Support, etc.). |
| `app/api/`               | Defines FastAPI routes and endpoints. |
| `app/models/`            | Database schema and ORM models using SQLAlchemy. |
| `app/policies/`          | Business rules stored as both **hardcoded policies** and **retrievable policies (RAG)**. |
| `app/services/`          | Service layer handling **LLM integration, database interactions, and conversations**. |
| `app/tests/`             | Unit and integration tests to ensure correctness. |
| `chroma_db/`             | Stores **retrieved policy documents** using **ChromaDB** for RAG. |
| `config.py`              | Application configuration file for **environment settings, DB URLs, and API keys**. |
| `docker-compose.yml`     | Defines multi-container setup (FastAPI + Postgres). |
| `Dockerfile`             | Docker build file for the chatbot service. |
| `.env`                   | Stores environment variables (e.g., DB connection strings). |
| `chatbot_db_backup.dump` | Backup file of the database. |
| `requirements.txt`       | Lists required Python dependencies for the project. |
| `logfile`                | Stores runtime logs for debugging. |
---

## 📜 **Notes & Assumptions**
	•	Database Persistence: PostgreSQL (via Docker) or in-memory fallback.
	•	Function Responses: Mocked values for now.
	•	LLM Reasoning Improvement: Chain-of-Thought (CoT) reasoning is applied.
	•	AI Tools Used: OpenAI ChatGPT, Copilot, Cursor.
	•	Ambiguous Requirements: Interpreted pragmatically.

## 📌 **Final Thoughts**

This chatbot system provides structured, policy-driven, and AI-enhanced customer interactions via a modular, testable, and scalable architecture.

## 🛠 Future Work
	•	Implement real function execution instead of mocked values.
	•	Extend policy retrieval to dynamically update via API.
	•	Enhance LLM prompt engineering with few-shot examples.
    	•   	Integrate with a nice looking frontend and UI.
    	•   	Implement caches according to use cases.
     	•   	Implement chunks and overlapping to RAG service to handle large policies text documents.

## 📜 License

MIT License – Free to use, modify, and distribute.
