# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glyles',
 'glyles.glycans',
 'glyles.glycans.factory',
 'glyles.glycans.mono',
 'glyles.glycans.poly',
 'glyles.grammar']

package_data = \
{'': ['*']}

install_requires = \
['antlr4-python3-runtime==4.13.1',
 'joblib>=1.2.0,<2.0.0',
 'networkx>=2.6.3',
 'numpy',
 'pydot>=1.4.2,<2.0.0',
 'rdkit>=2021.9.2']

entry_points = \
{'console_scripts': ['glyles = glyles.__main__:main']}

setup_kwargs = {
    'name': 'glyles',
    'version': '1.1.0',
    'description': 'A tool to convert IUPAC representation of glycans into SMILES strings',
    'long_description': '# GlyLES\n\n![testing](https://github.com/kalininalab/glyles/actions/workflows/test.yaml/badge.svg)\n[![docs-image](https://readthedocs.org/projects/glyles/badge/?version=latest)](https://glyles.readthedocs.io/en/latest/)\n[![piwheels](https://img.shields.io/piwheels/v/glyles)](https://pypi.org/project/glyles/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/glyles)](https://pypi.org/project/glyles/)\n[![codecov](https://codecov.io/gh/kalininalab/GlyLES/branch/main/graph/badge.svg)](https://codecov.io/gh/kalininalab/glyles)\n[![DOI](https://zenodo.org/badge/431874597.svg)](https://zenodo.org/badge/latestdoi/431874597)\n\nA tool to convert IUPAC representation of Glycans into SMILES representation. This repo is still in the development \nphase; so, feel free to report any errors or issues. The code is available on \n[github](https://github.com/kalininalab/GlyLES/) and the documentation can be found on \n[ReadTheDocs](https://glyles.readthedocs.io/en/latest/index.html).\n\n## Specification and (current) Limitations\n\nThe exact specification we\'re referring to when talking about "IUPAC representations of glycan" or "IUPAC-condensed", \nis given in the "Notes" section of this [website](https://www.ncbi.nlm.nih.gov/glycans/snfg.html). But as this package \nis still in the development phase, not everything of the specification is implemented yet (especially not all side \nchains you can attach to monomers). The structure of the glycan can be represented as a tree of the monosaccharides \nwith maximal branching factor 4, i.e., each monomer in the glycan has at most 4 children.\n\n## Installation\n\nSo far, this package can only be downloaded from the python package index. So the installation with `pip` is very easy.\nJust type\n\n``````shell\npip install glyles\n``````\n\nand you\'re ready to use it as described below. Use \n\n``````shell\npip install --upgrade glyles\n``````\n\nto upgrade the glyles package to the most recent version.\n\n## Basic Usage\n\n### As a Python Package\n\nConvert the IUPAC into a SMILES representation using the handy `convert` method\n\n``````python\nfrom glyles import convert\n\nconvert(glycan="Man(a1-2)Man", output_file="./test.txt")\n``````\n\nYou can also use the `convert_generator` method to get a generator for all SMILES:\n\n``````python\nfrom glyles import convert_generator\n\nfor smiles in convert_generator(glycan_list=["Man(a1-2)Man a", "Man(a1-2)Man b"]):\n    print(smiles)\n``````\n\nFor more examples of how to use this package, please see the notebooks in the \n[examples](https://github.com/kalininalab/GlyLES/tree/dev/examples) folder and checkout the documentation on \n[ReadTheDocs](https://glyles.readthedocs.io/en/latest/index.html).\n\n### In the Commandline\n\nAs of version 0.5.9, there is a commandline interface to GlyLES which is automatically installed when installing GlyLES \nthrough pip. The CLI is open for one or multiple IUPAC inputs as individual arguments. Due to the syntax of the \nIUPAC-condensed notation and the argument parsing in commandlines, the IUPAC strings must be given in quotes.\n\n``````shell\nglyles -i "Man(a1-2)Man" -o test_output.txt\nglyles -i "Man(a1-2)Man" "Fuc(a1-6)Glc" -o test_output.txt\n``````\n\nFile-input is also possible.\n``````shell\nglyles -i input_file.txt -o test_output.txt\n``````\n\nProviding multiple files and IUPAC-condensed names is als supported.\n``````shell\nglyles -i input_file1.txt "Man(a1-2)Man" input_file2.txt input_file13.txt "Fuc(a1-6)Glc" -o test_output.txt\n``````\n\n## Notation of glycans\n\nThere are multiple different notations for glycans in IUPAC. So, according to the \n[SNGF specification](https://www.ncbi.nlm.nih.gov/glycans/snfg.html), `Man(a1-4)Gal`, `Mana1-4Gal`, and `Mana4Gal` \nall describe the same disaccharide. This is also covered in this package as all three notations will be parsed into the \nsame tree of monosaccharides and result in the same SMILES string.\n\nThis is also described more detailed in a section on [ReadTheDocs](https://glyles.readthedocs.io/en/latest/notes/notation.html).\n\n## Poetry\n\nTo develop this package, we use the poetry package manager (see [here](https://python-poetry.org/) for detailed\ninstruction). It has basically the same functionality as conda but supports the package management better and also \nsupports distinguishing packages into those that are needed to use the package and those that are needed in the \ndevelopment of the package. To enable others to work on this repository, we also publish the exact \nspecifications of our poetry environment.\n\n## Citation\n\nIf you use GlyLES in your work, please cite\n```\n@article{joeres2023glyles,\n  title={GlyLES: Grammar-based Parsing of Glycans from IUPAC-condensed to SMILES},\n  author={Joeres, Roman and Bojar, Daniel and Kalinina, Olga V},\n  journal={Journal of Cheminformatics},\n  volume={15},\n  number={1},\n  pages={1--11},\n  year={2023},\n  publisher={BioMed Central}\n}\n```\n',
    'author': 'Roman Joeres',
    'author_email': 'roman.joeres@helmholtz-hips.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kalininalab/GlyLES',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
