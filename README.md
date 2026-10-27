<p align="center">
  <img src="assets/header.svg" width="840" alt="POLYMOOD: fast viewers for data that most software will not open, and careful tools for file formats that nobody documented">
</p>

<p align="center">
  <img src="assets/marquee.svg" width="840" alt="Welcome to my homepage. eoview and radview binaries are in their releases. Smithy is pre-alpha. Best viewed in 800x600. Sign my guestbook.">
</p>

<p align="center">
  <b>Welcome to my homepage!</b><br>
  Here I keep fast viewers for satellite, radar and other hard-to-open data,<br>
  and tools for old file formats that nobody documented. Click a button to visit a project.
</p>

<p align="center">
  <a href="https://github.com/polymood/eoview"><img src="assets/btn-eoview.svg" width="88" height="31" alt="eoview"></a>
  <a href="https://github.com/polymood/radview"><img src="assets/btn-radview.svg" width="88" height="31" alt="radview"></a>
  <a href="https://github.com/polymood/Smithy"><img src="assets/btn-smithy.svg" width="88" height="31" alt="Smithy"></a>
  <a href="https://github.com/polymood/tim2dump"><img src="assets/btn-tim2dump.svg" width="88" height="31" alt="tim2dump"></a>
  <a href="https://github.com/polymood/DocumentIndexer"><img src="assets/btn-docindex.svg" width="88" height="31" alt="DocumentIndexer"></a>
  <a href="https://github.com/polymood/nfod"><img src="assets/btn-nfod.svg" width="88" height="31" alt="nfod"></a>
  <a href="https://polymood.net"><img src="assets/btn-home.svg" width="88" height="31" alt="polymood.net"></a>
</p>

<p align="center"><img src="assets/rainbow.svg" width="840" height="6" alt=""></p>

<img src="assets/bar-remote.svg" width="840" alt="Remote sensing and imaging">

*Pixels from orbit and from radar, opened in seconds, at any size.*

| Project | What it does | Built with |
|---|---|---|
| **[eoview](https://github.com/polymood/eoview)** <img src="assets/new.svg" width="34" height="15" alt="new"><br><sub>[website](https://polymood.github.io/eoview/) &middot; [download](https://polymood.github.io/eoview/download.html)</sub> | Desktop viewer for Earth observation data: GeoTIFF and COG, JPEG 2000, NITF, EOPF Zarr, Sentinel-1, -2 and -3 SAFE, NetCDF-4 and HDF5. A chunk engine streams local files, HTTP and S3 while the interface stays fluid. Time series with a timeline, and a first 3D globe. Installers for Windows, Linux and macOS, with a signed self-update. | Rust, wgpu, egui |
| **[radview](https://github.com/polymood/radview)** | GPU viewer for SAR and ISAR imagery: NITF (SICD, SIDD), TIFF, BigTIFF and COG. Shows complex data as amplitude, phase, I or Q, opens files larger than 10 GB, and has editable color maps with a dB stretch. Release binaries come with checksums and build provenance. | Rust, wgpu, egui |

<img src="assets/bar-games.svg" width="840" alt="Game tooling and preservation">

*Old formats and old engines, treated with respect.*

| Project | What it does | Built with |
|---|---|---|
| **[Smithy](https://github.com/polymood/Smithy)**<br><sub>pre-alpha</sub> | Open-source mapping tools for Source engine games, built one useful piece at a time on the way to a Hammer++ replacement. Today: a texture browser that mounts VPKs, game detection from `gameinfo.txt`, lossless VMF round-trip, brush geometry and Python plugins. | C++, Qt 6 |
| **[tim2dump](https://github.com/polymood/tim2dump)** | Extracts PlayStation 2 TIM2 textures to BMP or PNG. Every pixel format, CLUT palettes, mipmaps and batch mode, plus GS register inspection and an ANSI preview in the terminal. | C++ |

<img src="assets/bar-docs.svg" width="840" alt="Documents and the terminal">

*Small tools that do one job well.*

| Project | What it does | Built with |
|---|---|---|
| **[DocumentIndexer](https://github.com/polymood/DocumentIndexer)** | Turns a pile of PDFs into a searchable library. It reads the text layer or runs OCR (Tesseract, or the DeepSeek-OCR vision model on a GPU), detects the language of each document, then feeds a Tantivy full-text index behind a desktop search interface. | Python, PySide6 |
| **[nfod](https://github.com/polymood/nfod)** | An NFO viewer for the terminal. One C file, one compiler command. | C |

<sub>Also here: [WerZatSongGUI](https://github.com/polymood/WerZatSongGUI), a desktop interface for WerZatSong, and [beautiful-python](https://github.com/polymood/beautiful-python), annotated examples of clean, idiomatic Python.</sub>

<p align="center"><img src="assets/rainbow.svg" width="840" height="6" alt=""></p>

<p align="center">
  <a href="https://github.com/polymood/polymood/issues/new?title=Guestbook%20entry&body=Hello%20polymood!"><img src="assets/btn-guestbook.svg" width="88" height="31" alt="Sign my guestbook"></a>
  <img src="assets/btn-800x600.svg" width="88" height="31" alt="Best viewed at 800x600">
  <img src="assets/btn-rust.svg" width="88" height="31" alt="Rust powered">
</p>

<p align="center">
  <img src="assets/construction.svg" width="360" height="54" alt="Under construction: this homepage is never finished">
</p>

<p align="center">
  <sub>Releases, changelogs and build instructions live in each repository.<br>
  Last updated: October 2026.</sub>
</p>
