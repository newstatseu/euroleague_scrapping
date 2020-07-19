m2r README.md
rm -rf dist/* && python setup.py sdist bdist_wheel
twine upload dist/*