# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                      |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------------------- | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py                 |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/extensions.py                   |      166 |       17 |     90% |28-29, 32, 70, 124, 177, 212, 222, 226, 249, 256-259, 262-264 |
| python/lammpsinputbuilder/fileio.py                       |      222 |       22 |     90% |30-31, 34, 37, 92, 116, 124, 132-136, 146-149, 179, 194, 215, 224, 242, 270, 305, 315, 321 |
| python/lammpsinputbuilder/group.py                        |      189 |       19 |     90% |25, 28, 49, 57, 68, 100, 123, 179, 185, 197, 229, 240, 246, 249, 266, 272, 284, 292, 298 |
| python/lammpsinputbuilder/instructions.py                 |      205 |       11 |     95% |29-30, 44, 57, 84, 95, 132, 145, 234, 304, 342 |
| python/lammpsinputbuilder/integrator.py                   |      199 |        9 |     95% |36, 50, 83, 156, 193, 273, 283, 288, 293 |
| python/lammpsinputbuilder/loader/\_\_init\_\_.py          |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/extension\_loader.py     |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/fileio\_loader.py        |       19 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/group\_loader.py         |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/instruction\_loader.py   |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/integrator\_loader.py    |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/section\_loader.py       |       22 |        2 |     91% |    23, 26 |
| python/lammpsinputbuilder/loader/typedmolecule\_loader.py |       16 |        0 |    100% |           |
| python/lammpsinputbuilder/quantities.py                   |      176 |       16 |     91% |82, 85, 105, 115, 132, 142, 162, 173, 190, 200, 220, 230, 246, 256, 273, 283 |
| python/lammpsinputbuilder/section.py                      |      272 |       12 |     96% |21, 34-37, 40-41, 44, 60, 204, 243, 246 |
| python/lammpsinputbuilder/templates/minimize\_template.py |       60 |        1 |     98% |        66 |
| python/lammpsinputbuilder/templates/template\_section.py  |       97 |        0 |    100% |           |
| python/lammpsinputbuilder/typedmolecule.py                |      162 |       26 |     84% |42-47, 68, 71, 78, 82, 109, 118, 120, 129, 141, 144-149, 157-158, 173, 182, 228, 247, 301 |
| python/lammpsinputbuilder/types.py                        |       83 |        3 |     96% |93, 97, 110 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/model\_to\_data.py      |      162 |       25 |     85% |34, 55, 58-61, 67-68, 130, 157, 182, 213-217, 231, 237-248 |
| python/lammpsinputbuilder/workflow\_builder.py            |       40 |        3 |     92% |23, 28, 36 |
|                                                 **TOTAL** | **2172** |  **166** | **92%** |           |


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