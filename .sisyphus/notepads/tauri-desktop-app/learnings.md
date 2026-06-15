
## Task 25 - Tauri Desktop App Configuration
- Created all 6 config/source files manually under `desktop/`
- Tauri v2 configured with Rust backend (greet command) and web frontend wrapper
- `tauri.conf.json` references `../web/out` for frontend dist and `../web` for dev/build commands
- Intentionally skipped installing Rust toolchain / Tauri CLI / building — config only
