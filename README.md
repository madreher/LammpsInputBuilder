# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/madreher/LammpsInputBuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                        |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------------ | -------: | -------: | ------: | --------: |
| python/lammpsinputbuilder/\_\_init\_\_.py                   |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/base.py                           |       20 |        3 |     85% | 60-61, 90 |
| python/lammpsinputbuilder/extensions.py                     |      173 |       19 |     89% |73-74, 87, 131, 167, 179, 278, 391, 477, 497, 509, 572, 591-594, 603-605 |
| python/lammpsinputbuilder/fileio.py                         |      218 |       22 |     90% |74-75, 88, 98, 222, 260, 268, 276-280, 303-306, 380, 414, 462, 491, 537, 584, 676, 695, 707 |
| python/lammpsinputbuilder/group.py                          |      190 |       22 |     88% |69, 82, 131, 157-158, 188, 264, 330, 449-450, 474-475, 506, 587, 617, 630, 640, 688, 709, 740, 754, 766 |
| python/lammpsinputbuilder/instructions.py                   |      205 |       11 |     95% |59-60, 102, 140, 209, 239, 332, 364, 514, 625, 715 |
| python/lammpsinputbuilder/integrator.py                     |      196 |       10 |     95% |84, 131, 220, 380, 382, 466, 615, 632, 642, 652 |
| python/lammpsinputbuilder/loader/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/extension\_loader.py       |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/fileio\_loader.py          |       19 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/group\_loader.py           |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/instruction\_loader.py     |       21 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/integrator\_loader.py      |       20 |        0 |    100% |           |
| python/lammpsinputbuilder/loader/section\_loader.py         |       22 |        2 |     91% |    23, 26 |
| python/lammpsinputbuilder/loader/typedmolecule\_loader.py   |       17 |        0 |    100% |           |
| python/lammpsinputbuilder/model/base\_model.py              |        3 |        0 |    100% |           |
| python/lammpsinputbuilder/model/extension\_model.py         |       49 |        0 |    100% |           |
| python/lammpsinputbuilder/model/fileio\_model.py            |       37 |        0 |    100% |           |
| python/lammpsinputbuilder/model/group\_model.py             |       43 |        0 |    100% |           |
| python/lammpsinputbuilder/model/instruction\_model.py       |       51 |        0 |    100% |           |
| python/lammpsinputbuilder/model/integrator\_model.py        |       42 |        0 |    100% |           |
| python/lammpsinputbuilder/model/quantity\_model.py          |       42 |        0 |    100% |           |
| python/lammpsinputbuilder/model/section\_model.py           |       27 |        0 |    100% |           |
| python/lammpsinputbuilder/model/template\_model.py          |       41 |        0 |    100% |           |
| python/lammpsinputbuilder/model/typedmolecule\_model.py     |       23 |        0 |    100% |           |
| python/lammpsinputbuilder/model/workflow\_builder\_model.py |       18 |        0 |    100% |           |
| python/lammpsinputbuilder/quantities.py                     |      176 |       15 |     91% |155, 196, 215, 251, 270, 310, 330, 367, 386, 427, 446, 483, 502, 539, 558 |
| python/lammpsinputbuilder/section.py                        |      291 |       13 |     96% |64-65, 85-88, 98-99, 107, 161, 418, 546, 549 |
| python/lammpsinputbuilder/templates/minimize\_template.py   |       60 |        1 |     98% |        66 |
| python/lammpsinputbuilder/templates/template\_section.py    |       98 |        0 |    100% |           |
| python/lammpsinputbuilder/typedmolecule.py                  |      280 |       43 |     85% |87-92, 129, 141, 158, 168, 214, 244, 246, 255, 267, 270-275, 284-285, 319, 328, 432, 470, 566, 650, 652, 661, 674, 677-682, 691-692, 719, 729, 766, 829, 861, 868 |
| python/lammpsinputbuilder/types.py                          |       83 |        3 |     96% |93, 97, 110 |
| python/lammpsinputbuilder/utility/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| python/lammpsinputbuilder/utility/model\_to\_data.py        |      172 |       20 |     88% |34, 55, 58-61, 67-68, 130, 157, 182, 217, 231, 237, 240-241, 246-248, 274, 278 |
| python/lammpsinputbuilder/utility/string\_utils.py          |        4 |        0 |    100% |           |
| python/lammpsinputbuilder/version.py                        |       15 |        2 |     87% |    11, 14 |
| python/lammpsinputbuilder/workflow\_builder.py              |       79 |       11 |     86% |46, 58, 100, 179, 184, 188, 192, 195, 199, 203, 206 |
|                                                   **TOTAL** | **2776** |  **197** | **93%** |           |


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