# COP-001: AT Invoice API Integration

## Document Information

| Field               | Value                                               |
| ------------------- | --------------------------------------------------- |
| **Document Number** | COP-001                                             |
| **Date**            | 2026-01-16                                          |
| **Author**          | João Magalhães <joamag@hive.pt>                     |
| **Subject**         | Complete Invoice API Integration for AT Webservices |
| **Status**          | Implemented                                         |
| **Version**         | 1.1                                                 |

## Description

### Problem

The AT plugin needs comprehensive support for all invoice-related operations provided by the Portuguese Tax Authority (Autoridade Tributária) webservices. While basic invoice submission exists, the full lifecycle management of invoices requires additional operations including querying previously submitted invoices, changing invoice status (e.g., for cancellations), and deleting erroneously submitted invoice communications.

### Solution

This document covers the complete set of invoice-related API operations available through the AT webservices:

| Operation             | Method                    | Purpose                                |
| --------------------- | ------------------------- | -------------------------------------- |
| Register Invoice (V1) | `submit_invoice_v1()`     | Submit invoice using legacy V1 API     |
| Register Invoice (V2) | `submit_invoice_v2()`     | Submit invoice using current V2 API    |
| Query Invoices        | `query_invoices()`        | Retrieve previously submitted invoices |
| Change Invoice Status | `change_invoice_status()` | Update status of submitted invoice     |
| Delete Invoice        | `delete_invoice()`        | Remove erroneously submitted invoice   |

## Endpoint Configuration

### Invoice Submission (V1 - Legacy)

| Environment | URL                                                          |
| ----------- | ------------------------------------------------------------ |
| Production  | `https://servicos.portaldasfinancas.gov.pt:400/fews/faturas` |
| Test        | `https://servicos.portaldasfinancas.gov.pt:700/fews/faturas` |

### Invoice Submission (V2 - Current)

| Environment | URL                                                           |
| ----------- | ------------------------------------------------------------- |
| Production  | `https://servicos.portaldasfinancas.gov.pt:423/fatcorews/ws/` |
| Test        | `https://servicos.portaldasfinancas.gov.pt:723/fatcorews/ws/` |

### Invoice Query

| Environment | URL                                                          |
| ----------- | ------------------------------------------------------------ |
| Production  | `https://servicos.portaldasfinancas.gov.pt:424/fatshare/ws/` |
| Test        | `https://servicos.portaldasfinancas.gov.pt:724/fatshare/ws/` |

**Note**: All endpoints follow the AT port pattern (4xx for production, 7xx for test).

## Operations

### 1. Register Invoice (V1 and V2)

Submits a new invoice to the AT. The V2 API is the current recommended version.

**Request Structure (RegisterInvoiceRequest)**:

- Invoice header information (InvoiceNo, InvoiceDate, InvoiceType, etc.)
- Tax registration numbers for seller and buyer
- Line items with tax details
- Document totals

**Response**: Returns `ATDocCodeID` on success.

### 2. Query Invoices

Retrieves previously submitted invoice information for verification and reconciliation.

**Request Structure (InvoicesRequest)**:

- **TaxRegistrationNumber** (choice): Portuguese VAT number (NIF) of the issuer
- **CustomerTaxID** (choice): VAT identifier of the buyer
- **StartDate**: Period start date (YYYY-MM-DD)
- **EndDate**: Period end date (YYYY-MM-DD)
- **Pagination** (optional): Page number and documents per page (max 5000)

**Response Structure (InvoicesResponse)**:

- **InvoicesList**: Collection of invoice records with pagination metadata
- **estadoExecucao**: Operation status (code and description)

### 3. Change Invoice Status

Updates the status of a previously submitted invoice, typically used for marking invoices as cancelled ("Anulado").

**Request Structure (ChangeInvoiceStatusRequest)**:

- **TaxRegistrationNumber**: NIF of the issuer
- **InvoiceNo**: The invoice number to update
- **InvoiceDate**: Original invoice date
- **InvoiceStatus**: New status code (e.g., "A" for Anulado/Cancelled)
- **InvoiceStatusDate**: Date of the status change

**Response**: Returns operation status code and message.

### 4. Delete Invoice

Removes an erroneously submitted invoice communication from the AT database. This is used when an invoice was communicated with incorrect data.

**Request Structure (DeleteInvoiceRequest)**:

- **TaxRegistrationNumber**: NIF of the issuer
- **InvoiceNo**: The invoice number to delete
- **InvoiceDate**: Original invoice date

**Response**: Returns operation status code and message.

## Implementation Details

### New Methods Added to ATClient

| Method                    | Description                                    |
| ------------------------- | ---------------------------------------------- |
| `query_invoices()`        | Query previously submitted invoices            |
| `change_invoice_status()` | Change status of a submitted invoice           |
| `delete_invoice()`        | Delete an erroneously submitted invoice        |
| `get_at_invoices()`       | Parse invoice query XML response to dictionary |

### Shared Infrastructure

All operations reuse the existing infrastructure:

- `_gen_envelope_v2()` for SOAP envelope generation with AES/RSA encryption
- `_submit_document()` for HTTP communication
- Certificate-based client authentication
- Error checking via `_check_at_errors_v2()`

## Usage Examples

### Query Invoices

```python
# Create and configure the AT client
at_client = api_at.create_client({"test_mode": True})
at_client.generate_at_structure("508605989/1", "password123")

# Build the query payload
query_payload = """
<InvoicesRequest xmlns="http://servicos.portaldasfinancas.gov.pt/faturas">
    <TaxRegistrationNumber>508605989</TaxRegistrationNumber>
    <StartDate>2026-01-01</StartDate>
    <EndDate>2026-01-31</EndDate>
</InvoicesRequest>
"""

# Execute query and parse response
response = at_client.query_invoices(query_payload)
invoices = at_client.get_at_invoices(response)
```

### Change Invoice Status (Cancel)

```python
# Build the status change payload
status_payload = """
<ChangeInvoiceStatusRequest xmlns="http://servicos.portaldasfinancas.gov.pt/faturas">
    <TaxRegistrationNumber>508605989</TaxRegistrationNumber>
    <InvoiceNo>FT 2026/1</InvoiceNo>
    <InvoiceDate>2026-01-15</InvoiceDate>
    <InvoiceStatus>A</InvoiceStatus>
    <InvoiceStatusDate>2026-01-16</InvoiceStatusDate>
</ChangeInvoiceStatusRequest>
"""

# Execute status change
response = at_client.change_invoice_status(status_payload)
```

### Delete Invoice

```python
# Build the delete payload
delete_payload = """
<DeleteInvoiceRequest xmlns="http://servicos.portaldasfinancas.gov.pt/faturas">
    <TaxRegistrationNumber>508605989</TaxRegistrationNumber>
    <InvoiceNo>FT 2026/1</InvoiceNo>
    <InvoiceDate>2026-01-15</InvoiceDate>
</DeleteInvoiceRequest>
"""

# Execute deletion
response = at_client.delete_invoice(delete_payload)
```

## Response Codes

The V2 API uses `codResultOper` for result codes:

- **2xxxx**: Success
- **3xxxx**: Validation errors
- **4xxxx**: Authentication/authorization errors
- **5xxxx**: System errors

## References

- WSDL Specifications:
  - `Fatcorews.wsdl` - Registration, modification, and deletion operations
  - `fatshareInvoices.wsdl` - Query operations
- Documentation: [e-Fatura Webservice](https://info.portaldasfinancas.gov.pt/pt/apoio_ao_contribuinte/Outras_entidades/Suporte_tecnologico/Webservice/e_Fatura/Paginas/default.aspx)
- Integration Manual: [Comunicacao dos elementos dos documentos de faturacao](https://info.portaldasfinancas.gov.pt/pt/apoio_ao_contribuinte/Outras_entidades/Suporte_tecnologico/Webservice/e_Fatura/Documents/Comunicacao_dos_elementos_dos_documentos_de_faturacao.pdf)

---

**Document Classification**: Internal Technical Documentation
