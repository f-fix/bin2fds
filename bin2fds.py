#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os.path
import sys

MFRS = {code: [en, ja] for (code, en, ja) in [
    [
        0,
        "<unlicensed>",
        "<非公認>"
    ],
    [
        1,
        "Nintendo",
        "任天堂"
    ],
    [
        8,
        "Capcom",
        "カプコン"
    ],
    [
        10,
        "Jaleco",
        "ジャレコ"
    ],
    [
        24,
        "Hudson Soft",
        "ハドソン"
    ],
    [
        73,
        "Irem",
        "アイレム"
    ],
    [
        74,
        "Gakken",
        "学習研究社"
    ],
    [
        139,
        "BulletProof Software (BPS)",
        "BPS"
    ],
    [
        153,
        "Pack-In-Video",
        "パックインビデオ"
    ],
    [
        155,
        "Tecmo",
        "テクモ"
    ],
    [
        156,
        "Imagineer",
        "イマジニア"
    ],
    [
        162,
        "Scorpion Soft",
        "スコーピオンソフト"
    ],
    [
        164,
        "Konami",
        "コナミ"
    ],
    [
        166,
        "Kawada Co., Ltd.",
        "河田"
    ],
    [
        167,
        "Takara",
        "タカラ"
    ],
    [
        168,
        "Royal Industries",
        "ロイヤル工業"
    ],
    [
        172,
        "Toei Animation",
        "東映動画"
    ],
    [
        175,
        "Namco",
        "ナムコ"
    ],
    [
        177,
        "ASCII Corporation",
        "アスキー"
    ],
    [
        178,
        "Bandai",
        "バンダイ"
    ],
    [
        179,
        "Soft Pro Inc.",
        "ソフトプロ"
    ],
    [
        182,
        "HAL Laboratory",
        "HAL研究所"
    ],
    [
        187,
        "Sunsoft",
        "サンソフト"
    ],
    [
        188,
        "Toshiba EMI",
        "東芝EMI"
    ],
    [
        192,
        "Taito",
        "タイトー"
    ],
    [
        193,
        "Sunsoft / Ask Co., Ltd.",
        "サンソフト アスク講談社"
    ],
    [
        194,
        "Kemco",
        "ケムコ"
    ],
    [
        195,
        "Square",
        "スクウェア"
    ],
    [
        196,
        "Tokuma Shoten",
        "徳間書店"
    ],
    [
        197,
        "Data East",
        "データイースト"
    ],
    [
        198,
        "Tonkin House/Tokyo Shoseki",
        "トンキンハウス"
    ],
    [
        199,
        "East Cube",
        "イーストキューブ"
    ],
    [
        202,
        "Konami / Ultra / Palcom",
        "コナミ"
    ],
    [
        203,
        "NTVIC / VAP",
        "バップ"
    ],
    [
        204,
        "Use Co., Ltd.",
        "ユース"
    ],
    [
        206,
        "Pony Canyon / FCI",
        "ポニーキャニオン"
    ],
    [
        209,
        "Sofel",
        "ソフエル"
    ],
    [
        210,
        "Bothtec, Inc.",
        "ボーステック"
    ],
    [
        219,
        "Hiro Co., Ltd.",
        "ヒロ"
    ],
    [
        231,
        "Athena",
        "アテナ"
    ],
    [
        235,
        "Atlus",
        "アトラス"
    ]
]}

def hexdump(bits, block_len):
    if block_len is None:
        block_len = 10
    i = -15
    while i < block_len:
        q = ''
        Q = ''
        if (i > len(bits)) and ((i + 16) <= block_len):
            if (i - 16) <= len(bits): print '...'
            i += 16
            continue
        print ('%04X ' % (i-1)),
        for j in xrange(16):
            if ((i + j) >= (block_len - 2)) or not (i + j):
                q = '\x1b[7m'
                Q = '\x1b[0m'
            elif (i + j) == 1:
                q = ''
                Q = ''
            if ((i + j) >= 0) and ((i + j) < len(bits)):
                print q+bits[i + j].encode('hex')+Q,
            else:
                print q+('  ' if (((i + j) >= block_len) or ((i + j) < 0)) else '><')+Q,
        s = ''
        Q = ''
        for j in xrange(16):
            if (i + j) < 0:
                s += ' '
            elif (i + j) < len(bits):
                if (i + j) in (0, block_len):
                    s += '\x1b[7m'
                    Q = '\x1b[0m'
                elif (i + j) == 1:
                    s += Q
                    Q = ''
                ch = ord(bits[i + j])
                if ch >= 0x20 and ch <= 0x7E:
                    s += chr(ch)
                else:
                    s += '.'
        print s+Q
        i += 16

def bin2fds(infnames, outfname):
    assert len(infnames) >= 1
    assert len(infnames) < 256
    assert not os.path.isfile(outfname)
    allfds = []
    for infname in infnames:
        disk_number = (len(allfds) // 2)
        side_number = len(allfds) % 2
        print('DISK %d SIDE %s (actual)' % (disk_number, 'AB'[side_number]))
        assert os.path.isfile(infname)
        bits = open(infname, 'rb').read()
        fds = ''
        skip = 26150//2//16
        bits = bits[skip:]
        print('SKIP: %d' % skip)
        next_file_size = 7
        last_type = 0
        ever_3 = False
        while bits:
            gap = 0
            skip_this_block = False
            while ((chr(ord(bits[:1])) == '\0' and (chr(ord(bits[1])) in '\0\1\2\3\4\5\7\x80')) or
                   (chr(0xFF ^ ord(bits[:1])) == '\0' and (chr(0xFF ^ ord(bits[1])) in '\0\1\2\3\4\5\7\x80'))):
                if False and (chr(0xFF ^ ord(bits[:1])) in '\0\1\2\3\4\5\7\x80'):
                    print('\x1B[7m FLIP \x1B[0m')
                    if next_file_size >= 0x70:
                        next_file_size = next_file_size >> 4
                    bits = ''.join(chr(0xFF ^ ord(ch)) for ch in bits)
                bits = bits[1:]
                gap += 1
            if gap and bits[:1] not in '\1\2\3\4\7':
                print('GAP: %d' % gap)
                if not bits: break
                if bits[0] != '\x80':
                    hexdump(bits, len(bits))
                if ord(bits[0]) == 0x80:
                    bits = bits[1:]
                else:
                    hexdump(bits, 1)
                    print('BAD PAD')
                    while bits[0:] == '\0': bits = bits[1:]
            block_type = ord(bits[0])
            if block_type == 7:
                block_type = 3
            if block_type > 4 or block_type == 0:
                hexdump(bits, len(bits))
                print('END OF DISK (%d more)' % len(bits))
                break
            if block_type == 4 and ever_3 and last_type != 3:
                hexdump(bits, len(bits))
                print('EXTRA FILE DATA, SKIPPING REST OF DISK (%d more)' % len(bits))
                break
            elif block_type == 4 and last_type != 3:
                skip_this_block = True
                hexdump(bits, len(bits))
                print('EXTRA FILE DATA, SKIPPING BLOCK')
            last_type = block_type
            ever_3 = ever_3 or (block_type == 3)
            block_len = {1: 58, 2: 4, 3: 18, 4: (next_file_size + 3)}.get(block_type, None)
            ok = False
            actual_crc = None
            expected_crc = None
            try:
                assert block_len >= 0
                assert len(bits) >= block_len
                chunk = bits[:(block_len - 2)]
                expected_crc = ord(bits[block_len - 2]) + 256 * ord(bits[block_len - 1])
                actual_crc = 0x8000
                for i in xrange(block_len):
                    byte = ord((chunk[i:][:1] + chr(0))[0])
                    for j in xrange(8):
                        bit = (byte >> j) & 1
                        carry = actual_crc & 1
                        actual_crc = (actual_crc >> 1) | (bit << 15)
                        if carry: actual_crc ^= 0x8408
                ok = True
                if actual_crc != expected_crc:
                    ok = False
            finally:
                print('BLOCK TYPE %d' % block_type),
                if block_len is not None:
                    print('LENGTH 0x%04X' % block_len)
                else:
                    print('LENGTH %s' % block_len)
                if not ok:
                    hexdump(bits, block_len)
                if expected_crc is not None:
                    print('BLOCK CRC (recorded) 0x%04X' % expected_crc)
                if actual_crc is not None:
                    print('BLOCK CRC (actual) 0x%04X' % actual_crc)
                if actual_crc != expected_crc:
                    print '\x1b[7m' + ' *** CRC MISMATCH *** ' + '\x1b[0m'
            next_file_size = 7
            if block_type == 1:
                assert chunk[1:15] == '*NINTENDO-HVC*'
                mfr = ord(chunk[15])
                print('MFR %d: %s\t%s' % (mfr, MFRS[mfr][0], MFRS[mfr][1]))
                game_name = chunk[16:19]
                game_type = chunk[19]
                game_version = ord(chunk[20])
                print('GAME %s' % repr(game_name))
                print('TYPE %s' % {' ': 'normal', 'E': 'event', 'R': 'reduced price'}.get(game_type, repr(game_type)))
                print('VER %d' % game_version)
                recorded_side_number = ord(chunk[21])
                recorded_disk_number = ord(chunk[22])
                print('DISK %d SIDE %s (recorded)' % (recorded_disk_number, 'AB'[recorded_side_number]))
            elif block_type == 2:
                file_count = ord(chunk[1])
                print('FILE COUNT %d' % file_count)
            elif block_type == 3:
                file_number = ord(chunk[1])
                file_id = ord(chunk[2])
                file_name = chunk[3:11]
                load_addr = ord(chunk[11]) + 256 * ord(chunk[12])
                next_file_size = ord(chunk[13]) + 256 * ord(chunk[14])
                file_type = ord(chunk[15])
                print('FILE %d %s-%d %s SIZE 0x%04X @ 0x%04X' % (file_number, {0: 'PRG', 1: 'CHR', 2: 'NAM'}.get(file_type, repr(file_type)), file_id, repr(file_name), next_file_size, load_addr))
            if not skip_this_block:
                fds += bits[:(block_len - 2)]
            bits = bits[block_len:]
            skip = 480//16
            bits = bits[skip:]
            print('SKIP: %d' % skip)
        if len(fds) < 65500:
            fds = fds + (chr(0) * (65500 - len(fds)))
        assert len(fds) == 65500
        allfds.append(fds)
    hdr = 'FDS' + chr(0x1A) + chr(len(allfds))
    hdr = hdr + (chr(0) * (16 - len(hdr)))
    assert len(hdr) == 16
    open(outfname, 'wb').write(hdr + ''.join(allfds))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        infname, outfname = sys.argv[1:]
        infnames = [infname]
    else:
        infnames = sys.argv[1:][:-1]
        outfname = sys.argv[-1]
    bin2fds(infnames, outfname)
