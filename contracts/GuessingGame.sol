pragma solidity ^0.5.0;
import "./SafeMath.sol";

contract GuessingGame {

    using SafeMath for uint;

    event newGameStarted(uint indexed _roundNumber, uint _timestamp);
    event guessMade(uint indexed _roundNumber, uint indexed _guessNumber, address _guesser, uint[4] guess, uint _timestamp);
    event guessValidated(uint indexed _roundNumber, uint indexed _guessNumber, uint _statusCode, uint _timestamp);
    event gameOver(uint indexed _roundNumber, uint indexed _guessNumber, address _winner, uint _winnings, uint _timestamp);

    uint public roundNo = 0;
    uint public guessCost = 1 wei;

    enum RoundState {NOT_STARTED, AWAITING_GUESS, AWAITING_VALIDATION}

    RoundState public roundState;

    struct gameState {
        uint guessNo;
        uint256 prizePool;
        address payable roundWinner;
        bytes32 winningHash;
        uint256 roundDecodeKey;
        uint[4] correctAnswer;
    }

    gameState public currentState;
    mapping (uint => gameState) archiveGames;

    uint[4] public lastGuess;
    address payable lastGuessOwner;
    bytes32 guessHash;

    address public whitelistAddress;

    /* Modifier to ensure only whitelisted resolver address can validate guesses */
    modifier onlyWhitelistResolver() {
        require(msg.sender == whitelistAddress, "Address calling is not whitelisted");
        _;
    }

    /* Modifier to ensure that input guess is within 0-9 range */
    modifier validDataInput (uint _A, uint _B, uint _C, uint _D) {
        require( 0 <= _A && _A <= 9 &&
                 0 <= _B && _B <= 9 &&
                 0 <= _C && _C <= 9 &&
                 0 <= _D && _D <= 9, "Invalid guess range");
        _;
    }

    /* PUBLIC FUNCTION - player calls to attempt guess ( 4 x num ) */
    function guess (uint _A, uint _B, uint _C, uint _D) public payable validDataInput (_A, _B, _C, _D) {
        require(roundState == RoundState.AWAITING_GUESS, "The game is not currently awaiting a guess");
        require(msg.value == guessCost, "Incorrect guess fee paid");

        guessHash = keccak256(abi.encodePacked(_A, _B, _C, _D));
        lastGuessOwner = msg.sender;

        lastGuess[0] = _A;
        lastGuess[1] = _B;
        lastGuess[2] = _C;
        lastGuess[3] = _D;

        roundState = RoundState.AWAITING_VALIDATION;
        currentState.prizePool = currentState.prizePool.add(msg.value);
        currentState.guessNo = currentState.guessNo.add(1);
        emit guessMade(roundNo, currentState.guessNo, msg.sender, lastGuess, block.timestamp);
    }

    /* PUBLIC FUNCTION - whitelisted account can retrieve current player guess */
    function retrieveGuess() public view onlyWhitelistResolver returns (uint, uint, bytes32,  uint[4] memory){
        require(roundState == RoundState.AWAITING_VALIDATION, "Game currently does not guess to check");

        return (roundNo, currentState.guessNo, guessHash, lastGuess);
    }

    /* PUBLIC FUNCTION - function for whitelisted account to return guess response */
    function returnResult(uint _rawData, uint _statusCode) public onlyWhitelistResolver {
        require(roundState == RoundState.AWAITING_VALIDATION, "Game currently does not need guess validation");
        emit guessValidated(roundNo, currentState.guessNo, _statusCode, block.timestamp);

        if(_statusCode == 0) {
            emit gameOver(roundNo, currentState.guessNo, lastGuessOwner, currentState.prizePool, block.timestamp);

            currentState.roundWinner = lastGuessOwner;
            currentState.roundDecodeKey = _rawData;
            currentState.correctAnswer = lastGuess;
            currentState.roundWinner.transfer(currentState.prizePool);

            archiveGames[roundNo] = currentState;
            delete currentState;
            roundState = RoundState.NOT_STARTED;
        } else {
            roundState = RoundState.AWAITING_GUESS;
        }
    }

    /* PUBLIC FUNCTION - function to start a new game */
    function newGame(bytes32 _winningHash) public onlyWhitelistResolver {
        require(roundState == RoundState.NOT_STARTED, "Game is currently running");
        roundNo = roundNo.add(1);
        delete lastGuess;
        delete guessHash;
        delete lastGuessOwner;

        currentState.winningHash = _winningHash;
        roundState = RoundState.AWAITING_GUESS;
        emit newGameStarted(roundNo, block.timestamp);
    }

    /* PUBLIC FUNCTION - function to change whitelisted address */
    function setWhitelistResolver(address _whitelistAddress) public onlyWhitelistResolver {
        whitelistAddress = _whitelistAddress;
    }

    function checkRoundState() public view returns (RoundState) {
        return roundState;
    }

    /* PUBLIC VIEW FUNCTION - return previous round hash/key combo */
    function checkRoundHistoryDecoder(uint _roundNumber) public view returns (bytes32, uint256, uint[4] memory){
        return (archiveGames[_roundNumber].winningHash, archiveGames[_roundNumber].roundDecodeKey, archiveGames[_roundNumber].correctAnswer);
    }

    /* Constructor to set initial state variables */
    constructor () public {
        roundNo = 0;
        guessCost = 1 wei;
        lastGuess = [0,0,0,0];

        currentState.guessNo = 0;
        currentState.prizePool = 0 wei;

        roundState = RoundState.NOT_STARTED;

        whitelistAddress = msg.sender;
    }
}
