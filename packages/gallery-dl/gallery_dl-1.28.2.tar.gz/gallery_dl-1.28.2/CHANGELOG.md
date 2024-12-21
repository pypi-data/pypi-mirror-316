## 1.28.2 - 2024-12-20
### Extractors
#### Additions
- [cyberdrop] add extractor for media URLs ([#2496](https://github.com/mikf/gallery-dl/issues/2496))
- [itaku] add `search` extractor ([#6613](https://github.com/mikf/gallery-dl/issues/6613))
- [lofter] add initial support ([#650](https://github.com/mikf/gallery-dl/issues/650), [#2294](https://github.com/mikf/gallery-dl/issues/2294), [#4095](https://github.com/mikf/gallery-dl/issues/4095), [#4728](https://github.com/mikf/gallery-dl/issues/4728), [#5656](https://github.com/mikf/gallery-dl/issues/5656), [#6607](https://github.com/mikf/gallery-dl/issues/6607))
- [yiffverse] add support ([#6611](https://github.com/mikf/gallery-dl/issues/6611))
#### Fixes
- [facebook] decode Unicode surrogate pairs in metadata values ([#6599](https://github.com/mikf/gallery-dl/issues/6599))
- [zerochan] parse API responses manually when receiving invalid JSON ([#6632](https://github.com/mikf/gallery-dl/issues/6632))
- [zerochan] fix `source` metadata extraction when not logged in
#### Improvements
- [bilibili] extract files from `module_top` entries ([#6687](https://github.com/mikf/gallery-dl/issues/6687))
- [bilibili] support `/upload/opus` URLs ([#6687](https://github.com/mikf/gallery-dl/issues/6687))
- [bluesky] default to `posts` timeline when `reposts` or `quoted` is enabled ([#6583](https://github.com/mikf/gallery-dl/issues/6583))
- [common] simplify HTTP error messages
- [common] detect `DDoS-Guard` challenge pages
- [deviantart] improve `tiptap` markup to HTML conversion ([#6686](https://github.com/mikf/gallery-dl/issues/6686))
  - fix `KeyError: 'attrs'` for links without `href`
  - support `heading` content blocks
  - support `strike` text markers
- [instagram] extract `date` metadata for stories ([#6677](https://github.com/mikf/gallery-dl/issues/6677))
- [kemonoparty:favorite] support new URL format ([#6676](https://github.com/mikf/gallery-dl/issues/6676))
- [saint] support `saint2.cr` URLs ([#6692](https://github.com/mikf/gallery-dl/issues/6692))
- [tapas] improve extractor hierarchy ([#6680](https://github.com/mikf/gallery-dl/issues/6680))
#### Options
- [cohost] add `avatar` and `background` options ([#6656](https://github.com/mikf/gallery-dl/issues/6656))
### Miscellaneous
- support `*` wildcards for `parent>child` categories, for example `reddit>*` ([#6673](https://github.com/mikf/gallery-dl/issues/6673))
- use latest Firefox UA as default `user-agent`
- use random unused port for `"user-agent": "browser"` requests
