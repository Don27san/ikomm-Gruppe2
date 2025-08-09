# Project Overview

## 🚀 Our Tasks

- [x] **Implement default connection handling**
- [x] **Feature:** Handle Connection Management
- [x] **Feature:** Build User Interface
- [x] **Feature:** Message delivery & reception
- [x] **Feature:** Writing Indicators
- [x] **Feature:** Live Location
- [x] **Support:** Translation & Documents

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
# Using Pipenv
pipenv install

# Using pip
pip install -r requirements.txt
```

### 3. Start the Server (before the client)

```bash
# Using Pipenv
pipenv run server

# Using Python directly
python -m server.main
```

### 4. Start the Client (in a new terminal)

```bash
# Using Pipenv
pipenv run client

# Using Python directly
python -m client.main
```

---

## 💡 Usage Hints

- For best compatibility, we recommend using this application on **macOS**.
- Please **deactivate your firewall** temporarily to ensure proper connection between server and client.
- Make sure both server and client are running on the same local network for seamless communication.
