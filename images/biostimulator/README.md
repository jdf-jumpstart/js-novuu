# Biostimulator images

## treatment-areas.png

The illustrated "treatment areas" face diagram shown in the **Treatment areas**
block on `biostimulator.html`. The dots and labels (Temples, Cheeks, Smile
lines, Jawline, Chin, Neck) are baked into this image.

- **Expected path:** `images/biostimulator/treatment-areas.png`
- **Native size used by the markup:** 1176 × 1338 px (portrait)

The pulse animation is **not** part of the image. It is an SVG overlay in
`biostimulator.html` (`.pulse-overlay`) whose `viewBox` is `0 0 1176 1338`, so
each `<circle class="halo">` is positioned in the image's native pixel space and
maps 1:1 onto the baked-in dots.

If you replace this image with a different size, update the `viewBox`, the `img`
`width`/`height`, and the halo `cx`/`cy` coordinates accordingly so the pulses
stay centered on the dots.
