# Device-Cloud-Hub
#### Devices-API-Storage — IoT Project on Aiohttp [GMA]

The application provides a cloud-based solution for managing IoT devices, offering a reliable and scalable API for interacting with these devices. This project includes CRUD functionality for device management, enabling users to add, update, retrieve, and delete devices, thus supporting their entire lifecycle. The application is deployed with Docker, ensuring ease of installation and portability, as well as a stable environment for interacting with the PostgreSQL database.

#### Stack:
 - Python
 - Aiohttp
 - PostgreSQL
 - Peewee
 - Docker
 - Pytest

Additional libraries are specified in the `requirements.txt` file.

## Project Setup with Docker
In this section, we will deploy the project on PC using Docker and Docker Compose.

### - Cloning a Project from GitHub
Create a root directory on your computer, then open it in your code editor or terminal.
<br>
Next, write this command into the command line:
```powershell
git clone https://github.com/S0fft/Device-Cloud-Hub.git .
```
You will see the project files appear in your directory.

### - Running Docker Desktop and Docker Compose
Afterwards, launch the already installed Docker Desktop. Next, while it is running, you can return to the editor or terminal and enter the following command in the terminal:
```powershell
docker-compose up --build
```
This command "collects and runs all the code", allowing you to interact with the project through a browser.

### - Check by Port
Now the project is already running on your computer, and is available on port 8000.
Go to this address to open it:
```powershell
http://localhost:8000/
```
Thus, we have run the project locally on computer.

### - Functionality Overview
Next, let's look at the functionality of this small project. Implemented CRUD keeping REST architecture in mind.
The goal of the assignment was to implement CRUD for Devices, which was done.
<br>
Below are the routes of this service and what request methods they support:

#### Create, Read (GET / POST)
```powershell
http://localhost:8000/devices/
```
This route supports: GET (All Devices) and POST (the request body must contain a new object that matches the validator, otherwise there will be an error)

#### Read, Update, Delete (GET / PUT / PATCH / DELETE)
```powershell
http://localhost:8000/devices/{id}/
```
This route supports: GET (by ID) to get the item, PUT for major update, PATCH for minor update, DELETE - to completely remove the item.
The routes follow REST architecture.

***Important Note: After deploying a project on a computer, the database is empty, therefore, to retrieve devices via the API, you must create them using the POST method, respecting all database fields. Otherwise, you will receive empty JSON!***

#### Example of a POST Request
```json
{
    "name": "Smart Thermostat",
    "device_type": "Thermostat",
    "login": "thermo_01",
    "password": "securePassword123",
    "location_id": 2,
    "api_user_id": 1
}
```

### - Working With Postman

You can use all of the above addresses in Postman (or other similar tools) by sending requests with different methods (GET, POST, PUT, PATCH, DELETE). This gives you a full opportunity to test the API. <br>

As mentioned before, you can run this project in the browser, but in this case, you will not be able to make POST, PUT, PATCH and DELETE requests. This is because a standard browser, without plugins, does not provide such capabilities when working with Aiohttp. <br>

Therefore, it is highly recommended to use Postman.

### - Recommendations For Improvement
This Aiohttp based API is asynchronous, but it does not take full advantage of it's capabilities due to the synchronous use of the Peewee ORM. To take full advantage of asynchrony, we must use an asynchronous ORM such as Tortoise-ORM or GINO. <br>

Even though all functions in the code are defined as asynchronous (async def), they call synchronous Peewee ORM methods to work with the database. This blocks the main thread of execution while the database executes queries, which violates the core principle of asynchronous programming - not to block the thread of execution. <br>

To improve our code, we can use an asynchronous ORM such as Tortoise-ORM, which fully supports asynchronous operations.

---

<details>
<summary><h3> Project Setup Without Docker </h3></summary>
These commands will help you deploy the project locally. <br>
<br>
 
 ***Important Note: The project is configured to work with Docker. If you use this deployment approach, you need to change the configuration in the .env and app.py files before starting the server. Specifically, you should: Uncomment the necessary commands that are already commented out and replace mutually exclusive lines as needed. These lines are marked in the code. <br> Otherwise, you will receive an error!*** <br>

### - Example of Lines of Code That Need to Be Changed (as shown below)
app.py:
```python
if __name__ == '__main__':
    db.connect()
    db_setup()
    # web.run_app(app, host="0.0.0.0", port=8080)  # Docker - MUST BE COMMENTED
    web.run_app(app, host='127.0.0.1', port=8080)  # Local - MUST BE UNCOMMENTED
```

.env:
```python
DB_NAME=gma_task
DB_USER=postgres
DB_PASSWORD=admin
# DB_HOST=db # Docker - MUST BE COMMENTED
DB_HOST=localhost # Local - MUST BE UNCOMMENTED
DB_PORT=5432
```
### - Routes in Local Development Without Docker
In this approach, the service routes are different, they are listed below.
<br>
#### Create, Read (GET / POST)
```powershell
http://127.0.0.1:8080/devices/
```
#### Read, Update, Delete (GET / PUT / PATCH / DELETE)
```powershell
http://127.0.0.1:8080/devices/{id}/
```
The functionality is the same, the HOST and PORT of the service are just different.

## <p align="center">Windows</p>

### - Installing the Stack
To begin, install: [Python](https://www.python.org/downloads/) | [PostgreSQL](https://www.postgresql.org/) <br> Links are provided to the latest versions of the tools.
<br>

### - Cloning a Project From GitHub
All the same, сreate a root directory on your computer, then open it in your code editor or terminal.
<br>
Next, write this command into the command line:
```powershell
git clone https://github.com/S0fft/Device-Cloud-Hub.git .
```
You will see the project files appear in your directory. After, continue to enter the following commands.

### - Creating a Virtual Environment
Create a virtual environment:
```powershell
python -m venv .venv
```

And activate it:

```powershell
.venv\Scripts\Activate
```

### - Installing the Requirements
Next, install packages:

```powershell
python.exe -m pip install --upgrade pip
```
```powershell
pip install -r requirements.txt
```

<!-- ### Fixtures
Load data from fixture for devices
```powershell
code
``` -->

### - Running the Server
Then, run server:
```powershell
python app.py
```
<br>

<!-- ---------------------------------------------- -->

## <p align="center">UNIX Systems</p>
These commands do the same thing as described above, only on UNIX systems. <br> Before this, the code must be modified as indicated in the note above!
<br>

### - Virtual a Environment
```bash
python3 -m venv ../venv
```

```bash
source ../venv/bin/activate
```

### - Installing the Requirements
```bash
pip3 install --upgrade pip
```
```bash
pip3 install -r requirements.txt
```

<!-- ### Fixtures
```bash
code
``` -->

### - Running the Server
```bash
python3 app.py
```
</details>
