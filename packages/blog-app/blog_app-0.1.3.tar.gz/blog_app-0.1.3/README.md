# Blog Project

## Repository links
[\[old repository link\]](https://gitlab.com/y.karzal/2024_assignment2_blogpss)

[\[new repository link\]](https://gitlab.com/m.sanvito17/2024_assignment2_blogpss2)

## Authors
Karzal Youness 879430

Sanvito Marco 886493

## Project Description

This project consists of a blogging platform with a frontend-backend architecture:
- Frontend: `HTML/JS` client application for blog post viewing and creation
- Backend: `Python Flask` REST API for post management with timestamp functionality

The application allows users to:
- **Create** new blog posts with titles and content
- **View** all posts in chronological order
- **Store** posts with creation timestamps

[\[API Documentation\]](https://2024-assignment2-blogpss-90c7f9.gitlab.io/)

## Technical Structure

### Frontend
-  `HTML/JavaScript` implementation
### Backend
- `Flask` framework for REST API implementation
- `SQLite` database for post storage
- Key dependencies:
  - `flask`: Web server framework
  - `flask-sqlalchemy`: Database ORM

## Pipeline
Our pipeline consists in the following stages:
- **Build**
- **Verify**
- **test**
- **Package**
- **Release**
- **Docs**
- **Deploy**

### Visual representation of the pipeline
![Pipeline image](/images/pipeline.png)

### Development and pipeline's execution
We divided our project mainly in 2 **branches**:
 - **main**: The main branch serves as our production environment branch, representing the stable and deployable state of our application. It includes the complete pipeline execution with deployment to the production environment.
 - **develop**: The develop branch is our primary integration branch.


The main branch executes the complete pipeline sequence, the develop branch diverges from main after testing, as it skips the package and release stages. Documentation generation is also bypassed on develop, and instead of deploying to production, the pipeline deploys to a staging environment.

### Configurations usage in our project
Since a lot of jobs use Python and Node.js as their base layers, our pipeline implements two reusable **configurations**: `.python_venv` for Python environment setup and `.npm_cache` for Node.js environment setup. The **cache system** is configured to persist dependencies between jobs for both environments, using distinct cache keys to avoid dependencies from being installed every time. Each job requiring Python extends the .python_venv configuration, while frontend-related jobs that require Node.js extend the .npm_cache configuration. 

The pipeline optimizes performance by storing Python packages in .cache/pip and npm packages in .cache/npm

### Environment variables
The pipeline uses several environment variables to manage configuration, security, and control pipeline behavior.


### Build
- Installs Python dependencies from `requirements.txt`
- Executed on all branches

### Verify
Uses parallel jobs for code analysis:
- Static Analysis:
  - `Prospector` for code quality of .py files
    - we divide pylint from prospector to get the code quality report
  - `Eslint` for code quality of .js files 
  - `Htmlhint` for code quality of .html files
  - `stylelint` for code quality of .css files
  - Artifacts saved on failure for debugging
- Dynamic Analysis:
  - `Bandit` for security scanning
  - Custom configuration via pyproject.toml
  - Results stored in SAST report format

We implemented a mechanism to avoid the verify stage if there are no changes in the app files, since there is no reason to verify them again.
  
  `rules`:

    - changes:
        paths:
          - run.py
          - blog_app/**/*.py

### Test
For the test stage we split the job into two phases:
- **Unit Tests**:
  - Backend API endpoint testing
  - Database operations verification
  - Post creation validation
- **Integration Tests**:
  - End-to-end API testing
  - Frontend-Backend integration
  - Timestamp handling verification

The **unit testing**'s job is to verify the correct result of a single "unit", for this task we use `pytest`

The **integration testing**'s job is to verify that the interface between our modules works correcly, for this task we use `pytest`

### Package
In the package stage we aim to create a wheel (`.whl`) and a source distribution(`.tar.gz`): a directory /dist is created where both zip and wheel are stored. The folder is saved as an artifact and used in the following step of the pipeline.
- Creates distribution packages for app
- Bundles frontend static files
- Generates:
  - Python `wheel` package
  - Create distribution bundle
- Only runs on main branch

### Release
- Publishes app package to `PyPI`

For the release of our project we use `twine` to upload the package to `PyPi`. We use Gitlab's variables to store twine's credentials:

![twine credentials](/images/twine_credentials.png)

The variables are stored as **Protected** and **Hidden** in the dashboard.

### Docs
This job use `MkDocs` to automate the creation and deployment of project documentation. The documentation generation flow consists of the following steps:
- Generates API documentation
- Creates frontend usage guide
- Publishes to **GitLab Pages**
- Includes:
  - API endpoints documentation
  - Setup instructions

### Deploy
The deployment process leverages `render.com`'s webhook system for automated deployments. Each environment (staging and production) has its own dedicated webhook URL that triggers a deployment when called.

During this phase the environment variables for this job are protected and hidden, and based on the current envirnoment.

#### Deployment Environments

- **Staging Environment**: Automatically deploys when changes are pushed to the `develop` branch

- **Production Environment**: Automatically deploys when changes are pushed to the `main` branch

When code is merged into either the `develop` or `main` branch, the corresponding webhook is triggered

The deployment configuration is maintained in render.yaml, which contains environment-specific settings and deployment parameters for both staging and production environments.

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

#### Static Analysis (Pylint)

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

- Test Dashboard: Shows test success rates and performance trends
![test dashboard](/images/testsfailed.png)
- Code Quality: Displays code issues and their evolution
![code quality dashboard](/images/codequality_dashboard.png)
- Security Dashboard: Tracks security vulnerabilities
- Pipeline Performance: Monitors job execution times and success rates

The artifacts expire after 30 days. All the artifacts that are **not** reports are only saved on failure.

### Branch Protection 
  `rules`:

    - if:  $CI_COMMIT_BRANCH == "main"`


#### Branch Protection Rules
Our project implements protection rules that avoid starting the pipeline by mistake: in our .gitlab-ci.yml, we implement branch restrictions using GitLab's rule system. The pipeline will only be triggered when commits are made to the main branch.

###  Workflow 
For the pipeline to start the commit needs to be on a protected branch or a merge request (not a draft)