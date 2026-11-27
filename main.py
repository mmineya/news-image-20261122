"""Validate and deliver the pre-rendered entry; Python 3.13, standard library only."""
import os
from pathlib import Path
import struct
import zlib


def validate_png(data: bytes) -> None:
    if len(data) > 1024 * 1024:
        raise ValueError('PNG exceeds 1 MiB')
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Invalid PNG signature')
    offset = 8
    chunks = []
    compressed = bytearray()
    ended = False
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError('Truncated PNG chunk')
        size, kind = struct.unpack_from('>I4s', data, offset)
        end = offset + 12 + size
        if end > len(data):
            raise ValueError('Truncated PNG payload')
        payload = data[offset + 8:offset + 8 + size]
        crc = struct.unpack_from('>I', data, offset + 8 + size)[0]
        if zlib.crc32(kind + payload) != crc:
            raise ValueError('PNG checksum mismatch')
        if not chunks and kind != b'IHDR':
            raise ValueError('Missing PNG header')
        if kind == b'IHDR':
            if chunks or size != 13:
                raise ValueError('Invalid PNG header')
            width, height, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', payload)
            if (width, height) != (1024, 1024):
                raise ValueError('PNG must be 1024x1024')
            if (depth, color, compression, filtering, interlace) != (8, 2, 0, 0, 0):
                raise ValueError('Expected an 8-bit RGB, noninterlaced PNG')
        elif kind == b'IDAT':
            if b'IDAT' in chunks and chunks[-1] != b'IDAT':
                raise ValueError('Nonconsecutive PNG image data')
            compressed.extend(payload)
        elif kind == b'IEND':
            if size or end != len(data) or not compressed:
                raise ValueError('Invalid PNG end')
            ended = True
        elif kind[0] & 32 == 0:
            raise ValueError('Unsupported critical PNG chunk')
        chunks.append(kind)
        offset = end
    if not ended:
        raise ValueError('Missing PNG end')
    expected = 1024 * (1 + 1024 * 3)
    decoder = zlib.decompressobj()
    raw = decoder.decompress(compressed, expected + 1)
    if len(raw) != expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError('Invalid PNG image data')
    if any(raw[i] > 4 for i in range(0, expected, 3073)):
        raise ValueError('Invalid PNG scanline filter')


def main() -> None:
    data = Path(__file__).with_name('entry.png').read_bytes()
    validate_png(data)
    output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    output.mkdir(parents=True, exist_ok=True)
    (output / 'entry.png').write_bytes(data)


if __name__ == '__main__':
    main()
