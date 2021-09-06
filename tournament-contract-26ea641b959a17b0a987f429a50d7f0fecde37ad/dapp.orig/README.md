### Dapp Usage Instructions
1. Run `server.py`. 
2. Open a Firefox, Chrome or Edge browser.
3. Navigate to http://localhost:8087/, or whichever port is specified in `server.py`.

### Connecting to Polygon on Metamask.
The Polygon Testnet is called Mumbai. The native token on both Polygon and Mumbai is called MATIC.

The following are steps to connect to Mumbai.
- Open the Metamask Widget.
- Click on the network button at the top. (It should say something like "Ropsten Test Network" or "Ethereum Mainnet").
- Click on "Custom RPC" at the bottom of the network list.
- Fill in the following:
    - Network Name: Mumbai
    - New RPC URL: https://rpc-mumbai.matic.today
    - Chain ID: 80001
    - Currency Symbol: MATIC
    - Block Explorer URL: https://mumbai.polygonscan.com
    
Set your network to the Mumbai network. Now, your transactions will be on the Mumbai layer-2 network. The Dapp, which connects via Metamask, will be connected to whichever network your Metamask is set to.
Remember to add the ERC20 tokens you are working with.

### Gas Pricing
1 Gwei is enough for transactions on Mumbai! 

Metamask sets the gas price to 30 Gwei by default so you will need to manually key this in each time. The gas price field will show up when Metamask pops up during the initiation of a transaction. 

### MATIC Faucet
Found here: https://faucet.matic.network/. Select the following when requesting from the faucet:

Token: *MATIC Token* 

Network: *Mumbai*

### Alternative RPC URLs
If for some reason there is a problem with the Metamask connection to Mumbai, you may try to use the following as alternatives under the 'New RPC URL' field.
- https://rpc-mumbai.maticvigil.com
- https://matic-mumbai.chainstacklabs.com
- https://matic-testnet-archive-rpc.bwarelabs.com
