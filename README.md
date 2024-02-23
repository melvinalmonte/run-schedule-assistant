# Rutgers Schedule Assistant API

The Rutgers Schedule Assistant API is a FastAPI application designed to interact with the Rutgers Schedule of Classes API. It fetches data from the Rutgers API and processes it to return a more user-friendly response. This processed data can be easily utilized to build various tools or integrated into AI models. The goal of this application is to simplify the data from the Rutgers API, making it more accessible and easier to work with for developers and users alike.

## Requirements

- **Python**: Latest version of python is needed (3.12)
- **PDM**: Python Dependency Manager...Can be downloaded [here](https://pdm-project.org/latest/).

## Setup

1. **Clone the Project**:

    ```sh
    git clone git@github.com:melvinalmonte/run-schedule-assistant.git
    cd run-schedule-assistant
    ```

2. **Install Dependencies**: This assumes you have your virtual environment setup

   Install dependencies

    ```sh
    pdm install
    ```

3. **Run the Project**: From root
    
    ```sh
    python ./src/run_schedule_assistant/main.py
    ```

TODO:
* Enhance logging
* Enhance error handling
* Integrate alerts