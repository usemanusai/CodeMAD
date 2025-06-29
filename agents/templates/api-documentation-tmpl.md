# {{API Name}} API Documentation

[[LLM: This template creates comprehensive API documentation. Follow the embedded instructions to populate each section based on the API specifications and requirements.]]

## Overview

### API Description
[[LLM: Provide a clear, concise description of what this API does and its primary purpose]]

### Base URL
```
{{Base URL for the API}}
```

### Version
**Current Version:** {{API Version}}

### Authentication
[[LLM: Describe the authentication method(s) used]]
- **Type:** {{Authentication type - API Key, OAuth 2.0, JWT, etc.}}
- **Location:** {{Where to include auth - Header, Query Parameter, etc.}}
- **Format:** {{Format of authentication}}

## Getting Started

### Prerequisites
[[LLM: List any prerequisites for using the API]]
- {{Prerequisite 1}}
- {{Prerequisite 2}}

### Quick Start
[[LLM: Provide a simple example of making your first API call]]

1. **Obtain API credentials**
   {{Instructions for getting API access}}

2. **Make your first request**
   ```bash
   curl -X GET "{{base_url}}/{{endpoint}}" \
     -H "Authorization: Bearer {{your_token}}"
   ```

3. **Expected response**
   ```json
   {
     "status": "success",
     "data": {}
   }
   ```

## Authentication

### API Key Authentication
[[LLM: If using API keys, provide detailed instructions]]

### OAuth 2.0 Flow
[[LLM: If using OAuth, document the complete flow]]

### Rate Limiting
- **Rate Limit:** {{requests per time period}}
- **Rate Limit Headers:** {{headers returned with rate limit info}}
- **Exceeded Limit Response:** {{what happens when limit is exceeded}}

## API Reference

### {{Resource Name}}

#### GET /{{endpoint}}
[[LLM: Document each endpoint with the following structure]]

**Description:** {{What this endpoint does}}

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| {{param1}} | {{type}} | {{Yes/No}} | {{Description}} |
| {{param2}} | {{type}} | {{Yes/No}} | {{Description}} |

**Request Example:**
```bash
curl -X GET "{{base_url}}/{{endpoint}}?param1=value1" \
  -H "Authorization: Bearer {{token}}" \
  -H "Content-Type: application/json"
```

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "id": "123",
    "name": "Example"
  },
  "meta": {
    "total": 1,
    "page": 1
  }
}
```

**Response Codes:**
| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

#### POST /{{endpoint}}
[[LLM: Repeat the above structure for each endpoint]]

## Data Models

### {{Model Name}}
[[LLM: Document each data model/schema]]

```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Field Descriptions:**
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier |
| name | string | Display name |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
```

### Common Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_REQUEST | 400 | Request format is invalid |
| UNAUTHORIZED | 401 | Authentication required |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| RATE_LIMITED | 429 | Rate limit exceeded |

## Code Examples

### JavaScript/Node.js
```javascript
const response = await fetch('{{base_url}}/{{endpoint}}', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

### Python
```python
import requests

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.get('{{base_url}}/{{endpoint}}', headers=headers)
data = response.json()
```

### cURL
```bash
curl -X GET "{{base_url}}/{{endpoint}}" \
  -H "Authorization: Bearer {{token}}" \
  -H "Content-Type: application/json"
```

## SDKs and Libraries

### Official SDKs
[[LLM: List any official SDKs available]]
- **JavaScript:** {{npm package or GitHub link}}
- **Python:** {{pip package or GitHub link}}
- **PHP:** {{composer package or GitHub link}}

## Changelog

### Version {{version}} - {{date}}
[[LLM: Document API changes and updates]]
- {{Change description}}
- {{Change description}}

## Support

### Getting Help
- **Documentation:** {{Link to full documentation}}
- **Support Email:** {{support email}}
- **Community Forum:** {{forum link}}
- **GitHub Issues:** {{GitHub issues link}}

### Status Page
**API Status:** {{Link to status page}}
