*Our Tasks*
- [ ] Implement default connection handling
- [ ] Feature: Message delivery & reception
- [ ] Feature: Writing Indicators
- [ ] Feature: Live Location
- [ ] Support: Read Receipts

*Entry Points:*
python -m client.main
python -m server.main

*Important commands:*
pip freeze > requirements.txt
protoc --python_out=. --pyi_out=. ./protobuf/messenger.proto

