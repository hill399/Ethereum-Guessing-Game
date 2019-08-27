const GuessingGame = artifacts.require('GuessingGame');
const truffleAssert = require('truffle-assertions');

/* UNIT TESTS TO CODE 
    1)   Should configure the whitelist resolver
    2)   Should start a new game
    3)   Should take a valid guess
    4)   Can't start a game if it's currently running
    5)   Start response is correct
    6)   Guess response is correct
    7)   Correct guess fee applies
    8)   Only whitelist can retrieve guesses
    9)   Can only retrieve in validation state
    10)  Guess returned in valid format
    11)  Validation response is correct
    12)  Contract resets for incorrect guess
    13)  Correct data is stored when game-over
    14)  Round counter correctly increments 
*/

contract("GuessingGame", (accounts) => {

    it('Should configure the whitelist resolver', async() => {
        const guessingGameInstance = await GuessingGame.deployed();

        await truffleAssert.reverts(
            guessingGameInstance.setWhitelistResolver(accounts[1], {from: accounts[1] }),
            "Address calling is not whitelisted"
        );

        const goodWhitelist = await guessingGameInstance.setWhitelistResolver.call(accounts[1], {from: accounts[0] });
        assert.equal(goodWhitelist, whiteListResolverAddress, "New whitelist was not set");
    });

    it('Should start a new game', async() => {
        const guessingGameInstance = await GuessingGame.deployed();
        const testWinningHash = web3.utils.sha3('9999991234');

        await truffleAssert.reverts(
            guessingGameInstance.newGame(testWinningHash, {from : accounts[1] }),
            "Address calling is not whitelisted"
        );

        const result = await guessingGameInstance.newGame(testWinningHash, {from : accounts[0] });
        await truffleAssert.eventEmitted(result, 'newGameStarted');
    });
/*
    it('Should take a valid guess'), async() => {
        const guessingGameInstance = await GuessingGame.deployed();
        const testWinningHash = web3.utils.sha3('9999991234');

        await guessingGameInstance.newGame(testWinningHash, {from : accounts[0] });

        await guessingGameInstance.guess(1,2,3,4, {from : accounts[0] });

    }
*/

});
