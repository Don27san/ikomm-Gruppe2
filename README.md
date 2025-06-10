*Our Tasks*
- [ ] Implement default connection handling
- [ ] Feature: Message delivery & reception
- [ ] Feature: Writing Indicators
- [ ] Feature: Live Location
- [ ] Support: Read Receipts

*Important commands:*
pip freeze > requirements.txt
protoc --python_out=. --pyi_out=. ./protobuf/messenger.proto
venv/bin/python -m client.main
venv/bin/python -m server.main
