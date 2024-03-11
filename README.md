# Data Access Service

Data Access Service is a program designed to manage users with different permission levels and interact with various databases.

## Features

- **Create Users**
  - Users can be created using the following classes:
    - `User`: Represents a regular user.
    - `Moderator`: Represents a moderator.
    - `Admin`: Represents an administrator.
   
- **Data Access Objects(DAO)**
  - You can connect to various Databases through these classes:
    - `PostgeDAO`: Connect to PostgreSQL.
    - `MysqlDAO`: Connect to MySQL.
    - `CommonDAO`: Connect to both Databases.
    
- **Database Interaction**
  - After creating a user instance and DAO, you can interact with the database using the following methods:
    - `dao_instance.`**create**(user_instance): Add user data to the database.
    - `dao_instance.`**delete**(user_instance): Remove user data from the database.
    - `dao_instance.`**update**(user_instance): Update existing user data in the database.

## Supported Databases

- PostgreSQL
- MySQL
- MongoDB (not yet)
