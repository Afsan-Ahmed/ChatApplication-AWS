# ⚡ Real-Time Chat Application

A serverless, scalable real-time chat application built using AWS WebSocket API, Lambda, and DynamoDB. Messages appear instantly for all connected users with zero server management.

![AWS](https://img.shields.io/badge/AWS-WebSocket%20%7C%20Lambda%20%7C%20DynamoDB-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Project Overview

This project demonstrates building a production-ready, event-driven real-time communication system using AWS serverless technologies. It showcases best practices in WebSocket communication, connection management, and scalable architecture design.

**Live Demo:** *[Add your deployed link here]*

## ✨ Features

- **Real-time messaging** - Messages appear instantly for all connected users
- **Connection management** - Tracks active users and handles disconnections gracefully
- **Message persistence** - All messages stored in DynamoDB for history
- **Serverless architecture** - Scales automatically from 1 to 10,000+ concurrent users
- **Event-driven design** - Separate Lambda functions for connect, disconnect, and messaging
- **Clean UI** - Modern, responsive chat interface with typing indicators

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │ (WebSocket Connection)
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  API Gateway        │ (WebSocket API)
│  - $connect         │
│  - $disconnect      │
│  - sendmessage      │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│           Lambda Functions            │
│  ┌────────────┐  ┌────────────┐      │
│  │  Connect   │  │ Disconnect │      │
│  └────────────┘  └────────────┘      │
│  ┌─────────────────────────────┐     │
│  │      SendMessage             │     │
│  │  - Save to DynamoDB          │     │
│  │  - Broadcast to all users    │     │
│  └─────────────────────────────┘     │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│          DynamoDB Tables              │
│  ┌────────────────┐  ┌─────────────┐ │
│  │ ChatConnections│  │ChatMessages │ │
│  │ (Active users) │  │  (History)  │ │
│  └────────────────┘  └─────────────┘ │
└──────────────────────────────────────┘
```

## 🛠️ Tech Stack

**Backend:**
- **AWS API Gateway** - WebSocket API for real-time bidirectional communication
- **AWS Lambda** - Serverless compute for handling connections and messages
- **AWS DynamoDB** - NoSQL database for connection tracking and message storage
- **Python 3.11** - Lambda runtime

**Frontend:**
- **HTML5/CSS3** - Modern, responsive UI
- **JavaScript** - WebSocket client and DOM manipulation

**Infrastructure:**
- **IAM** - Role-based access control for Lambda functions
- **CloudWatch** - Logging and monitoring

## 📋 Prerequisites

- AWS Account with appropriate permissions
- Basic understanding of AWS services (Lambda, DynamoDB, API Gateway)
- Python 3.11 or later (for local testing)
- Web browser with WebSocket support
