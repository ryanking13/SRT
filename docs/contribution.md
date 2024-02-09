# Contributing

You can contribute to `SRTrain` by:

- **Reporting bugs**: please report when bug occurred through [github issue](https://github.com/ryanking13/SRT/issues).
- **Fixing bugs**: when you fixes a bug, please run tests before submitting a PR.
- **Enhancing documentations**: SRTrain uses Sphinx + Markdown for documentation.
- **Adding/Proposing new features**

## How to run tests

```sh
export SRT_USERNAME=<YOUR_SRT_USERNAME>
export SRT_PASSWORD=<YOUR_SRT_PASSWORD>

# For Windows
# set SRT_USERNAME=<YOUR_SRT_USERNAME>
# set SRT_PASSWORD=<YOUR_SRT_PASSWORD>

pip install -e ".[test]"

pre-commit run --all-files
pytest SRT -v -x

# For full test
# Warning: 아래 테스트에는 실제로 표를 예약/취소하는 테스트가 포함되어 있습니다
pytest SRT -v -x --full
```

## How to build the documentation

```
pip install requirements/docs.txt
cd docs/
make html
```
