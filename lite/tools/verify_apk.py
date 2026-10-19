"""Inspect actual ZIP entries; signature/package are checked by Android tools in CI."""
import sys
import zipfile
with zipfile.ZipFile(sys.argv[1]) as apk:
    assert apk.testzip() is None, 'Corrupt APK archive'
    names = apk.namelist()
    libs = [n for n in names if n.startswith('lib/') and n.endswith('.so')]
    assert libs, 'Missing native libraries'
    assert all(n.startswith('lib/arm64-v8a/') for n in libs), 'Unexpected ABI'
    # Upstream CMake JNI target is citra-android.
    assert 'lib/arm64-v8a/libcitra-android.so' in libs, 'Missing emulator core'
    assert apk.getinfo('lib/arm64-v8a/libcitra-android.so').file_size > 1_000_000
    assert 'AndroidManifest.xml' in names and 'classes.dex' in names
    print('APK structure OK:', len(libs), 'ARM64 native libraries')
