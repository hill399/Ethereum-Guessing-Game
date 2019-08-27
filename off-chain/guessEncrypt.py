# IMPORTS
from web3 import Web3
import secrets
import sys

try:
    # Open current round details
	f = open("roundDetails.txt", "r")
	rawDigits = f.readline()
	roundKey = f.readline()
	concatCode = f.readline()
	concatEncrypt = f.readline()
	f.close()
except IOError:
    print('Previous round details are not accessible')
	
	
# Setup Infura parameters
infura_provider = Web3.HTTPProvider('INFURA_DETAILS_HERE')
w3 = Web3(infura_provider)

# Setup contract/Whitelist parameters
contract_address = "DEPLOYED_CONTRACT_HERE"
resolver_address = 'LOCAL_ETH_ADDRESS_HERE'
resolver_pk = 'LOCAL_ETH_ACCOUNT_PK_HERE'

# Contract ABI and setup
my_abi = [
	{
		"constant": 'false',
		"inputs": [
			{
				"name": "_A",
				"type": "uint256"
			},
			{
				"name": "_B",
				"type": "uint256"
			},
			{
				"name": "_C",
				"type": "uint256"
			},
			{
				"name": "_D",
				"type": "uint256"
			}
		],
		"name": "guess",
		"outputs": [],
		"payable": 'true',
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [],
		"name": "currentState",
		"outputs": [
			{
				"name": "guessNo",
				"type": "uint256"
			},
			{
				"name": "prizePool",
				"type": "uint256"
			},
			{
				"name": "roundWinner",
				"type": "address"
			},
			{
				"name": "winningHash",
				"type": "bytes32"
			},
			{
				"name": "roundDecodeKey",
				"type": "uint256"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'false',
		"inputs": [
			{
				"name": "_winningHash",
				"type": "bytes32"
			}
		],
		"name": "newGame",
		"outputs": [],
		"payable": 'false',
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [
			{
				"name": "_roundNumber",
				"type": "uint256"
			}
		],
		"name": "checkRoundHistoryDecoder",
		"outputs": [
			{
				"name": "",
				"type": "bytes32"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256[4]"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [],
		"name": "checkRoundState",
		"outputs": [
			{
				"name": "",
				"type": "uint8"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [],
		"name": "roundNo",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'false',
		"inputs": [
			{
				"name": "_rawData",
				"type": "uint256"
			},
			{
				"name": "_statusCode",
				"type": "uint256"
			}
		],
		"name": "returnResult",
		"outputs": [],
		"payable": 'false',
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [],
		"name": "guessCost",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [],
		"name": "retrieveGuess",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "bytes32"
			},
			{
				"name": "",
				"type": "uint256[4]"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'false',
		"inputs": [
			{
				"name": "_whitelistAddress",
				"type": "address"
			}
		],
		"name": "setWhitelistResolver",
		"outputs": [],
		"payable": 'false',
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [],
		"name": "roundState",
		"outputs": [
			{
				"name": "",
				"type": "uint8"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [],
		"name": "whitelistAddress",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": 'true',
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "lastGuess",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": 'false',
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": 'false',
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": 'false',
		"inputs": [
			{
				"indexed": 'true',
				"name": "_roundNumber",
				"type": "uint256"
			},
			{
				"indexed": 'false',
				"name": "_timestamp",
				"type": "uint256"
			}
		],
		"name": "newGameStarted",
		"type": "event"
	},
	{
		"anonymous": 'false',
		"inputs": [
			{
				"indexed": 'true',
				"name": "_roundNumber",
				"type": "uint256"
			},
			{
				"indexed": 'true',
				"name": "_guessNumber",
				"type": "uint256"
			},
			{
				"indexed": 'false',
				"name": "_guesser",
				"type": "address"
			},
			{
				"indexed": 'false',
				"name": "guess",
				"type": "uint256[4]"
			},
			{
				"indexed": 'false',
				"name": "_timestamp",
				"type": "uint256"
			}
		],
		"name": "guessMade",
		"type": "event"
	},
	{
		"anonymous": 'false',
		"inputs": [
			{
				"indexed": 'true',
				"name": "_roundNumber",
				"type": "uint256"
			},
			{
				"indexed": 'true',
				"name": "_guessNumber",
				"type": "uint256"
			},
			{
				"indexed": 'false',
				"name": "_statusCode",
				"type": "uint256"
			},
			{
				"indexed": 'false',
				"name": "_timestamp",
				"type": "uint256"
			}
		],
		"name": "guessValidated",
		"type": "event"
	},
	{
		"anonymous": 'false',
		"inputs": [
			{
				"indexed": 'true',
				"name": "_roundNumber",
				"type": "uint256"
			},
			{
				"indexed": 'true',
				"name": "_guessNumber",
				"type": "uint256"
			},
			{
				"indexed": 'false',
				"name": "_winner",
				"type": "address"
			},
			{
				"indexed": 'false',
				"name": "_winnings",
				"type": "uint256"
			},
			{
				"indexed": 'false',
				"name": "_timestamp",
				"type": "uint256"
			}
		],
		"name": "gameOver",
		"type": "event"
	}
]

guessEncryptContract = w3.eth.contract(address=contract_address, abi=my_abi)
nonce = w3.eth.getTransactionCount(resolver_address)

# Call current state to determine off-chain actions
currentState = guessEncryptContract.functions.checkRoundState().call()

# NOT_STARTED
if currentState == 0:
	# Generate new code numbers, roundKey encryptor
	secretsGenerator = secrets.SystemRandom()
	number_list = [0,1,2,3,4,5,6,7,8,9]

	secure_sample = secretsGenerator.sample(number_list, 4)
	print(secure_sample)
	
	roundKey = secretsGenerator.randint(10000000, 99999999)

	# Concatenate numbers into single string and hash encode
	answer_concat = int(str(roundKey) + str(secure_sample[0]) + str(secure_sample[1]) + str(secure_sample[2]) + str(secure_sample[3]))
	print(answer_concat)
	
	correct_answer_encrypt = Web3.toBytes(Web3.sha3(answer_concat))
	
	# Call new Tx to setup game
	newGameTX = guessEncryptContract.functions.newGame(correct_answer_encrypt,).buildTransaction({'chainId': 3,'gas': 140000,'gasPrice': w3.toWei('10', 'gwei'),'nonce': nonce,})

	signed_txn = w3.eth.account.signTransaction(newGameTX, private_key=resolver_pk)
	w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	# Write new round details to file	
	f = open("roundDetails.txt", "w+")
	f.write(str(secure_sample) + "\n")
	f.write(str(roundKey) + "\n")
	f.write(str(answer_concat) + "\n")
	f.write(str(correct_answer_encrypt) + "\n")
	f.close()

	print('New game started')

# AWAITING_GUESS
elif currentState == 1:
	# Nothing is done off-chain in this state
	print('Currently awaiting guess at address ' + str(resolver_pk))
	
	
# AWAITING_VALIDATION
elif currentState == 2:
	# Pull results off-chain and compare against correct values
	print('currently awaiting validation')
	
	statusCode = 0

	roundNo, guessNo, guessHash, guessRaw = guessEncryptContract.functions.retrieveGuess().call()

	print('results pulled')
	print('roundNo = ' + str(roundNo))
	print('guessNo = ' + str(guessNo))
	print('guessHash = ' + Web3.toHex(guessHash))
	print('guessRaw = ' + str(guessRaw))
	
	guessRawStr = str(guessRaw)
	numberLocation = [1,4,7,10]
	
	for x in numberLocation:
		if guessRawStr[x] != rawDigits[x]:
			if x == 1:
				statusCode = statusCode + 8
			elif x == 4:
				statusCode = statusCode + 4
			elif x == 7:
				statusCode = statusCode + 2
			elif x == 10:
				statusCode = statusCode + 1
			else:
				print('In catch-all')
		else:
			print('index[' + str(x) + '] correct')
		
	inputHash = guessHash
	
	if statusCode == 0:
		decoderHash = int(roundKey) 
	else:
		decoderHash = 0 
	
	
	print('statusCode = ' + str(statusCode))
	print('inputHash = ' + str(inputHash))
	print('decoderHash = ' + str(decoderHash))
	
	checkResultTX = guessEncryptContract.functions.returnResult(decoderHash,statusCode,).buildTransaction({'chainId': 3,'gas': 300000,'gasPrice': w3.toWei('10', 'gwei'),'nonce': nonce,})

	signed_txn = w3.eth.account.signTransaction(checkResultTX, private_key=resolver_pk)
	hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction) 
	
	print(hash)
	print('result submitted')
	

# DEFAULT
else:
	print('Error in processing')
