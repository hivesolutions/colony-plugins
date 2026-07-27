# AT Related Resources

## Passwords

The TesteWebServices.pfx file is protected by the password `TESTEwebservice`.

## Actions

### Download Test Certificate

The most recent test certificate bundle is published by the AT at [TesteWebservices.zip](https://info.portaldasfinancas.gov.pt/pt/apoio_ao_contribuinte/Outras_entidades/Suporte_tecnologico/Certificados_de_seguranca/Documents/TesteWebservices.zip), the bundle contains a single `TesteWebservices.pfx` file and is replaced by the AT every six months, meaning that the extraction below has to be re-run whenever the certificate expires.

```bash
curl -L -o TesteWebservices.zip https://info.portaldasfinancas.gov.pt/pt/apoio_ao_contribuinte/Outras_entidades/Suporte_tecnologico/Certificados_de_seguranca/Documents/TesteWebservices.zip
unzip TesteWebservices.zip
```

### Extract Test Certificate

In order to "extract" the private key (key.pem) from the pfx-based certificate file use:

```bash
openssl pkcs12 -in TesteWebservices.pfx -nocerts -nodes | openssl rsa > key.pem
```

To extract the base certificate file (certificate.crt) to be used in openssl from the pfx file use:

```bash
openssl pkcs12 -in TesteWebservices.pfx -out certificate.crt -nokeys -clcerts
```

Note that the `-out` based extraction prepends the PKCS#12 bag attributes (`Bag Attributes`, `subject=`, `issuer=`) to the resulting file and that both commands emit CRLF line endings on Windows. Since the committed files are expected to be "pure" PEM with LF line endings, the extracted files should be normalized using:

```bash
openssl x509 -in certificate.crt | tr -d '\r' > certificate.pem && mv certificate.pem certificate.crt
openssl rsa -in key.pem | tr -d '\r' > key.tmp.pem && mv key.tmp.pem key.pem
```

To confirm that the resulting certificate and private key belong to each other (the modulus digests must match) and to check the validity period use:

```bash
openssl x509 -in certificate.crt -noout -modulus | openssl md5
openssl rsa -in key.pem -noout -modulus | openssl md5
openssl x509 -in certificate.crt -noout -subject -dates
```
