# Data Access Service

Data Access Service is a program designed to manage users with different permission levels and interact with various databases.

## Features

- **Create Users**
  - Users can be created using the following classes:
    - `User`: Represents a regular user.
    - `Moderator`: Represents a moderator.
    - `Admin`: Represents an administrator.
- **Database Interaction**
  - After creating a user instance, you can interact with the database using the following methods:
    - `create()`: Add user data to the database.
    - `delete()`: Remove user data from the database.
    - `update()`: Update existing user data in the database.

## Supported Databases

- PostgreSQL
- MongoDB
- MySQL
