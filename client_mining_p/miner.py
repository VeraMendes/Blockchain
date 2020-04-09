import hashlib
import requests
from datetime import datetime

import sys
import json


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://0.0.0.0:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()


    # mined coins variable
    coins_mined = 0

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        print('the adventure begins...')
        start_time = datetime.now()
        block = data['last_block']
        new_proof = proof_of_work(block)
        end_time = datetime.now()
        print(f"You have mined {coins_mined} coins")
        print(f"It took you {end_time - start_time} to finish this mining cycle!")
        print('work finished!!!')

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()


        # If the server responds with a 'message' 'New Block Forged'
        if data['message'] == 'New Block Forged':
            # add 1 to the number of coins mined and print it. 
            coins_mined += 1
            print(f'Coins mined: {coins_mined}')  
            # Otherwise, print the message from the server.
        else:
            print(data['message'])    

# example for new transaction via curl: 
# curl -X POST -H "Content-Type: application/json" -d '{"sender":"vera-mendes", "recipient": "Brian", "amount": 1}' localhost:5000/transactions/new
# same available via postman or insomnia