# Blog Application

A simple blog application built with Flask.

## Features

- View all blog posts
- Add new posts
- Automatic timestamps for each post

## Package Structure

```
blog-app/
├── __init__.py
├── config.py
├── database.py
└── posts.py
```

## Setup with PyPI Package

1. Install the package
    ```bash
    pip install blog-app
    ```

2. Run the application
    ```bash
    python blog-app
    ```
   
3. Done
   - The API will be available at `http://localhost:5000`

## Setup with Source Code

1. Clone the repository
    ```bash
    git https://gitlab.com/y.karzal/2024_assignment2_blogpss
    cd 2024_assignment2_blogpss
    ```

2. Set up the application
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the application
    ```bash
    python run.py
    ```

4. Done
   - The API will be available at `http://localhost:5000`

## Testing (Unit and Integration) with Source Code

install pytest:
```bash
pip install pytest
```

Run backend unit tests:
```bash
pytest tests/unit
```

Run backend integration tests:
```bash
pytest tests/integration
```
