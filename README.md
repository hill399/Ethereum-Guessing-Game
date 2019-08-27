# Ethereum-Guessing-Game
Guessing game written in Solidity/Python3.6

Project created as a learning excercise in Ethereum development. Game has on-chain component written in Solidity and off-chain logic written in Python3.6.

Local Ethereum account and Infura access is required to be set within Python script. In order to keep game periodically running, Python script should be configured to run at
regular intervals (cronjob).

## Game Structure
Aim is to correctly guess 4-digit code generated off-chain and held in the python script. Submitted guesses is done on-chain which are then periodically retrieved, validated
and returned to the contract. Guesses are taken until correct answer is received and the winner is paid out of guess fees (prize pool).

Whitelisted address is set within the contract, which is the only address capable of validating guesses.

#### New Game State
	- When new game starts, 4-digit code is generated using python secrets.SystemRandom(). 
	- Random 8-digit code is created, concatenated with the 4-digit answer and hash generated for on-chain reference.
	- Answers are stored off-chain for validation stage.
	
#### Guess State
	- 4 Values between 0-9 are taken as data along with guess fee configurable by the whitelisted address.
	- Guess and sender is stored for guess validation.
	
#### Validate State
	- Guesses are retrieved by whitelisted address (Python script) and parsed for guess data. 
	- Guesses are compared against previously generated 4-digit code. 
	- A status code is returned based upon a 4-bit binary value to denote which numbers are incorrect.
	- If the guess is correct, the 8-bit hash code is sent to allow users to prove on-chain hash.
	
#### Result State
	- If guess is correct (status code == 0), round details are archived and prize pool is sent to winner.
	- If guess is incorrect (status code != 0), game state is reset to Guess State.


## Project State
On-chain and off-chain components are functional. Truffle unit tests to be finalised.