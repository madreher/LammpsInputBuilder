# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                              |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------------- | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/typedMolecule.py        |       89 |       40 |     55% |19, 22, 25, 28, 31-35, 39-40, 43, 46, 49, 52, 72, 74, 79, 84, 91-92, 99-107, 111-120 |
| python/lammpsinputbuilder/types.py                |       30 |        3 |     90% |30, 35, 38 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/modelToData.py  |      130 |       19 |     85% |35, 39, 94, 114, 133, 155-158, 172, 176-186 |
| python/lammpsinputbuilder/workflowBuilder.py      |       27 |        2 |     93% |    20, 25 |
|                                         **TOTAL** |  **276** |   **64** | **77%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/madreher/LammpsInputBuilder/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/madreher/LammpsInputBuilder/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fmadreher%2FLammpsInputBuilder%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.