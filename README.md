# conda-history-d

conda plugin which records a detailed history of environments in a history.d directory.

## Dev install

This package can be developed and tested within a conda environment

```
conda create --prefix ./env python=3.9 pip conda
conda activate ./env
python -m pip install -e .
```

With a dev install conda command should be run using

```
python -m conda <commmand>
```

In order to use `conda` for commands first run:

```
eval $(./env/condabin/conda shell.zsh hook)
```

## Usage

Once installed this plugin will automatically record information about each environment
state in a `conda-meta/history.d` directory. For example:

For example:

```
python -m conda create --prefix ./test zlib --yes
python -m conda install --prefix ./test sqlite --yes
tree test/conda-meta/history.d
```
