# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                      |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------------------- | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py                 |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/extensions.py                   |      164 |       17 |     90% |25-26, 29, 67, 121, 174, 209, 219, 223, 246, 253-256, 259-261 |
| python/lammpsinputbuilder/fileio.py                       |      222 |       22 |     90% |30-31, 34, 37, 92, 116, 124, 132-136, 146-149, 179, 194, 215, 224, 242, 270, 305, 315, 321 |
| python/lammpsinputbuilder/group.py                        |      189 |       19 |     90% |25, 28, 49, 57, 68, 100, 123, 179, 185, 197, 229, 240, 246, 249, 266, 272, 284, 292, 298 |
| python/lammpsinputbuilder/instructions.py                 |      205 |       11 |     95% |29-30, 44, 57, 84, 95, 132, 145, 234, 304, 342 |
| python/lammpsinputbuilder/integrator.py                   |      199 |       10 |     95% |36, 50, 83, 130, 156, 193, 273, 283, 288, 293 |
| python/lammpsinputbuilder/loader/\_\_init\_\_.py          |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/extension\_loader.py     |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/fileio\_loader.py        |       19 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/group\_loader.py         |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/instruction\_loader.py   |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/integrator\_loader.py    |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/section\_loader.py       |       22 |       22 |      0% |      3-32 |
| python/lammpsinputbuilder/loader/typedmolecule\_loader.py |       16 |        0 |    100% |           |
| python/lammpsinputbuilder/quantities.py                   |      176 |       16 |     91% |82, 85, 105, 115, 132, 142, 162, 173, 190, 200, 220, 230, 246, 256, 273, 283 |
| python/lammpsinputbuilder/section.py                      |      228 |      142 |     38% |18-21, 24-25, 28-31, 34-35, 38, 43-47, 50, 53, 56, 59, 62-68, 71-107, 113-152, 165, 168, 174, 177, 180-186, 189-226, 246, 251, 279, 284, 292-293, 296, 299-302, 305-311, 316-323 |
| python/lammpsinputbuilder/typedmolecule.py                |      162 |       26 |     84% |42-47, 68, 71, 78, 82, 109, 118, 120, 129, 141, 144-149, 157-158, 173, 182, 228, 247, 301 |
| python/lammpsinputbuilder/types.py                        |       94 |       35 |     63% |19-26, 30-39, 56-61, 68-71, 85-91, 100, 103, 106, 121, 125, 138 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/model\_to\_data.py      |      162 |       25 |     85% |34, 55, 58-61, 67-68, 130, 157, 182, 213-217, 231, 237-248 |
| python/lammpsinputbuilder/workflow\_builder.py            |       40 |        3 |     92% |23, 28, 36 |
|                                                 **TOTAL** | **1980** |  **348** | **82%** |           |


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