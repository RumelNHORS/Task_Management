# Task Management Project

This project is a simple project for task management.

## Getting Started

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.x
- PostgreSQL

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/RumelNHORS/Task_Management.git
    ```

2. **Navigate to the main project directory:**
    ```sh
    cd Task_Management/task_management
    ```

3. **Create a Python virtual environment:**
    ```sh
    python -m venv env
    ```

4. **Activate the virtual environment:**
    - On Windows:
        ```sh
        .\env\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source env/bin/activate
        ```

5. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

6. **Set up the PostgreSQL database:**
    - Create a new PostgreSQL database.
    - Update the database settings in the `settings.py` file with your database credentials.

7. **Make migrations and migrate:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

8. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

Your task management project should now be running locally. Open your web browser and navigate to `http://127.0.0.1:8000/` to view the application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

On Going...