# Generate new certificate & private key

From time to time it's important to generate private key and certificate pairs.
To do so use the following command:

```bash
openssl req -x509 -nodes -days 36500 -newkey rsa:2048 -keyout dummy.key -out dummy.crt
```
