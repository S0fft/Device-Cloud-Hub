# Global-Mind-Associated-Task
#### Devices CRUD — CSR (API) GMA-Test-Task-Project on Aiohttp

#### Stack:
 - Pyhton
 - Aiohttp
 - PostgreSQL
 - Peewee
 - Docker
 - Pytest

And also other small libraries specified in requirements.txt

## Deployment with Docker
In this section, we will deploy the project on PC using Docker and Docker Compose.

### Cloning a project from GitHub
Create a root directory on your computer, then open it in your code editor or terminal.
<br>
Next, write this command into the command line:
```powershell
git clone https://github.com/S0fft/Global-Mind-Associated-Task.git .
```
You will see the project files appear in your directory.

### Running Docker Desktop and Docker Compose
Afterwards, launch the already installed Docker Desktop. Next running it, you can return to the editor or terminal and enter the following command in the terminal:
```powershell
docker-compose up --build
```
This command "collects and runs all the code", allowing you to interact with the project through a browser.

### Check by Port
Now the project is already running on your computer, and is available on port 8000.
Go to this address to open it:
```powershell
http://localhost:8000/
```
Thus, we have run the project locally on your computer.

### Functionality overview
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
This route supports: GET (by ID) to get item, PUT to major update, PATCH to minor update, DELETE - to complete remove item.
The routes follow REST architecture.

---

<details>
<summary><h3> Local Deployment Without Docker </h3></summary>
These commands will help you deploy the project locally (without Docker).

## <p align="center">Windows</p>

### Stack Installing
To begin, install: [Python](https://www.python.org/downloads/) | [PostgreSQL](https://www.postgresql.org/) <br> Links are provided to the latest versions of the tools.
<br>

### Cloning a Project From GitHub
Create a root directory on your computer, then open it in your code editor or terminal.
<br>
Next, write this command into the command line:
```powershell
git clone https://github.com/S0fft/Global-Mind-Associated-Task.git .
```
You will see the project files appear in your directory. After, continue to enter the following commands.

### Virtual Environment
Create virtual environment:
```powershell
python -m venv .venv
```

And activate it:

```powershell
.venv\Scripts\Activate
```

### Requirements
Next, install packages:

```powershell
pip install --upgrade pip
```
```powershell
pip install -r requirements.txt
```

<!-- ### Fixtures
Load data from fixture for devices
```powershell
code
``` -->

### Server Rise
Then, run server:
```powershell
python app.py
```
<br>

<!-- ---------------------------------------------- -->

## <p align="center">UNIX Systems</p>
These commands do the same thing as described above, only on UNIX systems.
<br>

### Virtual Environment
```bash
python3 -m venv ../venv
```

```bash
source ../venv/bin/activate
```

### Requirements
```bash
pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

<!-- ### Fixtures
```bash
code
``` -->

### Server Rise
```bash
python3 app.py
```
</details>
