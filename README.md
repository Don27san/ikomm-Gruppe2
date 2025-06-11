# Project Overview

## 🚀 Our Tasks

- [ ] **Implement default connection handling**
- [ ] **Feature:** Message delivery & reception
- [ ] **Feature:** Writing Indicators
- [ ] **Feature:** Live Location
- [ ] **Support:** Read Receipts

---

## 🏁 Entry Points

```bash
python -m client.main
python -m server.main
```

---

## 💡 Important Commands

```bash
# Export dependencies
pip freeze > requirements.txt

# Generate Python code from protobuf
protoc --python_out=. --pyi_out=. ./protobuf/messenger.proto
```
