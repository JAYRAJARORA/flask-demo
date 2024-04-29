# Web Backend with Python

This repository is a collection of backend projects and strategies implemented in Python, showcasing a progression from fundamental CRUD operations to advanced scalable backend solutions.

## Overview

The journey begins with implementing basic CRUD applications, such as a library management system, using popular databases like MySQL and MongoDB. Each folder within the repository represents a unique application or concept implemented using Python-based web frameworks, Flask and FastAPI.

## Projects

- **Library Management Systems**: Utilize MySQL and MongoDB to understand the nuances of different databases and how to interact with them using Python.
  - `library-management-using-mysql`: A simple Flask-based web application with MySQL for managing books in a library.
  - `library-management-using-mongodb`: FastAPI application demonstrating document-based data management with MongoDB.

- **Scalable Backend Strategies**: As the projects evolved, advanced backend strategies were incorporated to address scalability and performance.
  - `database-replication-using-mongodb-replica-set`: Implementing database replication to ensure high availability and data redundancy using MongoDB's replica set feature.
  - `load-balancing-using-nginx`: Configuring NGINX as a load balancer to distribute incoming network traffic across multiple servers, improving responsiveness and availability of applications.
  - `email-background-sender-using-celery`: Leveraging Celery, an asynchronous task queue, to handle the background processing of email sending tasks, thus keeping the web application's main thread free for user requests.
  - `item-management-using-redis-and-mysql`: Employing Redis as a caching layer to enhance the performance of an item management system backed by MySQL, reducing data retrieval times and database load.

## Getting Started

Each folder contains a self-contained application or concept demonstration. To get started with any of the projects:

Clone the repository to your local machine:
   ```bash
   git clone https://github.com/<your-username>/web-backend-with-python.git
   ```
