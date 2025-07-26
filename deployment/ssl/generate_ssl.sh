"""
#!/bin/bash
# SSL Certificate Generation for Development/Staging

set -e

SSL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SSL_DIR"

echo "Generating SSL certificates for local development..."

# Create private key
openssl genrsa -out server.key 2048

# Create certificate signing request
openssl req -new -key server.key -out server.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Create self-signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# Create certificate chain (self-signed)
cp server.crt server-chain.crt

# Set appropriate permissions
chmod 600 server.key
chmod 644 server.crt server.csr server-chain.crt

echo "SSL certificates generated:"
echo "  Private key: server.key"
echo "  Certificate: server.crt"
echo "  Chain: server-chain.crt"
echo ""
echo "Note: These are self-signed certificates for development only."
echo "For production, use certificates from a trusted CA."

# Clean up CSR
rm server.csr
"""
