# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                    |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------------------- | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py               |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/extensions.py                 |      112 |        5 |     96% |18, 21, 51, 93, 134 |
| python/lammpsinputbuilder/fileIO.py                     |      144 |      103 |     28% |8, 11-14, 17, 20, 23, 26, 31, 34, 37, 40, 43, 46, 52-57, 60-66, 69-76, 79-94, 97, 100, 106-109, 112-117, 120-125, 128, 131, 134, 139-143, 146, 149, 152, 155-160, 163-168, 171-181, 184, 187 |
| python/lammpsinputbuilder/group.py                      |       89 |       55 |     38% |12-15, 19, 22, 25, 30-31, 34-37, 41-44, 47-54, 57, 67-69, 75-79, 83-91, 94-98, 101, 108-110, 114-116, 119, 122 |
| python/lammpsinputbuilder/integrator.py                 |      139 |       95 |     32% |11, 14-16, 19, 22, 25, 28, 35-37, 40-42, 45, 49-51, 54-58, 61-65, 69, 72, 75, 86-91, 94-101, 104-111, 114, 117, 120-122, 125, 130, 133-135, 138-140, 143, 146, 149-182 |
| python/lammpsinputbuilder/loader/\_\_init\_\_.py        |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/computationLoader.py   |       17 |       17 |      0% |      1-23 |
| python/lammpsinputbuilder/loader/fileIOLoader.py        |       19 |       19 |      0% |      1-25 |
| python/lammpsinputbuilder/loader/integratorLoader.py    |       17 |       17 |      0% |      1-23 |
| python/lammpsinputbuilder/loader/sectionLoader.py       |       18 |       18 |      0% |      1-24 |
| python/lammpsinputbuilder/loader/typedMoleculeLoader.py |       16 |       16 |      0% |      1-22 |
| python/lammpsinputbuilder/quantities.py                 |      175 |       16 |     91% |73, 76, 91, 101, 113, 123, 138, 148, 161, 171, 186, 196, 207, 216, 228, 238 |
| python/lammpsinputbuilder/section.py                    |       96 |       65 |     32% |9, 12-15, 18-19, 22-25, 28, 31, 37-38, 41, 44-47, 50-51, 54, 57, 61-63, 66, 69-72, 75-83, 86-91, 94-98, 102-106, 110-111, 114, 117-120, 123-124 |
| python/lammpsinputbuilder/typedMolecule.py              |      125 |       14 |     89% |43, 46, 49, 52, 74, 76, 84, 95-98, 109, 116, 146, 164 |
| python/lammpsinputbuilder/types.py                      |       62 |       27 |     56% |14-21, 24-33, 46-49, 52-57, 70, 75, 78 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py       |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/modelToData.py        |      130 |       19 |     85% |35, 39, 94, 114, 133, 155-158, 172, 176-186 |
| python/lammpsinputbuilder/workflowBuilder.py            |       40 |        5 |     88% |20, 24, 27, 32, 59 |
|                                               **TOTAL** | **1199** |  **491** | **59%** |           |


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