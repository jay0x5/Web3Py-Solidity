// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract Escrow{

    mapping(address => uint) public DepositMap;
    mapping(address => uint) WithdrawedMap;

    address owner;
    address payable public payee;
    uint public depamount;
    uint public existingamount;
    uint public newAmt;
    uint public amtwithdraw;
    uint public newbalance;

    function SetPayee(address payable _payee) public {
        payee = _payee;
    }
    
    modifier IsOwner() {
        require(owner == msg.sender, "Not Owner!");
        _;
    }

    modifier IsPayee() {
        require(payee == address(payee), "Please enter a valid address");
        _;
    }

    

    constructor(){
        owner = msg.sender;
    }

    function deposit() payable public IsOwner{

        depamount = msg.value; //get the amount to be deposited
        existingamount = DepositMap[owner]; //just extending the existing mapped deposited amount to a variable
        newAmt = existingamount + depamount; //add existing and to be deposited amount
        DepositMap[owner] =  newAmt;
        // updateDep();
        
        
    }

    function withdraw(uint _amt) payable public IsPayee{    

        amtwithdraw = _amt * 1000000000000000000; // ether to wei conversion
        existingamount = DepositMap[owner]; // fetch the existing balance
        require(amtwithdraw <= existingamount,"Lack of funds!"); //check if owner has enough to pay for requested withdrawal 
         
        newbalance = existingamount - amtwithdraw; //subtract existing from amount to be withdrawn
        DepositMap[owner] = newbalance; //update the new balance for owner
        payee.transfer(amtwithdraw); //send the amount




        
    }

    
}
//not the best code but pretty good for a Day2 Solidity Guy