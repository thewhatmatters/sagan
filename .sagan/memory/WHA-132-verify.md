# WHA-132 verify retro

- **What blocked:** Vercel Deployment Protection (`ssoProtection: all_except_custom_domains`) returns 302 → SSO on every `*.vercel.app` URL of the project, including "stable" aliases. `protectionBypass` was null, and the automate-browser profile is not logged into Vercel, so prod content checks were unreachable. Creating a bypass secret would mutate project settings — out of verify's lane; left for PM.
- **What worked:** binding evidence without page access — Vercel API (`/v13/deployments/<url>`) gives `readyState`, `target`, and `githubCommitSha`, which matched local HEAD `dbbfcdf` exactly; TLS verified via `openssl s_client`; content AC verified against local `site/dist` (the literal deployment artifact per `vercel.json`), clearly labeled supplementary.
- **Gotchas for next run:**
  - `curl -sI` shows 302 + `_vercel_sso_nonce`, not 401 — recognize either as deployment protection.
  - A naive "did we land back on the deployment host" URL check passes spuriously: the SSO redirect embeds the deployment hostname literally in its query string. Check `new URL(page.url).host`, not substring.
  - `sagan-steel.vercel.app` (first alias in the API list) 404s while the others 302 — alias list is not all live.
  - Deployment meta had `gitDirty: 1` despite a matching commit SHA — worth flagging in evidence.
- **Standing ask:** once protection is off or sagan.run is attached (custom domains are exempt), re-run checks 1–4 against prod; local-dist numbers to beat: 6 requests, 0 third-party, 216,412 bytes.
