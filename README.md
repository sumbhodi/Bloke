# Bloke

Minimal Android app to run local LLMs (llama.cpp) on Pixel phones.

## What Works

- Minimal Kivy chat UI with text input, chat history, and send button
- Pre-built llama.cpp .so files (libllama.so, libggml*.so, libmtmd.so) for arm64-v8a
- ctypes wrapper to load .so files (stub for now)
- GitHub Actions workflow that builds APK with manual .so injection
- The "90s approach" that bypasses buildozer's broken packaging

## Architecture

```
Bloke/
├── Main.py                 # Kivy chat UI
├── llama_wrapper.py        # ctypes wrapper for llama.cpp
├── buildozer.spec          # Buildozer config (API 33, arm64-v8a)
└── .github/workflows/
    └── build-apk.yml       # CI/CD: download .so, build, inject, upload
```

## Requirements

- Python 3.10+
- Kivy
- Plyer
- Buildozer (for Android builds)
- Pre-built llama.cpp libraries (hosted as GitHub release)

## Local Development

```bash
# Install dependencies
pip install kivy plyer

# Run locally (without Android)
python Main.py
```

## Android Build

### Option 1: GitHub Actions (Recommended)

1. Create a GitHub release with your pre-built .so files:
   - Tag: `llama-libs-v1.0`
   - Upload: libllama.so, libggml.so, libggml-base.so, libggml-cpu.so, libmtmd.so

2. Update `.github/workflows/build-apk.yml` line 30 with your release URL

3. Push to main or trigger "Build APK" workflow manually

4. Download timestamped APK from workflow artifacts

### Option 2: Local Build

```bash
# Install buildozer
pip install buildozer cython==0.29.33

# Build APK
buildozer android debug

# Manual .so injection (if needed)
mkdir -p temp_inject/lib/arm64-v8a
cp path/to/*.so temp_inject/lib/arm64-v8a/
cd temp_inject && zip -r ../bin/*.apk lib/
```

## How It Works

1. Buildozer creates base APK with Python code
2. GitHub Actions downloads pre-built .so files from release
3. Manual injection: `zip` adds .so files to APK's `lib/arm64-v8a/`
4. ctypes loads `.so` files at runtime on Android
5. (Future) Call llama.cpp C API for inference

## Key Design Decisions

- **No llama-cpp-python**: Too heavy, packaging issues with buildozer
- **Manual .so injection**: Bypasses buildozer's broken lib packaging
- **Timestamped artifacts**: Prevents browser cache issues during testing
- **Source verification**: Catches issues before 20min buildozer run
- **Minimal UI**: Start simple, add features once basics work

## Current Status

- [x] Chat UI (Kivy)
- [x] ctypes wrapper (stub)
- [x] GitHub Actions build + injection
- [x] Timestamped APK artifacts
- [ ] Actual llama.cpp inference (TODO)
- [ ] Model loading UI
- [ ] Multi-turn conversation support

## License

Apache 2.0 - See [LICENSE](LICENSE)

## Contributing

This is a minimal proof-of-concept. Contributions welcome once core functionality is proven.

## Troubleshooting

**APK won't install:**
- Check Android version (need API 26+, Android 8.0+)
- Enable "Install from unknown sources"

**Build fails in GitHub Actions:**
- Verify .so files exist in GitHub release
- Check release URL in workflow file
- Review workflow logs for specific errors

**App crashes on launch:**
- Check logcat: `adb logcat | grep python`
- Verify .so files are in APK: `unzip -l app.apk | grep .so`
