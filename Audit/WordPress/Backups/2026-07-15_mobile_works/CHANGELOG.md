# Mobile works gallery fix — 2026-07-15

## Problem

On the homepage mobile view, the "Наши работы" photo gallery was impossible to scroll:
touching a photo immediately opened the lightbox instead of allowing swipe/scroll.

## Root cause

1. `laser178-lightbox.js` attached `touchstart`/`touchmove`/`touchend` to each
   `.laser-works-item` individually. On a swipe, if the finger lifted over the same
   item it started on, the script treated it as a clean tap and opened the lightbox.
2. There was no mobile CSS for `.laser-works-grid`, so the grid stayed as 3 columns
   and did not provide a natural horizontal scroll area.

## Changes made

### 1. `laser178-lightbox.js` (uploaded to `/wp-content/plugins/`)

- Touch listeners are now attached to the whole `.laser-works-grid` container.
- A `touchend` only opens the lightbox if:
  - the touch started and ended on the same `.laser-works-item`;
  - finger movement did not exceed 10 px;
  - touch duration is under 300 ms.
- Desktop behavior remains unchanged (click / Enter / Space on each item).
- Version bumped to `1.1` in `laser178-style.php` enqueue.

### 2. `laser178-style.css` (uploaded to `/wp-content/plugins/`)

Added mobile media query (`max-width: 768px`) for `.laser-works-grid`:

- `display: flex` with `flex-wrap: nowrap`;
- `overflow-x: auto` for horizontal swipe scrolling;
- `scroll-snap-type: x mandatory`;
- each item is 75% width / max 280 px;
- `pointer-events: none` on images so the container handles touch events cleanly.

## Verification

- Open `https://laser178.ru/` on a mobile device or DevTools mobile emulation.
- Swipe left/right in the "Наши работы" block — it should scroll horizontally.
- Tap briefly on a photo — it should open the lightbox.
- Swipe up/down to scroll the page — the lightbox should not open.

## Backups

Server-side backups were created on the FTP server:

- `laser178-lightbox.js.bak_20260715_*`
- `laser178-style.css.bak_20260715_*`

Local copies downloaded to:
`/root/laser178-ai-framework/Audit/WordPress/Backups/2026-07-15_mobile_works/`
