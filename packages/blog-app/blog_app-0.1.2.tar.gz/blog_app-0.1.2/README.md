# Blog Project

## Repository link
[\[repository link\]](https://gitlab.com/y.karzal/2024_assignment2_blogpss)

## Authors
Karzal Youness 879430

Sanvito Marco 886493

## Project Description

This project consists of a blogging platform with a frontend-backend architecture:
- Frontend: HTML/JS client application for blog post viewing and creation
- Backend: Python Flask REST API for post management with timestamp functionality

The application allows users to:
- Create new blog posts with titles and content
- View all posts in chronological order
- Store posts with creation timestamps

[\[API Documentation\]](https://2024-assignment2-blogpss-90c7f9.gitlab.io/)

## Technical Structure

### Frontend
-  HTML/JavaScript implementation
### Backend
- Flask framework for REST API implementation
- SQLite database for post storage
- Key dependencies:
  - `flask`: Web server framework
  - `flask-sqlalchemy`: Database ORM

## Pipeline
Our pipeline consists in the following stages:
- **Build**
- **Verify**
- **Unit-test**
- **Integration-test**
- **Package**
- **Release**
- **Deploy**

Since a lot of jobs use Python as their base layer, our pipeline implements a reusable .python_venv **template** for environment setup. The **cache system** is configured to persist dependencies between jobs, avoiding dependencies from being installed every time. Each job requiring Python extends this template.

The pipeline uses several environment variables to manage configuration, security, and control pipeline behavior.

### Build
- Installs Python dependencies from `requirements.txt`
- Verifies frontend static files
- Executed on all branches

### Verify
Uses parallel jobs for code analysis:
- Static Analysis:
  - Prospector for code quality
  - Configuration set to high strictness
  - Artifacts saved on failure for debugging
- Dynamic Analysis:
  - Bandit for security scanning
  - Custom configuration via pyproject.toml
  - Results stored in SAST report format

### Test
Split into two phases:
- Unit Tests:
  - Backend API endpoint testing
  - Database operations verification
  - Post creation validation
- Integration Tests:
  - End-to-end API testing
  - Frontend-Backend integration
  - Timestamp handling verification

### Package
- Creates distribution packages for backend
- Bundles frontend static files
- Generates:
  - Python wheel package
  - Frontend distribution bundle
- Only runs on main branch and tags

### Release
- Publishes backend package to PyPI
- Deploys frontend static files
- Executed only on main branch
- Uses credentials from GitLab variables

### Docs
- Generates API documentation
- Creates frontend usage guide
- Publishes to GitLab Pages
- Includes:
  - API endpoints documentation
  - Database schema
  - Setup instructions

## Pipeline Artifacts and Reports
The pipeline is configured to store artifacts and reports during the pipeline to enable monitoring and analysis through GitLab's dashboards. 

### Test Results

#### Unit Test Reports

Stored in JUnit XML format
Enables GitLab's test visualization
Tracks test performance across pipeline runs
Command used: pytest backend/tests/unit -v --junitxml=unit_test_output.xml


#### Integration Test Reports

Also stored in JUnit XML format
Shows end-to-end test results
Helps identify integration issues
Command used: pytest backend/tests/integration -v --junitxml=integration_test_output.xml



### Code Analysis Reports

#### Static Analysis (Prospector)

Generates code quality reports
Stored as artifacts on failure
Helps identify problematic code patterns
Available in GitLab's Code Quality dashboard


#### Security Analysis (Bandit)

Produces security scanning reports in JSON format
Integrated with GitLab's Security dashboard
Tracks security vulnerabilities over time
Command used: bandit -r . -f json -o bandit_output.json



### Dashboard Integration
These artifacts are configured to integrate with GitLab's various dashboards:

Test Dashboard: Shows test success rates and performance trends
Code Quality: Displays code issues and their evolution
Security Dashboard: Tracks security vulnerabilities
Pipeline Performance: Monitors job execution times and success rates

### Branch Protection and Version Control


    - if: $CI_COMMIT_TAG && $CI_COMMIT_BRANCH == "main"`


#### Branch Protection Rules
Our project implements protection rules that avoid starting the pipeline by mistake: in our .gitlab-ci.yml, we implement branch restrictions using GitLab's rule system. The pipeline will only be triggered when commits are made to the main branch.

#### Version Control System
To add another layer of security to ensure that we dont trigger the pipeline by accident, we implemented a tag control system that ensures that the pipeline is executed only when a new version of the app is detected. This tag is added manually with the following git command when pushing or merging:

`git tag <tagname> -a`
