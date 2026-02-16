# Security & Privacy Information

## What's Secure ✅

1. **Local Storage**: 
   - API keys stored in `.env` file (not exposed)
   - Chat history only in memory (deleted when app closes)
   - No database or permanent storage

2. **No Personal Data Collection**:
   - App doesn't ask for or store personal information
   - No registration or login required
   - No tracking or analytics

3. **Open Source**:
   - All code is visible and can be reviewed
   - No hidden functionality

## Privacy Considerations ⚠️

1. **AI Service (Groq)**:
   - Your messages are sent to Groq servers for processing
   - Groq may temporarily log conversations (check their privacy policy)
   - Don't share: phone numbers, addresses, bank details, passwords

2. **Network**:
   - Currently runs on HTTP (not HTTPS)
   - If accessing from phone, data travels over local network
   - Use only on trusted networks (your home WiFi)

## Best Practices 🛡️

1. **Don't Share**:
   - ❌ Phone numbers
   - ❌ Full addresses
   - ❌ Bank/payment details
   - ❌ Personal identification numbers
   - ✅ General farming questions are safe

2. **Safe to Share**:
   - ✅ Crop types
   - ✅ General location (city/district)
   - ✅ Farming problems
   - ✅ Weather questions

3. **For Production Use**:
   - Add HTTPS/SSL certificate
   - Add user authentication
   - Use your own AI model (self-hosted)
   - Add rate limiting
   - Implement data encryption

## Groq Privacy Policy
https://groq.com/privacy-policy/

## Recommendations

**For Family Use (Current Setup)**: ✅ Safe
- Use on home network only
- Don't share sensitive personal info
- Perfect for farming advice

**For Public/Commercial Use**: ⚠️ Needs Improvements
- Add HTTPS
- Add authentication
- Consider self-hosted AI
- Add data encryption
