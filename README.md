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


