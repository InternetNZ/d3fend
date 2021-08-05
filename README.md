# D3fend
A tool to work with MITRE D3FEND, a knowledge graph of cybersecurity countermeasures.

**NOTE:** Rows 41, 42 and 43 don't have `d3fend-id` as they are in experimental state.

## How to install
To run this script you need `python 3.8+`.

Clone this repository:
```shell
git clone https://github.com/InternetNZ/d3fend.git
```

Create a python virtual environment (Optional):

```shell
cd d3fend
python3 -m venv d3fend-venv
. d3fend-venv/bin/activate
```

Install the dependencies:
```shell
pip3 install -r requirements.txt
```

## How to run the script
The script at the moment has only one functionality which is generating a CSV.

To see the help run:
```shell
./d3fend.py -h
```
```
usage: d3fend.py [-h] {csv} ...

This script is used to load MITER D3FEND ontology and work with it.

optional arguments:
  -h, --help  show this help message and exit

Commands:
  {csv}       Available commands
    csv       Generates CSV file
```

To see the help for `csv` command run:
```shell
./d3fend.py csv -h
```
```
usage: d3fend.py csv [-h] [-o OUTPUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output csv file name. Default 'd3fend.csv'
  -v, --verbose         More verbose
```

To run the script with default values use below command:
```shell
./d3fend.py csv
```

This generates `d3fend.csv` file in the current directory.

## Development
Install development dependencies:

```shell
python3 -n venv d3fend-venv
. d3fend-venv/bin/activate

pip install -r requirements.dev.txt
```

To run the liner:
```shell
./scripts/linter.sh
```

To audit the dependencies:
```shell
./scripts/package-audit.sh
```

To run a security check on the code:
```shell
./scripts/security-check.sh
```

For contributing in project please see [CONTRIBUTING.md](CONTRIBUTING.md) file.
