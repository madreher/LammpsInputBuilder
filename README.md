# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                        |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------------ | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py                   |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/base.py                           |       18 |        1 |     94% |        20 |
| python/lammpsinputbuilder/extensions.py                     |      163 |       17 |     90% |24-25, 28, 66, 120, 173, 208, 218, 222, 245, 252-255, 258-260 |
| python/lammpsinputbuilder/fileio.py                         |      217 |       22 |     90% |26-27, 30, 33, 88, 112, 120, 128-132, 142-145, 174, 188, 209, 218, 236, 264, 299, 309, 315 |
| python/lammpsinputbuilder/group.py                          |      186 |       19 |     90% |22, 25, 46, 54, 65, 97, 120, 176, 182, 194, 226, 237, 243, 246, 263, 269, 281, 289, 295 |
| python/lammpsinputbuilder/instructions.py                   |      202 |       11 |     95% |24-25, 39, 52, 79, 90, 127, 140, 229, 299, 337 |
| python/lammpsinputbuilder/integrator.py                     |      196 |        9 |     95% |32, 46, 79, 152, 189, 269, 279, 284, 289 |
| python/lammpsinputbuilder/loader/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/extension\_loader.py       |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/fileio\_loader.py          |       19 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/group\_loader.py           |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/instruction\_loader.py     |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/integrator\_loader.py      |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/section\_loader.py         |       22 |        2 |     91% |    23, 26 |
| python/lammpsinputbuilder/loader/typedmolecule\_loader.py   |       16 |        0 |    100% |           |
| python/lammpsinputbuilder/model/base\_model.py              |        3 |        0 |    100% |           |
| python/lammpsinputbuilder/model/extension\_model.py         |       34 |        0 |    100% |           |
| python/lammpsinputbuilder/model/fileio\_model.py            |       28 |        0 |    100% |           |
| python/lammpsinputbuilder/model/group\_model.py             |       25 |        0 |    100% |           |
| python/lammpsinputbuilder/model/instruction\_model.py       |       33 |        0 |    100% |           |
| python/lammpsinputbuilder/model/integrator\_model.py        |       27 |        0 |    100% |           |
| python/lammpsinputbuilder/model/quantity\_model.py          |       18 |        0 |    100% |           |
| python/lammpsinputbuilder/model/section\_model.py           |       19 |        0 |    100% |           |
| python/lammpsinputbuilder/model/template\_model.py          |       31 |        0 |    100% |           |
| python/lammpsinputbuilder/model/typedmolecule\_model.py     |       14 |        0 |    100% |           |
| python/lammpsinputbuilder/model/workflow\_builder\_model.py |       12 |        0 |    100% |           |
| python/lammpsinputbuilder/quantities.py                     |      176 |       16 |     91% |82, 85, 105, 115, 132, 142, 162, 173, 190, 200, 220, 230, 246, 256, 273, 283 |
| python/lammpsinputbuilder/section.py                        |      270 |       12 |     96% |23, 31-34, 37-38, 41, 57, 200, 239, 242 |
| python/lammpsinputbuilder/templates/minimize\_template.py   |       60 |        1 |     98% |        66 |
| python/lammpsinputbuilder/templates/template\_section.py    |       98 |        0 |    100% |           |
| python/lammpsinputbuilder/typedmolecule.py                  |      162 |       26 |     84% |42-47, 68, 71, 78, 82, 109, 118, 120, 129, 141, 144-149, 158-159, 174, 183, 229, 248, 302 |
| python/lammpsinputbuilder/types.py                          |       83 |        3 |     96% |93, 97, 110 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/model\_to\_data.py        |      162 |       25 |     85% |34, 55, 58-61, 67-68, 130, 157, 182, 213-217, 231, 237-248 |
| python/lammpsinputbuilder/utility/string\_utils.py          |        4 |        0 |    100% |           |
| python/lammpsinputbuilder/version.py                        |       15 |        2 |     87% |    11, 14 |
| python/lammpsinputbuilder/workflow\_builder.py              |       77 |       10 |     87% |25, 30, 41, 98, 102, 106, 109, 113, 117, 120 |
|                                                   **TOTAL** | **2472** |  **176** | **93%** |           |


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