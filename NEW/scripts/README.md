# Tournament by Rocket Capital Investment 
___
## < *For internal use.* >
Python >= 3.8 is required for these scripts to run.
1. Download the [scripts](https://github.com/rocketcapital-ai/tournament-contract/tree/main/scripts) folder.
2. From within the [scripts](https://github.com/rocketcapital-ai/tournament-contract/tree/main/scripts) folder, do a `pip install` on the latest `.whl` file inside the `dist` folder. For example: 
> pip install dist/rci_tournament_utilities-0.1a22-py3-none-any.whl
3. Start jupyter notebook and start running `organizer_quickstart.ipynb` or `participant_quickstart.ipynb`.
---
## < *For external use.* >
## Setting Up Utility Scripts
The following are instructions for setting up your environment to run the tournament utility scripts.
For a more general overview of the tournament structure, please see the [Tournament Participants' Guide](https://github.com/rocketcapital-ai/tournament-contract/blob/main/scripts/Tournament%20-%20Participants'%20Guide.pdf).
### Recommended - Create a new virtual environment for running these scripts.
If you have [`conda`](https://www.anaconda.com/products/individual) installed, do
>conda create --name <your_env_name> python=3.9 numpy pandas pip

The following will assume you are working in a python >= 3.9 environement with numpy, pandas and pip installed.

### Install and/or upgrade pip.
> pip install --upgrade pip setuptools wheel

### Install the rci-tournament-utilities package
> pip install rci-tournament-utilities --extra-index-url https://test.pypi.org/simple/ --no-cache-dir

### Quickstart.
Download the [`paticipant_quickstart.ipynb`](https://github.com/rocketcapital-ai/tournament-contract/blob/main/scripts/participant_quickstart.ipynb) file.

### Open the notebook.
In the folder where you saved [`paticipant_quickstart.ipynb`](https://github.com/rocketcapital-ai/tournament-contract/blob/main/scripts/participant_quickstart.ipynb), run 
> jupyter notebook

Make sure your notebook is set to run in the environment you created.

### Obtaining a wallet address via Metamask.
Metamask is an Ethereum wallet that functions as a browser add-on.
Download from [here](https://metamask.io/download) and follow the steps to create a new wallet.

### Signing transactions with your private key.
For transactions that modify information on the blockchain, such as sending in a transaction to record your submissions' IPFS location, your private key will be required to sign the transaction.
In the first cell of the notebook, you will be prompted for your private key. 
For metamask, you may obtain this from Metamask > *3-dot menu on top right* > Account Details > Export Private Key.
Please do not paste this key in any file or section of code that can be accessed without authorization.