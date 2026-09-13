# AT Related Resources

## Passwords

The TesteWebServices.pfx file is protected by the password `TESTEwebservice`.

The test webservice account of the AT, used automatically in test mode (see below), is the NIF `599999993` with the sub-user `0037` and the password `Testes1234!`. The AT rotates this password together with the test certificate and announces the new value by email to the registered software producers, the most recent change having replaced the previous `testes1234` on 2026-07-27. Both values are defined in `system.py` and have to be updated together with the certificate, as a deployment that carries one without the other fails to authenticate.

## Test Mode

The client targets the test webservices of the AT whenever the test mode flag is set, either through the `test_mode` API attribute passed to `create_client()` or through the `AT_TEST_MODE` configuration variable, the configuration variable taking precedence over the attribute.

Test mode is not only a change of endpoint, it replaces every credential of the submission with fixed values, so that nothing of the registered configuration is used:

| Element     | Production              | Test                                         |
| ----------- | ----------------------- | -------------------------------------------- |
| Username    | `at_structure.username` | `599999993/0037` (hardcoded)                 |
| Password    | `at_structure.password` | `Testes1234!` (hardcoded)                    |
| Certificate | `AT_CERTIFICATE`        | `api_at/resources/certificate.crt` (bundled) |
| Private key | `AT_KEY`                | `api_at/resources/key.pem` (bundled)         |

As a consequence a test environment cannot be pointed at another certificate or at another account through configuration, the values are the ones shipped with the plugin and changing them requires deploying a new version of it.

The endpoints share the host `servicos.portaldasfinancas.gov.pt` and the test ports are the production ones offset by 300:

| Service             | Production                         | Test                               |
| ------------------- | ---------------------------------- | ---------------------------------- |
| Invoices (v1)       | `:400/fews`                        | `:700/fews`                        |
| Invoices (v2)       | `:423/fatcorews/ws/`               | `:723/fatcorews/ws/`               |
| Invoice query       | `:425/fatshare/ws/fatshareFaturas` | `:725/fatshare/ws/fatshareFaturas` |
| Transport documents | `:401/sgdtws`                      | `:701/sgdtws`                      |
| Series (ATCUD)      | `:422/SeriesWSService`             | `:722/SeriesWSService`             |

### Troubleshooting Authentication

An expired certificate fails during the TLS handshake, before the AT produces any response, so it completely masks a password that is also out of date. When a test environment starts failing to authenticate, check both halves at once instead of one at a time:

```bash
openssl x509 -in certificate.crt -noout -enddate
grep -n "Testes1234" ../system.py
```

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
