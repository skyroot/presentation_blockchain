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
