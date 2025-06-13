# Project Overview

## 🚀 Our Tasks

- [ ] **Implement default connection handling**
- [ ] **Feature:** Build User Interface
- [ ] **Feature:** Message delivery & reception
- [ ] **Feature:** Writing Indicators
- [ ] **Feature:** Live Location
- [ ] **Support:** Read Receipts

---

## 📝 Getting Started

Follow these steps to set up and run both the server and client:

### 1. Clone the Repository
```bash
git clone https://github.com/Don27san/ikomm-Gruppe2.git
cd ikomm-Gruppe2
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

```bash
python -m server.main
```

### 4. Start the Client (in a new terminal)

```bash
python -m client.main
```

---

## 💡 Important Commands

If you are using `Pipenv`, you can use the following scripts defined in your `Pipfile` for easier setup and management:

```bash
# Start the client on localhost
pipenv run client

# Start the server on localhost
pipenv run server

# Start the client on local network
pipenv run client-prod

# Start the server on local network
pipenv run server-prod

# Generate Python code from protobuf definitions
pipenv run pb-compile

# Update requirements.txt with current dependencies
pipenv run update-requirements
```

These scripts simplify running common tasks without typing full commands. :)