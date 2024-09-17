# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                    |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------------------- | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py               |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/extensions.py                 |      113 |        5 |     96% |19, 22, 52, 94, 135 |
| python/lammpsinputbuilder/fileIO.py                     |      194 |       24 |     88% |25, 28, 31, 36, 39, 42, 45, 48, 51, 95, 118, 126, 131-134, 144-147, 173, 186, 198, 207, 225, 251 |
| python/lammpsinputbuilder/group.py                      |      151 |       25 |     83% |23, 26, 41, 48, 59, 90, 111, 152, 158, 170, 189-190, 193, 196, 199, 202-205, 209-212, 215, 218 |
| python/lammpsinputbuilder/instructions.py               |      182 |       25 |     86% |25, 35, 47, 66, 75, 103, 114, 194, 236-241, 244-254 |
| python/lammpsinputbuilder/integrator.py                 |      156 |        6 |     96% |30, 43, 70, 108, 134, 168 |
| python/lammpsinputbuilder/loader/\_\_init\_\_.py        |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/extensionLoader.py     |       18 |       18 |      0% |      1-24 |
| python/lammpsinputbuilder/loader/fileIOLoader.py        |       19 |       19 |      0% |      1-25 |
| python/lammpsinputbuilder/loader/groupLoader.py         |       20 |       20 |      0% |      1-26 |
| python/lammpsinputbuilder/loader/instructionLoader.py   |       19 |       19 |      0% |      1-25 |
| python/lammpsinputbuilder/loader/integratorLoader.py    |       19 |       19 |      0% |      1-25 |
| python/lammpsinputbuilder/loader/sectionLoader.py       |       20 |       20 |      0% |      1-26 |
| python/lammpsinputbuilder/loader/typedMoleculeLoader.py |       16 |       16 |      0% |      1-22 |
| python/lammpsinputbuilder/quantities.py                 |      175 |       16 |     91% |73, 76, 91, 101, 113, 123, 138, 148, 161, 171, 186, 196, 207, 216, 228, 238 |
| python/lammpsinputbuilder/section.py                    |      228 |      141 |     38% |16-19, 22-23, 26-29, 32, 35, 41-45, 48, 51, 54, 57, 60-66, 69-105, 110-148, 159, 162, 168, 171, 174-180, 183-218, 236, 241, 268, 273, 280-281, 284, 287-290, 293-299, 302-306 |
| python/lammpsinputbuilder/typedMolecule.py              |      161 |       30 |     81% |33-38, 56, 59, 62, 65, 68, 89, 94, 96, 104, 114, 117-122, 129-130, 139, 146, 169-171, 192, 210, 239 |
| python/lammpsinputbuilder/types.py                      |       94 |       35 |     63% |15-22, 25-34, 48-53, 58-61, 72-76, 79, 82, 85, 99, 103, 108 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py       |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/modelToData.py        |      160 |       24 |     85% |39, 42-45, 51-52, 106, 126, 149, 172-176, 190, 194-204 |
| python/lammpsinputbuilder/workflowBuilder.py            |       40 |        3 |     92% |21, 25, 33 |
|                                               **TOTAL** | **1785** |  **465** | **74%** |           |


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