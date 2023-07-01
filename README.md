# CSE406 - Computer Security

## Offline 1 (AES Encryption-Decryption with Diffie-Hellman Key Exchange)
Navigate to [solutions](Offline_1/solutions) folder and run the following commands:

```bash
pip install -r requirements.txt
```

### Part 1 - Independent Implementation of AES
run [testAES.py](Offline_1/solutions/testAES.py) to see the results.

### Part 2 - Independent Implementation of Diffie-Hellman Key Exchange
run [testDH.py](Offline_1/solutions/testDH.py) to see the results.

### Part 3 - Implementation of AES cryptosystem with TCP socket programming
run [server.py](Offline_1/solutions/server.py) and [client.py](Offline_1/solutions/client.py) to see the results.

### Bonus Tasks
- **RSA Key Exchange**: RSA is used to exchange the AES key between the client and the server. The keys are generated on client side. The client and passes the public key to the server. The server then uses the public key to encrypt p, g, A and send those to the client. Run [testRSA.py](Offline_1/solutions/testRSA.py) to see the results.
