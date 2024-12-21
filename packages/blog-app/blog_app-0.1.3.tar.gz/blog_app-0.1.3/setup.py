from setuptools import setup, find_packages

with open("PYPI_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blog-app",
    version="0.1.3",
    author="Team IT",
    author_email="y.karzal@campus.unimib.it",
    description="A simple blog application with Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/m.sanvito17/2024_assignment2_blogpss2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires=">=3.11",
    install_requires=[
        'flask>=3.1.0',
        'flask-sqlalchemy>=3.1.1',
        'flask-cors>=5.0.0',
        'python-dotenv>=1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'blog-app=blog_app:run',
        ],
    },
)
