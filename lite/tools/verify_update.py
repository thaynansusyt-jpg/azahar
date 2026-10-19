"""Verify a real ARM64 APK and update identity against the previous release."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import zipfile


def output(command):
    return subprocess.check_output([str(x) for x in command], text=True, stderr=subprocess.STDOUT)


def inspect(apk, tools):
    signature = output([tools/'apksigner','verify','--verbose','--print-certs',apk])
    digest = re.search(r'Signer #1 certificate SHA-256 digest: ([0-9a-fA-F]+)', signature)
    assert digest, 'missing signer certificate'
    badging = output([tools/'aapt','dump','badging',apk])
    package = re.search(r"package: name='([^']+)' versionCode='(\d+)' versionName='([^']+)'",badging)
    assert package, 'missing package identity'
    assert "native-code: 'arm64-v8a'" in badging
    align = output([tools/'zipalign','-c','-P','16','4',apk])
    libraries = {}
    with zipfile.ZipFile(apk) as archive:
        assert archive.testzip() is None
        assert 'AndroidManifest.xml' in archive.namelist() and 'classes.dex' in archive.namelist()
        for info in archive.infolist():
            if not info.filename.startswith('lib/') or not info.filename.endswith('.so'):
                continue
            assert info.filename.startswith('lib/arm64-v8a/'), 'unexpected ABI'
            data = archive.read(info)
            assert data[:6] == b'\x7fELF\x02\x01', 'expected little-endian ELF64'
            assert struct.unpack_from('<H',data,18)[0] == 183, 'expected AArch64'
            libraries[info.filename] = len(data)
            if info.filename.endswith('/libcitra-android.so'):
                assert len(data) > 1_000_000
                assert b'Java_org_citra_citra_1emu_NativeLibrary_run__Ljava_lang_String_2' in data
        assert 'lib/arm64-v8a/libcitra-android.so' in libraries
    return {'file': str(apk), 'bytes': apk.stat().st_size,
            'sha256': hashlib.sha256(apk.read_bytes()).hexdigest(),
            'package': package[1], 'version_code':int(package[2]), 'version_name':package[3],
            'certificate_sha256':digest[1].lower(), 'libraries':libraries,
            'signature_verified':True,'zip_integrity':True,'zipalign_16k':True,
            'jni_run_present':True,'device_execution_tested':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('previous',type=Path)
    parser.add_argument('updated',type=Path)
    parser.add_argument('--build-tools',type=Path,required=True)
    args = parser.parse_args()
    old,new = inspect(args.previous,args.build_tools),inspect(args.updated,args.build_tools)
    assert old['package'] == new['package'] == 'org.azaharlite.emu'
    assert old['certificate_sha256'] == new['certificate_sha256'], 'update signer changed'
    assert new['version_code'] > old['version_code'], 'versionCode must increase'
    print(json.dumps({'previous':old,'updated':new,'update_identity_compatible':True},indent=2))

if __name__ == '__main__':
    main()
