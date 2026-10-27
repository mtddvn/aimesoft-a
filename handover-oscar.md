# Handover: Aimesoft 2.0 home pages A and B (Leo, 27/10/2026 22:30)

Task from Lewis (Tristan 21:22, due 23:30): two full home pages, A (light) and B (dark), live on aimesoft-a.ciaosoft.vn and aimesoft-b.ciaosoft.vn. Stopped at 22:25 on the coordinator's order (weekly token quota). Nothing was sent to Tristan.

## Rules that stay
1. Every fact, figure, customer logo, product line and news item must exist on aimesoft.com (EN) or aimesoft.com/vi/ (VI). Nothing invented. Source snapshots of 27/10 are in `home-v2/source-snapshots-2026-10-27/`. Each block in `home-v2/_gen/content.py` carries its source page.
2. Gates: Iris >= 8/10 at 1440 and at 390 for each page, Owl PASS on text and figures. Neither page has passed yet (see Status).
3. Hosting: one GitHub Pages repo per page on account `mtddvn` (gh is logged in), file `CNAME` = exact domain. DNS belongs to Tristan/Kane (zone ciaosoft.vn is on Kane's Cloudflare, not reachable by the cf CLI). Do not touch DNS.
4. The approved header + hero of each page must not change (pixel diff against `approval-block-v2/option-a-1440.png` and `option-b-1440.png`; A diff is 0.0% of pixels > 24, B is 0.02%).
5. No "minh hoạ", "demo", "placeholder" on any UI. No em/en dash, middle dot, emoji. Files in English. No `cd`, no `sh -c` in Bash (all paths absolute).
6. A page that has been sent to Iris/Owl is frozen: bump the version and archive before regenerating.

## Where things are (all under `/Users/ciaosoft/Claude/BRvault/Projects/Aimesoft website 2.0/home-v2/`)
- `_gen/content.py` shared copy EN+VI and links. `_gen/prep_assets.py` image prep. `_gen/build_a.py` and `_gen/build_b.py` generators (run with `/Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python`). `_gen/qa_full.py` full-page gate (14 widths x EN/VI; run in the foreground with a long timeout; its mobile scrollWidth check was fixed at 22:15 to compare with the requested width). `_gen/shot.py` screenshots. `_gen/deploy.sh <a|b> <version>` pushes `site-<x>/` to repo `mtddvn/aimesoft-<x>`. `_gen/deploy_preview.sh <a|b> <version>` pushes the same site without CNAME to `mtddvn/aimesoft-<x>-preview`.
- Sites: `site-a/`, `site-b/` (index.html + CNAME + .nojekyll + assets). Archives: `site-a-archive/0.1.1/`, `site-b-archive-0.1.0/` (the versions Iris and Owl reviewed).
- Screenshots: `shots-a/` (a-1440-en.png, a-390-en.png, -vi, per-section crops), `site-b-shots/` (b-1440-en.png, b-390-en.png, -vi, per-section crops).
- Content taken from aimesoft.com: home (aimesoft.com, /vi/), product pages aimeface, aimespeech, aimecard, aimegpt, products, services, company, press (EN and /vi/). Hero v2 is from `approval-block-v2/`.

## Repos and links (created, public)
| Repo | What | State at 22:30 |
|---|---|---|
| mtddvn/aimesoft-a | custom domain aimesoft-a.ciaosoft.vn | A 0.2.0-wip pushed, Pages building |
| mtddvn/aimesoft-b | custom domain aimesoft-b.ciaosoft.vn | B 0.2.0-wip pushed, Pages building |
| mtddvn/aimesoft-a-preview | no CNAME, temporary link | https://mtddvn.github.io/aimesoft-a-preview/ returns 200 |
| mtddvn/aimesoft-b-preview | no CNAME, temporary link | https://mtddvn.github.io/aimesoft-b-preview/ returns 200 |

The `*.ciaosoft.vn` names still return Cloudflare 520: both names resolve to Cloudflare proxy IPs (104.21.27.56, 172.67.141.119). A repo with a custom domain makes `mtddvn.github.io/aimesoft-a/` redirect (301) to that domain, so the plain github.io link is dead until DNS is fixed. That is why the two `-preview` repos exist.
DNS change needed (Tristan or Kane): for `aimesoft-a` and `aimesoft-b` replace the proxied A records by CNAME -> `mtddvn.github.io`, DNS only (grey cloud). Then in each repo's Pages settings tick "Enforce HTTPS" once the certificate is issued.

## Status
- B: Iris round 1 gave 7,3 (1440) and 6,8 (390), Owl round 1 FAIL (3 blockers). Round 2 (`site-b` 0.2.0, md5 71a98051...) fixes all of Iris C1-C5 and Owl's blockers; own gates 0 findings; NOT yet re-scored by Iris or Owl.
- A: Iris round 1 gave 7,4 (1440) and 6,8 (390), Owl round 1 FAIL (3 blockers: 390 EN scroll width 405 from over-long no-break chunk, VI "Chăm sóc khách hàng" overflow in the industries tile, AimeSpeech EN chips not verbatim). Round 2 (`site-a` 0.2.0-wip, md5 679fe939...) fixes those, redoes industries as ruled columns, CTA with the card-in-hand picture, type tiers, mobile height 12.2k -> 10.2k px. NOT yet re-scored. qa_full still flags orphans: EN `.p-ctasub` last line 2 words at >= 420 px (all widths), "face immediately" and "Speaker identification" at 600/1100/1180, "105-0022, Japan" at 1024; fix by binding 3 words or rewording, then rerun.

## Order of remaining work
1. A: fix the orphans above, rerun `qa_full.py` (expect 0), rerun `qa-deliverable.py` on index.html, archive as `site-a-archive/0.2.0`, freeze, send to Iris and Owl.
2. B: send `site-b` (0.2.0) to Iris and Owl as it stands.
3. Fix whatever they flag (one round each), rerun gates, redeploy with `_gen/deploy.sh` and `_gen/deploy_preview.sh`.
4. When both pass: take full-page screenshots (1440 and 390) with `shot.py`, name them `aimesoft-home-a-1440.png`, `aimesoft-home-a-390.png`, same for b, and submit to Lewis: 2 links per page (domain + github.io preview), screenshots, Iris scores, Owl result, and the DNS note above.
5. Re-check `curl -I http://aimesoft-a.ciaosoft.vn` after Tristan/Kane change DNS.

## Things Tristan may need to decide (from Owl)
- aimesoft.com contradicts itself: home says "200+ installations", the company page says "over 300". Pages use 200+ only.
- News dates differ between the EN and VI lists (VIIE: Oct 24, 2025 vs 29/09/2025; Top 10: Oct 15 vs 13/10/2025); pages mirror each language. The URLs end in 20250929 and 20251013, which match the VI dates.
- The Top 10 press body says "Top 1 Capabilities Group" and "Top 10 AIoT"; pages follow the headline and company page ("Top 10").
- The VI site has no VI version of the industries lede and a few lines; those stay EN or come from services-vi (noted in `content.py`).
- Footer phone: EN uses tel:+18553028668 (site has no country code), VI uses +84 98-538-7426 as the VI site header does.

## Lessons to add to `Brain Identity/Leo/METHOD — Leo.md` (not yet written there)
- A gate that measures overflow against `innerWidth` in mobile emulation is blind: the layout viewport widens with the content. Compare `scrollWidth` with the requested width.
- Binding the last 3 words with no-break spaces can create a chunk wider than a narrow column (390 scroll width 405). Cap the chunk length and let `text-wrap-style:pretty` do the rest.
- Vietnamese compound lists with no-break wrappers must stay short (under 15 characters); a long one ("chăm sóc khách hàng") overflowed a tile.
- A repo with a custom domain redirects its github.io URL to the domain; keep a separate no-CNAME preview repo when DNS is not ready.
