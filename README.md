# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                    |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------------------- | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py               |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/extensions.py                 |      112 |        5 |     96% |18, 21, 51, 93, 134 |
| python/lammpsinputbuilder/fileIO.py                     |      165 |       18 |     89% |23, 26, 29, 34, 37, 40, 43, 46, 49, 88, 106, 118, 144, 157, 169, 178, 196, 219 |
| python/lammpsinputbuilder/group.py                      |      151 |       25 |     83% |23, 26, 41, 48, 59, 90, 111, 152, 158, 170, 189-190, 193, 196, 199, 202-205, 209-212, 215, 218 |
| python/lammpsinputbuilder/instructions.py               |      181 |       25 |     86% |24, 34, 46, 65, 74, 102, 113, 193, 235-240, 243-253 |
| python/lammpsinputbuilder/integrator.py                 |      155 |        6 |     96% |29, 42, 69, 107, 133, 167 |
| python/lammpsinputbuilder/loader/\_\_init\_\_.py        |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/extensionLoader.py     |       18 |       18 |      0% |      1-24 |
| python/lammpsinputbuilder/loader/fileIOLoader.py        |       19 |       19 |      0% |      1-25 |
| python/lammpsinputbuilder/loader/groupLoader.py         |       20 |       20 |      0% |      1-26 |
| python/lammpsinputbuilder/loader/instructionLoader.py   |       19 |       19 |      0% |      1-25 |
| python/lammpsinputbuilder/loader/integratorLoader.py    |       19 |       19 |      0% |      1-25 |
| python/lammpsinputbuilder/loader/sectionLoader.py       |       20 |       20 |      0% |      1-26 |
| python/lammpsinputbuilder/loader/typedMoleculeLoader.py |       16 |       16 |      0% |      1-22 |
| python/lammpsinputbuilder/quantities.py                 |      175 |       16 |     91% |73, 76, 91, 101, 113, 123, 138, 148, 161, 171, 186, 196, 207, 216, 228, 238 |
| python/lammpsinputbuilder/section.py                    |      223 |      139 |     38% |15-18, 21-22, 25-28, 31, 34, 40-44, 47, 50, 53, 56, 59-65, 68-104, 109-147, 161, 164, 167-173, 176-211, 229, 234, 261, 266, 273-274, 277, 280-283, 286-292, 295-299 |
| python/lammpsinputbuilder/typedMolecule.py              |      149 |       21 |     86% |32-37, 55, 58, 61, 64, 67, 93, 95, 103, 114-117, 130, 137, 178, 196, 225 |
| python/lammpsinputbuilder/types.py                      |       62 |       25 |     60% |14-21, 24-33, 46-49, 54-57, 70, 75, 78 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py       |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/modelToData.py        |      145 |       19 |     87% |35, 39, 94, 114, 133, 155-158, 172, 176-186 |
| python/lammpsinputbuilder/workflowBuilder.py            |       40 |        2 |     95% |    20, 32 |
|                                               **TOTAL** | **1689** |  **432** | **74%** |           |


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