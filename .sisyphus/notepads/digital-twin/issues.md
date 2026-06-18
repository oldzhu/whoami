## Known Issues

### Hydration Warning on /settings (Next.js 16.2 + Turbopack)
- **Symptom**: Recoverable hydration mismatch on first load
- **Cause**: Next.js 16.2 Turbopack dev mode — `useRouter()` triggers client-side Suspense boundary not matching server render
- **Impact**: Cosmetic only. Disappears on refresh. Does NOT occur in production build (`npm run build`)
- **Status**: Known framework issue, will be resolved by Next.js update
