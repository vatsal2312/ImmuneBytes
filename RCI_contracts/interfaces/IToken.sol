pragma solidity 0.8.4;

// SPDX-License-Identifier: MIT

/**
 * @dev Interface for interacting with Token.sol.
 */
interface IToken {

    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    function increaseAllowance(address spender, uint256 addedValue) external returns (bool);

    function decreaseAllowance(address spender, uint256 subtractedValue) external returns (bool);

    function grantPermission(address spender) external returns (bool success);

    function getPermission(address spender) external view returns (bool permitted);

    function revokePermission(address spender) external returns (bool success);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event PermissionGranted(address indexed owner, address indexed spender);
    event PermissionRevoked(address indexed owner, address indexed spender);


}