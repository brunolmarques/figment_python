Your task is to provide some basic aggregation, based on data from Ethereum network.
Input file (stored as git-lfs in repository) in input_data directory contains information about validators in ETH2 from selected blocks.

Process the file by using any tool/library which you want, but it should be orchestrated in Python language.
Please provide following aggregations:

Per block:
* total balance for all validators
* total effective balance for all validators
* Number of slashed validators
* Number of validators per status

Total aggregation for all blocks:
* total balance for all validators
* total effective balance for all validators
* Number of slashed validators
* Number of validators per status

Whole process should be as automated as possible. Readme file should be updated with instruction
how to run the pipeline.

Output structure is defined in verify.py file which can be used to verify correctness of the result.

Solution should be sent as tar archive on Greenhouse platform (with input data removed to reduce the size)

## Project Structure
.
├── .devcontainer
│   ├── git-aliases.conf
│   └── devcontainer.json
├── .github
│   └── workflows
│       └── ci.yml
├── input_data
│   └── validators_data.json.gz
├── src
│   ├── aggregator.py
│   ├── config.py
│   ├── logger.py
│   └── utils.py
├── tests
│   └── test_aggregator.py
├── Makefile
├── README.md
├── requirements.txt
└── verify.py

