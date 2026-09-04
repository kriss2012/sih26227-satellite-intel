# Data Sources

The evaluation environment goes offline after setup, so every dataset used must
be **downloaded and staged locally before the demo**, not fetched live.

## Sentinel-2 (optical, primary)
- Best for: buildings, roads, vegetation, water, general land-use change.
- Access (while online, during prep): Copernicus Data Space Ecosystem, or via
  `sentinelsat` / `pystac-client` against a STAC catalog.
- Pick a ~10km grid AOI, download 4-6 dates spanning at least a year for a
  visible change story (e.g. new construction).

## Sentinel-1 SAR
- Useful because SAR penetrates cloud cover — pairs well with Sentinel-2 gaps.
- Adds robustness to your false-alarm-suppression story: "confirmed by both
  optical and SAR" is a strong confidence signal to show judges.

## Landsat Collection 2
- Longer historical baseline (decades) if you want to show long-range change
  beyond what Sentinel-2 (2015+) covers.

## Bhuvan / ISRO open EO data
- India-focused; worth using if your demo AOI is in India — strengthens
  relevance to the Indian Army/DGIS context of the problem statement.

## Staging checklist (do this well before Sept 19's offline test)
- [ ] Raw imagery downloaded and converted to Cloud-Optimized GeoTIFF (COG)
- [ ] Embedding model weights downloaded locally (not fetched at runtime)
- [ ] Vector index pre-built and saved to disk
- [ ] All Python packages installed (no `pip install` at runtime)
- [ ] Frontend `npm install` run, `node_modules` present
- [ ] Test the full stack with the network adapter disabled
