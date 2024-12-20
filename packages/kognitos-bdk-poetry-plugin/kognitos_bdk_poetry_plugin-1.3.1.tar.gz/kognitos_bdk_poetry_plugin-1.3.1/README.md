# Poetry Plugin for Book Development Kit

The Poetry plugin for BDK is designed to enhance documentation workflows by automatically generating a comprehensive 
USAGE.md file from the docstrings embedded within a Poetry-managed Python project. This plugin seamlessly integrates 
with the Poetry ecosystem, parsing the docstrings of functions and classes to produce a well-structured and readable 
markdown file that outlines usage examples, input and output concepts, return types, and descriptions.

## Usage

In order to be able to use the plugin, you must first add the BDK repository to Poetry itself:

Edit `~/.config/pypoetry/pyproject.toml` and add the following lines to it:

NOTE: If you are on macOS that path is `~/Library/Application\ Support/pypoetry/pyproject.toml`

```toml
[[tool.poetry.source]]
name = "bdk"
url = "https://kognitos-719468614044.d.codeartifact.us-west-2.amazonaws.com/pypi/bdk/simple/"
priority = "explicit"
```

Authenticate the repository using your AWS credentials (notice the authentication will only last 12 hours):

```shell
poetry config http-basic.bdk aws $(aws codeartifact get-authorization-token --domain-owner 719468614044 --domain kognitos --query 'authorizationToken' --output text)
```

Add the plugin to poetry:

```shell
poetry self add kognitos-bdk-poetry-plugin --source bdk
```

## Build and Contribute

### Prerequisites
Before you begin, ensure you have the following installed on your system:

#### Python 3.11
The project is developed with Python 3.11. We recommend using Pyenv to manage your Python versions.

To manage Python 3.11 with Pyenv, follow these steps:

##### Install Pyenv
If you haven't installed Pyenv yet, you can find the installation instructions on the Pyenv GitHub page. The 
installation process varies depending on your operating system.

##### Install Python 3.11
Once Pyenv is installed, you can install Python 3.11 using the following command:

```shell
pyenv install 3.11.0
```
 
#### Poetry
Poetry is used for dependency management and packaging in this project. 

##### Install Poetry
Run the following command to install Poetry:

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

### Setting Up the Project

#### Clone the Repository
Ensure you have the necessary permissions to access the repository and clone it to your local machine:

```shell
git clone https://github.com/kognitos/bdk.git
cd bdk
```

#### Install Dependencies
Use Poetry to install all required dependencies in an isolated environment:

```shell
poetry install
```

### Building the Project
To build the project, run:

```shell
poetry build
```

### Running Tests
BDK uses Pytest as its test runner. You can execute it using the following command:

```shell
poetry run tests
```

### Formatting Code
BDK uses yapf as its source formatter. You can execute it using the following command:

```shell
poetry run format
```

### Linting Code
BDK uses pylint as its source linter. You can execute it using the following command:

```shell
poetry run lint
```
