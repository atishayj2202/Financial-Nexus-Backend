# Catalogify Backend

Welcome to the Financial Nexus backend repository! This backend repository serves as the core infrastructure powering the Financial Nexus platform.

Financial Nexus is a centralized hub designed for users to seamlessly manage and monitor their entire financial ecosystem. By consolidating expenses, income, investments, and liabilities in one intuitive platform, Financial Nexus provides users with a comprehensive overview of their financial landscape. With its user-friendly interface and customizable features, Financial Nexus empowers users to make informed decisions, track their progress, and ultimately achieve their financial objectives. The platform maintains a steadfast commitment to security and privacy, ensuring that users' financial data remains protected at all times. Whether you're striving for financial stability or aiming for growth, Financial Nexus is your essential tool for efficiently navigating the complexities of personal finance.
## Project Links

This section contains links to the frontend and backend repositories, as well as the base URL and documentation for the backend API.

### Frontend Live 
-  Repository URL: [https://financial-nexus.vercel.app/](https://financial-nexus.vercel.app/)

### Frontend Repository
-  Repository URL: [https://github.com/coderkhushal/financial-nexus-Frontend](https://github.com/coderkhushal/financial-nexus-Frontend)

### Backend Repository
-  Repository URL:[https://github.com/atishayj2202/Financial-Nexus-Backend](https://github.com/atishayj2202/Financial-Nexus-Backend)

### Backend API Endpoint Base URL
-  Base URL: https://financial-nexus-backend.yellowbush-cadc3844.centralindia.azurecontainerapps.io 

### Backend API Endpoint Documentation
- Documentation URL: https://financial-nexus-backend.yellowbush-cadc3844.centralindia.azurecontainerapps.io/docs

## Technologies Used
- **Programming Language**: Python
- **Framework**: fastAPI
- **Database**: PostgresSQL( Azure SQL)
- **Authentication**: Firebase Authentication
- **Deployment**: Azure Container App
- **Poetry**: Poetry is used as the dependency manager for managing Python packages and dependencies.

## Project Structure
The backend project follows a standard fastAPI project structure with modular apps for different functionalities. Here's an overview of the main components:
- **auth**: This directory contains modules related to authentication, including functions for handling authentication for each request.
- **client**: Here resides the client modules for Firebase Authentication and database. It provides functionalities to interact with Firebase services.
- **db**: This directory handles the database interactions and includes the schema definition for each table and view. 
  - The base.py file contains the parent Schema and basic algorithms for each table. 
  - The tables subdirectory contains schema definitions for various database tables, while the views subdirectory contains schema definitions for database views.
- **schemas**: Contains schema definitions for requests and responses. This helps maintain a structured approach to handling data exchanges.
- **routers**: Contains router modules for FastAPI. These routers define the API endpoints and link them to appropriate handlers.
- **services**: Includes algorithms to handle queries in the database and return data. These services encapsulate business logic related to data manipulation.
- **main.py**: This is the entry point of the application. It connects all routers to FastAPI, initializing the web server and defining routes.

## Deployment Instructions
The backend is designed to be deployed on Azure Platform (GCP) for scalability, reliability, and performance. Follow these steps for deployment:
##### Prerequisites
- Docker Daemon installed.
- Access to a remote location to upload Docker images (e.g., Docker Hub, Google Artifact Registry).

##### Build, Push & Deploy Docker Image
1. Update credentials in the `deploy.sh` file.
2. Run the following command to build and push the Docker image:
```shell
sh deploy/deploy.sh build_push
   ```

## Linting/Formatting
The following commands can be used:

```shell
poetry run sh deploy/local_test.sh check-format
poetry run sh deploy/local_test.sh format
```

## Bumpversion

```shell
poetry run bumpversion --config-file=./deploy/.bumpversion.cfg <option>
```
The option can be:
- patch: to update the patch version
- minor: to update the minor version
- major: to update the major version
- release: to update the release version
  - also add `--tag` to create a git tag when releasing

## Contributors
- Atishaya Jain
- Ajeem Ahmed
- Khushal Bhasinprompt, asset, bank, card, emi, loan, stock
- Rudr Pratap Singh
