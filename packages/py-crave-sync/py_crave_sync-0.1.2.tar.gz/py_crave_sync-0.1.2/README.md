py-crave-sync
A Python package that creates a local live server for syncing and serving data seamlessly. Designed to be lightweight, fast, and easily extensible.

# Features

Lightweight local live server for syncing operations.
Easy integration with other Python packages like py-crave-gui.
Simple to set up and run.
---------------------------------------------------------------------------------
# Installation

Make sure you have Python 3.6 or higher installed.

Install py-crave-sync via pip:

pip install py-crave-sync

---------------------------------------------------------------------------------

# Usage

Running the Server:
After installation, you can start the live server using the following command:

python -m py_crave_sync.server
This will start the server at http://localhost:5000.

---------------------------------------------------------------------------------

# Endpoints

By default, the server provides the following endpoint:

GET /: Returns a JSON message confirming the server is running.
Example response:

Copy code
{
    "message": "Welcome to the live server!"
}

---------------------------------------------------------------------------------

# Dependencies

This project uses the following dependencies:

Flask: A lightweight WSGI web application framework.
These dependencies will be installed automatically when you install the package.

---------------------------------------------------------------------------------

# License

This project is licensed under the MIT License.
