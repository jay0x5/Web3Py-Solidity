// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract SimpleContract {
    // uint var_int1;
    string name = "hughie";
    // constructor(){ 
    //     var_int1 = 100;
    // }

    // function getInt() public view returns(uint){
    //     return var_int1;
    // }

    // function updateInt() public{
    //     var_int1 = var_int1 + 1;
        

    // }
    function WriteName(string memory _name) public{
        name = _name;

    }

    function GetName() public view returns(string memory){
        return name;
    }
}