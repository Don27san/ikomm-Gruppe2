# Testing Server-to-Server Connections

## Quick Test Instructions

To test the server-to-server discovery and connection functionality:

### 1. Start Multiple Servers

Open 3 separate terminal windows/tabs and run:

**Terminal 1:**
```bash
python test_server_connection.py --server-id server_1 --port-offset 0
```

**Terminal 2:**
```bash
python test_server_connection.py --server-id server_2 --port-offset 10
```

**Terminal 3:**
```bash
python test_server_connection.py --server-id server_3 --port-offset 20
```

### 2. Expected Output

Each server will:
1. Start its announcement service (responds to discovery requests)
2. Discover other servers via UDP broadcast
3. Connect to discovered servers via TCP
4. Show connection status

You should see output like:
```
Server server_1: Starting announcement service...
Server server_1: Discovering other servers...
Discovered server:  {'serverId': 'server_2', 'feature': [...], 'server_ip': '127.0.0.1'}
Discovered server:  {'serverId': 'server_3', 'feature': [...], 'server_ip': '127.0.0.1'}
Server server_1: Found 2 other servers
  - server_2 at 127.0.0.1
  - server_3 at 127.0.0.1
Server server_1: Connecting to discovered servers...
CONNECTED to server server_2
CONNECTED to server server_3
Server server_1: Connected to 2 servers:
  - Connected to server_2
  - Connected to server_3
```

### 3. Stop Servers

Press `Ctrl+C` in each terminal to gracefully stop the servers. You should see hangup messages as servers disconnect from each other.

## Integration with Main Application

To use this in the main chat application, the server-to-server functionality is already integrated into `server/main.py`. When you start a server with:

```bash
python -m server.main
```

It will automatically:
- Start the announcement service
- Discover other servers
- Connect to them for inter-server communication

## Configuration

The implementation uses the existing configuration in `config.py`. Key settings:

- `discovery_port`: UDP port for server discovery (default: 9999)
- `ping_timeout`: Connection timeout in seconds (default: 300)
- `serverId`: Unique identifier for this server
- Feature ports for different services (chat, typing, location)

## Port Offset System

The test script uses a port offset system to run multiple servers on the same machine:

- Server 1: Base ports (6666, 7777, 8888, etc.)
- Server 2: Base ports + 10 (6676, 7787, 8898, etc.)  
- Server 3: Base ports + 20 (6686, 7797, 8908, etc.)

This avoids port conflicts during testing.
