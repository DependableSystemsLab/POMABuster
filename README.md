# POMABuster
POMABuster is an automated engine to detect Price Oracle Manipualtion Attack (POMA) to blockchain oracles.
For more details about POMABuster, please refer to the paper [POMABuster: Detecting Price Oracle Manipulation Attacks in Decentralized Finance](https://sp2024.ieee-security.org/) (link to be announce).

If you use POMABuster, please cite this paper
```
TBA
```

## Dataset Availability
All our datasets are publicly available:
- The transaction dataset is stored separated on [Zenodo](https://zenodo.org/records/10359283). You can also obtain it from [Google BigQuery](https://evgemedvedev.medium.com/ethereum-blockchain-on-google-bigquery-283fb300f579) or run [Etehreum-ETL](https://ethereum-etl.readthedocs.io/en/latest/quickstart/) on your local Ethereum node.
- The code4rena dataset is available under the `dataset` folder of this repo. The source are from an ICSE'23 paper, [Demystifying Exploitable Bugs in Smart Contracts](https://github.com/ZhangZhuoSJTU/Web3Bugs).
- The ERC20 token/tokenholder dataset are crawled from [Etherscan](https://etherscan.io/). Scripts are available at the `src/tokens/erc20` folder.

## Quick Start

1. Download the transaction dataset
2. Run the ERC20 token/tokenholder scripts
```
cd src/tokens/erc20
scrapy crawl ERC20 -o erc20.jsonlines
scrapy crawl holder -o holder.jsonlines
```
3. Run the notebooks in the following order
    1. `pomabuster.ipynb`
    2. `linking.ipynb`
