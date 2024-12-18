![nexios Logo](docs/logo.png)
# nexios API Framework 🚀💻

Welcome to **nexios**, a lightning-fast web framework built with Python, designed by **TechWithDunamix** — a Nigerian developer! 🇳🇬💡 nexios is your go-to framework for building APIs combining speed and simplicity to supercharge your projects. ⚡

---

## Why Choose nexios? 🤔

- **⚡ Blazing Fast**: Experience unmatched performance for all your web applications.
- **👨‍💻 Developer-Friendly**: Clean and minimal code that prioritizes productivity.
- **🔌 Easy Integration**: Get started effortlessly — no steep learning curve or complex configurations.

---

## Quick Start 🚀

Follow these steps to set up nexios and create your first app in minutes!

---

### 1. Install nexios 📦

Install the framework directly from GitHub:

```bash
pip install git+https://github.com/TechWithDunamix/nexios.git
```

---

### 2. Create Your First Application 💻

Use the `nexios create` command to generate your project structure:

```bash
nexios create <app_name>
```

#### Example Output:
```plaintext
To get started:
1. cd <app_name>
2. Run the application with uvicorn
3. Your app will be available at http://localhost:8000
```

---

### 3. Project Structure

The generated project will have the following structure:

```plaintext
project_name/
├── controllers/
│   └── home_handler.py
├── main.py
├── models.py
├── settings.py
└── README.md
```

---

## Code Example: Basic nexios Application

```python
import uvicorn
from nexios import get_application
from nexios.routers import Routes
from controllers.home_handler import home_handler

app = get_application()

app.add_route(Routes("/", home_handler))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Create the `home_handler.py` in the `controllers/` directory:

```python
from nexios.http.request import Request
from nexios.http.response import nexiosResponse

async def home_handler(request: Request, response: nexiosResponse, **kwargs):
    return response.json({
        "message": "Welcome to nexios!",
        "docs": "https://nexios.example.com/docs"
    })
```

---

## Step-by-Step Development Workflow

1. **Install Dependencies**:
   ```bash
   pip install git+https://github.com/TechWithDunamix/nexios.git
   ```

2. **Run Your Application**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Access Your App**:
   Visit [http://localhost:8000](http://localhost:8000) to see your application in action.

4. **Migrate Database** (if applicable):
   ```bash
   aerich init -t settings.migration
   aerich migrate
   aerich upgrade
   ```

---

## Project Components

### **1. main.py**

The entry point for your application.

Responsibilities:
- Initialize the nexios app
- Setup startup/shutdown hooks
- Configure routes
- Start the ASGI server with Uvicorn

### **2. controllers/home_handler.py**

Handles the routing logic for your application.

Responsibilities:
- Define HTTP endpoints
- Process incoming requests
- Format and return responses

### **3. settings.py**

Centralized configuration for your application.

Responsibilities:
- Manage application settings (e.g., `SECRET_KEY`)
- Configure ORM and environment variables
- Provide settings for different environments (development/production)

### **4. models.py**

Defines database models and handles ORM integration.

Responsibilities:
- Map Python classes to database tables
- Provide schema validation
- Integrate with Tortoise ORM for migrations

---

## Extending the Framework

1. **Add New Directories**:
   - `middlewares/`: Add custom middleware.
   - `schemas/`: Define validation schemas for requests and responses.
   - `services/`: Encapsulate business logic.

2. **Extend Configuration**:
   - Add logging configurations.
   - Separate settings for environments (e.g., `settings_dev.py`).

3. **Enhance Database Management**:
   - Use Aerich for database migrations.
   - Configure additional connections in `settings.py`.

---

## Best Practices

1. **Secure Configuration**:
   - Store sensitive data (e.g., `SECRET_KEY`) in environment variables.
   - Use separate settings for development and production.

2. **Keep Code Modular**:
   - Define handlers in `controllers/`.
   - Separate business logic into dedicated services.

3. **Consistent Responses**:
   - Ensure all endpoints return structured and documented responses.

---

### nexios — Powering Simplicity and Speed in Web Development 