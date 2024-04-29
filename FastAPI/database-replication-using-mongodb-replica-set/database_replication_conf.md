# FastAPI with MongoDB Replica Set Setup

This README outlines how to set up and run a FastAPI application with MongoDB configured in a replica set.

## Prerequisites

- Python 3.8 or higher
- MongoDB 4.4 or higher
- pip for installing Python packages

## Installation and Setup

### 1. Install MongoDB

Download and install MongoDB from the [MongoDB official site](https://www.mongodb.com/try/download/community).

### 2. Configure MongoDB Instances

Create directories for MongoDB data storage and start the MongoDB instances as part of a replica set:

# Create data directories for MongoDB instances
```bash
mkdir -p data/rs0-1 data/rs0-2 data/rs0-3
```
# Start MongoDB instances
```bash
mongod --replSet rs0 --port 27018 --bind_ip localhost --dbpath ./data/rs0-1 --oplogSize 50
mongod --replSet rs0 --port 27019 --bind_ip localhost --dbpath ./data/rs0-2 --oplogSize 50
mongod --replSet rs0 --port 27020 --bind_ip localhost --dbpath ./data/rs0-3 --oplogSize 50
```
### 3. Connect to one of the MongoDB instances and initialize the replica set:

# Connect to MongoDB
```bash
mongosh --port 27018
```
# Initialize the replica set

```bash
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "localhost:27018" },
    { _id: 1, host: "localhost:27019" },
    { _id: 2, host: "localhost:27020" }
  ]
})
```

### 4. Install Python Dependencies
```bash
pip3 install fastapi uvicorn pymongo pydantic
```
### 5. Run the FastAPI Application

# Replace 'main' with the name of your Python script
```bash
uvicorn database_replication:app --reload --host 0.0.0.0 --port 8000
```

### 6. Monitoring

Regularly check the status of the MongoDB replica set

# Connect to MongoDB
```bash
mongo --port 27018
```
# Check replica set status
```bash
rs.status()
```

### 7. Testing the API with HTTPie
You can use HTTPie, a command-line HTTP client, to test the API endpoints of the FastAPI application. This tool provides a simple and user-friendly way to send requests. Here are the commands to test the primary operations:

- **Create an Item**:
  To add a new item to the database, you can use the following HTTPie command. Replace `name`, `description`, and `price` with your data values:
  ```bash
  http POST localhost:8000/items name='Laptop' description='Sample Laptop' price=999
  http POST localhost:8000/items name='Phone' description='Sample Phone' price=799
  ```

- **Read an Item**:

```bash
http GET localhost:8000/items/{item_id}
```

- **Read all items**:
```bash
http GET localhost:8000/items 
```

### 8. Simulating Primary Node Failure in MongoDB Replica Set

**Identify the Current Primary Node**:
   # Determine the primary node by connecting to any of the MongoDB instances:
   ```bash
   mongo --port 27018  # Adjust the port if needed
   rs.status() # Look for "stateStr": "PRIMARY"
   ```

**Shut Down the Primary Node**:
Simulate a primary node failure by stopping the MongoDB process 
   ```bash
   mongod --shutdown --dbpath ./data/rs0-X  # Replace X with the number corresponding to the primary node
```

**Observe Automatic Failover**:
```bash
mongo --port 27019  # Use the port of a non-primary node
rs.status()  # Verify the new primary node
```

**Test the FastAPI Application**:
```
http GET localhost:8000/items/  # Example endpoint to fetch all items
```

