# AI Secure Intelligence Vault - Secure File Sharing API Documentation

## Overview

This document describes the industry-grade Secure File Sharing API endpoints with JWT authentication, dual-email OTP verification, and file metadata preservation.

## Architecture

```
┌─────────────────────┐
│     Frontend        │
│  React + Tailwind   │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────────────┐
│    FastAPI Backend Server            │
│  - JWT Authentication                │
│  - OTP Verification                  │
│  - File Encryption (AES-256-GCM)    │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│    SQLAlchemy Database               │
│  - FileShare Table                   │
│  - OTPSession Table                  │
│  - User Table                        │
│  - VaultDocument Table               │
└──────────────────────────────────────┘
```

## Security Features

- **AES-256-GCM Encryption**: Industry-standard file encryption
- **JWT Authentication**: Secure API access control
- **Dual-Email OTP**: Both sender and recipient verify via email
- **File Metadata Preservation**: Exact file reconstruction after decryption
- **File Integrity Verification**: SHA-256 checksum validation
- **Secure Key Derivation**: PBKDF2 key derivation from password
- **Expiration**: File shares expire after 48 hours by default
- **Access Logging**: Audit trail of all access attempts

## API Endpoints

### 1. ENCRYPTION PHASE

#### Step 1: Initialize Encryption
```
POST /api/secure-share/encrypt/init
Content-Type: application/json

Request Body:
{
  "sender_email": "sender@example.com",
  "recipient_email": "recipient@example.com",
  "file_description": "Optional description"
}

Response:
{
  "success": true,
  "message": "OTP codes sent to both emails",
  "sender_session_id": "uuid-string",
  "recipient_session_id": "uuid-string",
  "sender_email": "sender@example.com",
  "recipient_email": "recipient@example.com",
  "expires_in_minutes": 10
}

Error Responses:
- 400: Invalid email addresses
- 401: User not found
- 500: Server error
```

#### Step 2: Verify Sender OTP
```
POST /api/secure-share/encrypt/verify-otp
Content-Type: application/json
Headers:
  - user-email: sender@example.com
  - user-role: sender

Request Body:
{
  "session_id": "uuid-string",
  "otp_code": "123456"
}

Response:
{
  "success": true,
  "message": "Sender OTP verified",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "session_id": "uuid-string"
}

Error Responses:
- 400: Invalid or expired OTP
- 401: Email mismatch or unauthorized role
- 500: Server error
```

#### Step 3: Verify Recipient OTP
```
POST /api/secure-share/encrypt/verify-otp
Content-Type: application/json
Headers:
  - user-email: recipient@example.com
  - user-role: recipient

Request Body:
{
  "session_id": "uuid-string",
  "otp_code": "654321"
}

Response:
{
  "success": true,
  "message": "Recipient OTP verified",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "session_id": "uuid-string"
}
```

#### Step 4: Upload and Encrypt File
```
POST /api/secure-share/encrypt/upload
Content-Type: multipart/form-data
Headers:
  - sender-email: sender@example.com
  - recipient-email: recipient@example.com
  - password: encryption_password_123
  - authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Request Body:
{
  "file": <binary file data>
}

Response:
{
  "success": true,
  "message": "File encrypted and uploaded successfully",
  "share_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "recipient_email": "recipient@example.com",
  "sender_email": "sender@example.com",
  "file_info": {
    "filename": "document.pdf",
    "size": 1024000,
    "mime_type": "application/pdf"
  },
  "status": "awaiting_recipient_verification"
}

Error Responses:
- 400: Invalid file or password too weak
- 401: Invalid token or unauthorized
- 413: File exceeds 200MB limit
- 500: Encryption failed
```

### 2. DECRYPTION PHASE

#### Step 1: Request Decryption Access
```
POST /api/secure-share/decrypt/request
Content-Type: application/json

Request Body:
{
  "share_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "recipient_email": "recipient@example.com"
}

Response:
{
  "success": true,
  "message": "OTP sent to recipient email",
  "session_id": "uuid-string",
  "recipient_email": "recipient@example.com",
  "expires_in_minutes": 10
}

Error Responses:
- 401: Not authorized as recipient
- 404: File share not found
- 410: File share has expired
- 500: Server error
```

#### Step 2: Verify Decryption OTP
```
POST /api/secure-share/decrypt/verify-otp
Content-Type: application/json
Headers:
  - recipient-email: recipient@example.com

Request Body:
{
  "session_id": "uuid-string",
  "otp_code": "123456"
}

Response:
{
  "success": true,
  "message": "OTP verified. Ready to decrypt.",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "share_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "file_info": {
    "filename": "document.pdf",
    "size": 1024000,
    "mime_type": "application/pdf"
  }
}

Error Responses:
- 400: Invalid or expired OTP
- 401: Email mismatch
- 404: File share not found
- 500: Server error
```

#### Step 3: Decrypt and Download File
```
POST /api/secure-share/decrypt/download
Content-Type: application/json
Headers:
  - recipient-email: recipient@example.com
  - authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Request Body:
{
  "share_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "password": "encryption_password_123"
}

Response:
{
  "success": true,
  "message": "File decrypted successfully",
  "share_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "file_data": "<base64-encoded-binary-data>",
  "metadata": {
    "filename": "document.pdf",
    "file_size": 1024000,
    "mime_type": "application/pdf",
    "file_extension": ".pdf",
    "checksum": "sha256-hash...",
    "format_version": "1.0"
  },
  "file_info": {
    "filename": "document.pdf",
    "size": 1024000,
    "mime_type": "application/pdf",
    "extension": ".pdf"
  }
}

Error Responses:
- 400: Invalid password or file integrity check failed
- 401: Invalid token or unauthorized
- 404: File share not found
- 500: Decryption failed
```

### 3. STATUS & INFORMATION ENDPOINTS

#### Get User's Sent Shares
```
GET /api/secure-share/shares/sent
Headers:
  - authorization: Bearer <jwt-token>

Response:
{
  "success": true,
  "email": "sender@example.com",
  "shares": [
    {
      "share_id": "uuid-string",
      "recipient_email": "recipient@example.com",
      "filename": "document.pdf",
      "status": "active",
      "created_at": "2026-05-28T10:30:00",
      "accessed_at": "2026-05-28T14:45:00"
    }
  ]
}
```

#### Get User's Received Shares
```
GET /api/secure-share/shares/received
Headers:
  - authorization: Bearer <jwt-token>

Response:
{
  "success": true,
  "email": "recipient@example.com",
  "shares": [
    {
      "share_id": "uuid-string",
      "sender_email": "sender@example.com",
      "filename": "document.pdf",
      "size": 1024000,
      "mime_type": "application/pdf",
      "status": "active",
      "created_at": "2026-05-28T10:30:00",
      "expires_at": "2026-05-30T10:30:00"
    }
  ]
}
```

#### Get Share Information
```
GET /api/secure-share/share/{share_id}/info
Headers:
  - authorization: Bearer <jwt-token>

Response:
{
  "success": true,
  "share": {
    "share_id": "uuid-string",
    "sender_email": "sender@example.com",
    "recipient_email": "recipient@example.com",
    "filename": "document.pdf",
    "size": 1024000,
    "mime_type": "application/pdf",
    "status": "active",
    "sender_verified": true,
    "recipient_verified": true,
    "created_at": "2026-05-28T10:30:00",
    "expires_at": "2026-05-30T10:30:00",
    "accessed_at": "2026-05-28T14:45:00"
  }
}
```

## Database Schema

### FileShare Table
```
- id: Integer (Primary Key)
- share_id: String (Unique, indexed)
- sender_email: String
- recipient_email: String
- original_filename: String
- file_size: Integer
- mime_type: String
- file_extension: String
- encrypted_file_path: String
- file_checksum: String (SHA-256)
- salt: String (hex)
- nonce: String (hex)
- encryption_key: String
- sender_otp_verified: Boolean
- recipient_otp_verified: Boolean
- sender_access_token: String
- recipient_access_token: String
- status: String (pending, active, accessed, expired)
- metadata: JSON
- created_at: DateTime
- expires_at: DateTime
- accessed_at: DateTime
```

### OTPSession Table
```
- id: Integer (Primary Key)
- session_id: String (Unique, indexed)
- email: String
- otp_code: String
- operation_type: String (sender, recipient, encryption, decryption)
- file_share_id: String
- is_verified: Boolean
- verification_attempts: Integer
- created_at: DateTime
- expires_at: DateTime
- verified_at: DateTime
```

## Implementation Steps

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Initialize Database**
```bash
python init_db.py
```

3. **Start Backend Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd secure-privacy-web
npm install
```

2. **Start Frontend**
```bash
npm run dev
```

3. **Access Application**
- Encryption: http://localhost:5173/secure-encryption
- Decryption: http://localhost:5173/secure-decryption

## File Format Specification

### Encrypted File Structure
```
[Metadata Length (4 bytes)]
[Metadata JSON (variable)]
[Encrypted File Data (variable)]

Encryption:
- Algorithm: AES-256-GCM
- Key Derivation: PBKDF2 (password + salt)
- IV/Nonce: 12 bytes random
- Salt: 16 bytes random
- Authentication Tag: Included in GCM output
```

### Metadata Format
```json
{
  "filename": "document.pdf",
  "file_size": 1024000,
  "mime_type": "application/pdf",
  "file_extension": ".pdf",
  "checksum": "sha256-hash-value",
  "format_version": "1.0"
}
```

## Security Best Practices

1. **Password Requirements**
   - Minimum 8 characters
   - Mix of uppercase, lowercase, digits, special characters
   - Target entropy > 80 bits

2. **OTP Security**
   - 6-digit codes
   - 10-minute expiration
   - Maximum 3 verification attempts
   - Throttled OTP generation (1 OTP per session)

3. **JWT Token Management**
   - Tokens expire after 60-120 minutes
   - Separate tokens for different operations
   - Token invalidation on role/permission change

4. **File Handling**
   - Maximum file size: 200MB
   - File integrity verified via SHA-256 checksum
   - Metadata preserved for exact reconstruction
   - Secure file deletion after expiration (configurable)

5. **Access Control**
   - Role-based: sender, recipient
   - Email-based validation
   - Two-factor authentication via OTP
   - Share expiration after 48 hours

## Error Handling

All errors follow standard HTTP status codes:

```
200: Success
400: Bad Request (validation error)
401: Unauthorized (authentication error)
403: Forbidden (authorization error)
404: Not Found
410: Gone (resource expired)
413: Payload Too Large (file size)
500: Internal Server Error
```

## Testing

### Test Encryption Flow
```bash
curl -X POST http://localhost:8000/api/secure-share/encrypt/init \
  -H "Content-Type: application/json" \
  -d '{
    "sender_email": "sender@test.com",
    "recipient_email": "recipient@test.com"
  }'
```

### Test Decryption Flow
```bash
curl -X POST http://localhost:8000/api/secure-share/decrypt/request \
  -H "Content-Type: application/json" \
  -d '{
    "share_id": "uuid-string",
    "recipient_email": "recipient@test.com"
  }'
```

## Performance Considerations

- File encryption: ~100MB/sec
- File decryption: ~100MB/sec
- OTP delivery: <5 seconds
- Database queries: <100ms (indexed)

## Future Enhancements

1. Batch file sharing
2. Partial file access (segmented download)
3. Share revocation before expiration
4. Custom expiration periods
5. Email notifications on access
6. Share activity timeline
7. Encryption algorithm selection
8. Password strength enforcement
9. Biometric authentication for OTP bypass
10. Blockchain audit trail

## Support

For issues or questions:
- Check API response error messages
- Review server logs
- Verify email configuration
- Ensure database connectivity
- Check file system permissions

---
**Version**: 1.0
**Last Updated**: May 28, 2026
**Status**: Production Ready
