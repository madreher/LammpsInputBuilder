# Dev Section

## Manual build and upload the package on the test repo

Source: https://packaging.python.org/en/latest/tutorials/packaging-projects/

Register an account for testpypi: https://test.pypi.org/account/register/
Register an account for pypi: https://pypi.org/account/register/
Create the file ~/.pypirc and add the token api after generating it in the testpypi and/or pypi account.

The file should look like this:
```
[testpypi]
  username = __token__
  password = <pwd>

[pypi]
  username = __token__
  password = <pwd>
```


Then you can build and upload the package: 

```
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload --repository pypi dist/*
```

The package is available at the address: https://test.pypi.org/project/lammpsinputbuilder/0.0.3/ and https://pypi.org/project/lammpsinputbuilder/0.0.3/

To install the package:
```
python3 -m venv test-lib
source test-lib/bin/activate
pip3 install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple lammpsinputbuilder==0.0.3
# OR
pip3 install -i https://pypi.org/simple/ lammpsinputbuilder==0.0.3
``` 

## Automated Build and Upload package by Github actions

The Github workflow needs to be declared in the test Pypi repo. This can be done here:
- https://test.pypi.org/manage/project/lammpsinputbuilder/settings/publishing/
- https://pypi.org/manage/project/lammpsinputbuilder/settings/publishing/ 

Note: The project should already exists and a version should have been pushed manually once before hand otherwise it seems to cause some token issues.
The version used for the manual upload should also be different than the automated one to avoid trying to upload a file which already exists.

After that, the workflow are implemented following the documentation available here: https://packaging.python.org/en/latest/tutorials/packaging-projects/

To trigger the github workflows, the following conditions must be met:
- The branch name must follow the pattern `test-**` for `test.pypi` and `release-**` for `pypi`. Additionnally, in the case of a release, a tag should also be set with the right version for the package.
- To push the tag: `git push origin tag v0.0.6`