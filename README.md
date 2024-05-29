# Real-Time Chat Application

## Overview

This project is a real-time chat application built using Django. The application allows users to sign up, log in, send messages to each other in real-time, and view their chat history. The application includes a REST API for user authentication and chat functionality, as well as WebSocket endpoints for real-time communication.

## Features

- **User Authentication**: Users can sign up with an email and password, log in, and log out.
- **Chat Functionality**: Users can see a list of other users, start chat sessions, send and receive messages, and view chat history.
- **Real-Time Communication**: Implemented using Django Channels and WebSockets.
- **Security**: WebSocket connections are secured and authenticated.

## Running the application

### Prerequisites
- Install Docker : [Docs](https://docs.docker.com/engine/install/)

### 1. Clone the Repository

```bash
git clone https://github.com/OzoneBht1/chat-app-rest
```

### 2. Create a .env file. 

> Change the example.env file name to .env, and edit the file to set in your values. Just setting a new password will work.

### 3. Building and Running Containers with Django, Redis and Postgres 

```bash
 docker-compose up --build
```

Once the Docker containers have been built and started successfully, you can access the application by navigating to http://localhost:8000 in your web browser.

**ASGI Server**

The application is served using the ASGI protocol, and it utilizes Daphne as the ASGI server for handling WebSocket connections.


## Rest API Documentation

The application comes with Swagger UI integrated to easily explore and interact with the API endpoints. To access the API documentation, you can visit:

[Swagger UI](http://localhost:8000/schema/swagger-ui)

Here, you'll find a comprehensive overview of all available endpoints, along with detailed descriptions of request and response parameters.

Additionally, you can download the OpenAPI schema from:

[OpenAPI Schema](http://localhost:8000/schema/)

You can import this schema into tools like Postman for easier API testing and integration.

## Websocket Endpoints Documentation

### Prerequisites for Connecting to Websocket
To connect to the Websocket server, you must first log in into the application. The system uses token based (JWT) authentication. 

To obtain a token: [Create a new user](http://localhost:8000/schema/swagger-ui/#/users/users_register_create) -> [Log in with Your New User](http://localhost:8000/schema/swagger-ui/#/users/users_token_create)

> You can create a few additional users as they will be required for opening a new connection to the websockets. After that, you can fetch the users to start a chat through [here](http://localhost:8000/schema/swagger-ui/#/users/users_list)

#### Connecting to WebSocket

All of the connections to the websockets are authenticated with JWT. For requests to websocket server, add authorization token in request headers.

```bash
Authorization: Bearer <token>
```

To start a chat with a user, pass their user id to the url<br>

**WebSocket URL**: ws://localhost:8000/ws/chat/{user_id}/

You will be connected to the websocket server. In case of failure, make sure the user_id passed is correct and the JWT token is correct and not expired.

#### Sending Messages

Once connected, clients can send messages to the WebSocket server using JSON payloads. The format of the message payload should include the following fields:

    message: The content of the message.

Example JSON message payload:

```json
{
  "message": "Hello, user2!",
}
```

#### Receiving Messages

Clients will receive messages from the WebSocket server in JSON format. Each message will include the following fields:

    type: The type of message. In our case, it will be "chat.message".
    message: The content of the message.
    sender: The username of the sender.

Example JSON message received from the server:

```json
{
  "type": "chat.message",
  "message": "Hello, user1!",
  "sender": "user2"
}
```

#### Closing the Connection

To disconnect from the WebSocket server, clients can close the WebSocket connection.

## Testing

The application uses pytest as the primary testing tool, along with faker and factoryboy for generating test data.

To run the tests, exec inside the docker container of django and run pytest.

1) View running containers to obtain the id or name of django container.

```bash
docker ps
```
> Copy the name or container id of the running django container. It should be the one running on port 8000.

2) Open the container shell. 
```bash
docker exec -it <container_name_or_id> bash
```
3) Run the tests.
```bash
pytest
```

The tests live inside the core_apps/tests directory, and currently contain the test cases of users, messages and websocket.
