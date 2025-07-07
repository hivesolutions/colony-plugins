# AT Related Resources

## Passwords

The TesteWebServices.pfx file is protected by the password `TESTEwebservice`.

## Actions

### Extract Test Certificate

In order to "extract" the private key (key.pem) from the pfx-based certificate file use:

```bash
openssl pkcs12 -in TesteWebServices.pfx -nocerts -nodes | openssl rsa > key.pem
```

To extract the base certificate file (certificate.crt) to be used in openssl from the pfx file use:

```bash
openssl pkcs12 -in TesteWebServices.pfx -out certificate.crt -nokeys -clcerts
```
