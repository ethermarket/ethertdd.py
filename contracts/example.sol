contract example{
    address public owner;
    uint public fee;
    mapping (string32 => address) public names;

    function example() {
        owner = msg.sender;
        fee = 10000; // in wei
    }

    function setName(string32 name, address newAddress) returns (uint8 r) {
        if (isOwner()==0 || msg.value < fee || (names[name] != 0x0 && names[name] != msg.sender)) {
            return 0;
        }
        names[name] = newAddress;

        if (msg.value > fee) {
            newAddress.send(msg.value - fee);
        }
        return 1;
    }

    function forceTrue() returns (uint r) {
        return 7;
    }

    function setOwner(address newOwner) returns (uint8 r) {
        if (isOwner()==0) return 0;
        owner = newOwner;
        return 1;
    }

    function setFee(uint32 newFee) returns (uint8 r) {
        if (isOwner()==0) return 0;
        fee = newFee;
        return 1;
    }

    function isOwner() returns (uint8 r) {
        if (msg.sender == owner) return 1;
        return 0;
    }

    function withdraw(uint32 amount) returns (uint8 r) {
        if (isOwner()==0) return 0;

        owner.send(amount);
        return 1;
    }
}
