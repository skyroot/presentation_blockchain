#!/usr/bin/env python

import os,sys
import json
import time

target = 'http://127.0.0.1:8545'

casino_bytecode = '60806040526103e86000556103e860015534801561001c57600080fd5b5060028054600160a060020a031916331790556103788061003e6000396000f30060806040526004361061006c5763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416635c886b34811461007157806370a082311461007e5780637365870b146100be57806373c18c7c146100c9578063e1c7392a146100d1575b600080fd5b61007c6004356100d9565b005b34801561008a57600080fd5b506100ac73ffffffffffffffffffffffffffffffffffffffff60043516610113565b60408051918252519081900360200190f35b61007c600435610125565b61007c61024c565b61007c61028b565b336000908152600360205260409020546064106100f557600080fd5b60015433600090815260036020526040902080549190920290039055565b60036020526000908152604090205481565b6000670de0b6b3a7640000341161013b57600080fd5b336000908152600360205260408120541161015557600080fd5b6000544281151561016257fe5b0490506101a46040805190810160405280600981526020017f74696d657374616d700000000000000000000000000000000000000000000000815250426102a0565b508181146101f95733600081815260036020526040808220829055516706f05b59d3b1ffff19340180156108fc0292909190818181858888f193505050501580156101f3573d6000803e3d6000fd5b50610248565b6040513390670de0b6b3a763ffff19340180156108fc02916000818181858888f19350505050158015610230573d6000803e3d6000fd5b50336000908152600360205260409020805460640190555b5050565b60025473ffffffffffffffffffffffffffffffffffffffff16331461027057600080fd5b60025473ffffffffffffffffffffffffffffffffffffffff16ff5b33600090815260036020526040902060649055565b60007f941296a39ea107bde685522318a4b6c2b544904a5dd82a512748ca2cf839bef783836040518080602001838152602001828103825284818151815260200191508051906020019080838360005b838110156103085781810151838201526020016102f0565b50505050905090810190601f1680156103355780820380516001836020036101000a031916815260200191505b50935050505060405180910390a1506001929150505600a165627a7a723058209ca8f8522f86520ca3844e09495084089874533e9f9d0333b034bd99232336260029'


# get the accounts
cmd_1 = 'curl -H "Content-type: application/json" -X POST --data \'{"jsonrpc":"2.0","method":"eth_accounts","params":[],"id":1}\'  %s 2>/dev/null'%(target)
res = os.popen(cmd_1).read()
accounts = json.loads(res)['result']
my_eth_addr = accounts[1]
print '[*] your_eht_address: ' + my_eth_addr

# deploy casino contract via json-rpc
cmd_2 = 'curl -H "Content-type: application/json" -X POST --data \'{"jsonrpc":"2.0","method":"eth_sendTransaction","params":[{"data":"0x%s","gas":"0x100000","from":"%s"}],"id":1}\'  %s 2>/dev/null'%(casino_bytecode,my_eth_addr,target)
res = os.popen(cmd_2).read()
receipt = json.loads(res)['result']
print '[*] receipt_id: ' + receipt

# waiting for the transaction to be received the miner
print '[*] waiting for mining...'
time.sleep(10)

# get the contract address
cmd_3 = 'curl -H "Content-type: application/json" -X POST --data \'{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["%s"],"id":1}\'  %s 2>/dev/null' %(receipt,target)
res = os.popen(cmd_3).read()
contract_addr = json.loads(res)['result']['contractAddress']
print '[*] contract_address: ' + contract_addr


