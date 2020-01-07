### Contributing to python-demandapi-client

This is an InnerSource python project. It is the work of someone who thought it might benefit someone else in the company as well.

### Maintainers

This repository is maintained by

1. [Ridley Larsen](@RidleyLarsen)
1. [Bradley Wogsland](@wogsland)

### Community Guidelines

This project follows the [Github Community Guidlines](https://help.github.com/en/github/site-policy/github-community-guidelines). Please feel free to contact the maintainers with any issues.

### Contributing Code

The best place to start is by looking at the [GitHub Issues](https://github.com/dynata/python-demandapi-client/issues) to see what needs to be done. If you decide to take on a task make sure to comment on it so work isn't duplicated. A good PR completely resolves the associated issue, passes python linting, and includes test coverage for your new code. This Github repository is integrated with CircleCI, so a PR cannot be accepted that has merge conflicts, fails to pass linting or tests, or lowers the repository's test coverage. Additionally your PR should include a high level description of your work or reviewers will be peppering you with questions. Approval of the maintainer is required merge a PR into `dev`, which is where all PRs go.

### Linting

Linting software is strongly recommended to improve code quality and maintain readability in Python projects. Python's official linting package is called pycodestyle, but another useful linting package is called flake8. Flake8 runs three different linters on your code, including pycodestyle, and a package called PyFlakes that checks for things like unused imports.

Read more [here](http://flake8.pycqa.org/en/latest/)

To lint the files,

    virtualenv venv
    . venv/bin/activate
    pip install flake8
    flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
    deactivate

### Testing

To run the tests,

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pytest tests
    deactivate

to run the tests for this project.

### Filing Issues

Please use the [GitHub Issues](https://github.com/dynata/python-demandapi-client/issues/new) to file an issue.

Thats it.
