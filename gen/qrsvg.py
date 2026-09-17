#!/usr/bin/env python3
"""Tiny dependency-free QR Code encoder → inline SVG (byte mode, error-correction level M, versions 1–10).

Used by the web-daily generators (palette2048/play/build.py, quote2048/play/build.py) to print an
"install the app" QR next to the App Store CTA on desktop. Kept in the repo on purpose: the daily
rebuild runs under launchd with a plain Homebrew/system python3 that has no third-party packages, and
the pages must not call any external QR service/CDN.

Algorithm follows ISO/IEC 18004 (same structure as Project Nayuki's reference encoder). Verified
against segno (identical matrices for every mask) and by decoding the rendered page with jsQR.

  from qrsvg import qr_svg
  svg = qr_svg("https://apps.apple.com/app/id123?ct=x&mt=8", title="App Store QR")
"""
from html import escape

# version → (ec codewords per block, [(block count, data codewords per block), ...]) for level M
_M_BLOCKS = {
    1: (10, [(1, 16)]), 2: (16, [(1, 28)]), 3: (26, [(1, 44)]), 4: (18, [(2, 32)]),
    5: (24, [(2, 43)]), 6: (16, [(4, 27)]), 7: (18, [(4, 31)]), 8: (22, [(2, 38), (2, 39)]),
    9: (22, [(3, 36), (2, 37)]), 10: (26, [(4, 43), (1, 44)]),
}
_ALIGN = {1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30], 6: [6, 34],
          7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50]}
_ECL_M = 0  # format-info bits for level M
_PENALTY = (3, 3, 40, 10)
_MASKS = [
    lambda x, y: (x + y) % 2 == 0,
    lambda x, y: y % 2 == 0,
    lambda x, y: x % 3 == 0,
    lambda x, y: (x + y) % 3 == 0,
    lambda x, y: (x // 3 + y // 2) % 2 == 0,
    lambda x, y: x * y % 2 + x * y % 3 == 0,
    lambda x, y: (x * y % 2 + x * y % 3) % 2 == 0,
    lambda x, y: ((x + y) % 2 + x * y % 3) % 2 == 0,
]


# ─── Reed–Solomon over GF(256), polynomial 0x11D ─────────────────────────────
def _gf_mul(x, y):
    z = 0
    for i in range(7, -1, -1):
        z = (z << 1) ^ ((z >> 7) * 0x11D)
        z ^= ((y >> i) & 1) * x
    return z


def _rs_divisor(degree):
    result = [0] * (degree - 1) + [1]
    root = 1
    for _ in range(degree):
        for j in range(degree):
            result[j] = _gf_mul(result[j], root)
            if j + 1 < degree:
                result[j] ^= result[j + 1]
        root = _gf_mul(root, 0x02)
    return result


def _rs_remainder(data, divisor):
    result = [0] * len(divisor)
    for b in data:
        factor = b ^ result.pop(0)
        result.append(0)
        for i, coef in enumerate(divisor):
            result[i] ^= _gf_mul(coef, factor)
    return result


# ─── Encoding ────────────────────────────────────────────────────────────────
def _capacity(version):
    return sum(n * k for n, k in _M_BLOCKS[version][1])


def _data_codewords(data, version):
    bits = []

    def put(val, n):
        bits.extend((val >> i) & 1 for i in range(n - 1, -1, -1))

    put(0b0100, 4)                                   # byte mode
    put(len(data), 8 if version < 10 else 16)
    for b in data:
        put(b, 8)
    cap_bits = _capacity(version) * 8
    put(0, min(4, cap_bits - len(bits)))             # terminator
    put(0, (-len(bits)) % 8)
    out = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    pad = 0xEC
    while len(out) < _capacity(version):
        out.append(pad)
        pad ^= 0xEC ^ 0x11
    return out


def _interleave(codewords, version):
    ec_len, groups = _M_BLOCKS[version]
    divisor = _rs_divisor(ec_len)
    blocks, k = [], 0
    for count, size in groups:
        for _ in range(count):
            blocks.append(codewords[k:k + size])
            k += size
    ecs = [_rs_remainder(b, divisor) for b in blocks]
    out = []
    for i in range(max(len(b) for b in blocks)):
        out.extend(b[i] for b in blocks if i < len(b))
    for i in range(ec_len):
        out.extend(e[i] for e in ecs)
    return out


class _Matrix:
    def __init__(self, version):
        self.version = version
        self.size = version * 4 + 17
        n = self.size
        self.mod = [[False] * n for _ in range(n)]
        self.fn = [[False] * n for _ in range(n)]
        self._function_patterns()

    def set_fn(self, x, y, dark):
        self.mod[y][x] = dark
        self.fn[y][x] = True

    def _function_patterns(self):
        n = self.size
        for i in range(n):                           # timing
            self.set_fn(6, i, i % 2 == 0)
            self.set_fn(i, 6, i % 2 == 0)
        for cx, cy in ((3, 3), (n - 4, 3), (3, n - 4)):   # finders + separators
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < n and 0 <= y < n:
                        d = max(abs(dx), abs(dy))
                        self.set_fn(x, y, d not in (2, 4))
        pos = _ALIGN[self.version]
        last = len(pos) - 1
        for i, ay in enumerate(pos):
            for j, ax in enumerate(pos):
                if (i == 0 and j == 0) or (i == 0 and j == last) or (i == last and j == 0):
                    continue
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        self.set_fn(ax + dx, ay + dy, max(abs(dx), abs(dy)) != 1)
        self.draw_format(0)                          # reserve
        if self.version >= 7:
            rem = self.version
            for _ in range(12):
                rem = (rem << 1) ^ ((rem >> 11) * 0x1F25)
            bits = self.version << 12 | rem
            for i in range(18):
                bit = (bits >> i) & 1 == 1
                a, b = n - 11 + i % 3, i // 3
                self.set_fn(a, b, bit)
                self.set_fn(b, a, bit)

    def draw_format(self, mask):
        data = _ECL_M << 3 | mask
        rem = data
        for _ in range(10):
            rem = (rem << 1) ^ ((rem >> 9) * 0x537)
        bits = (data << 10 | rem) ^ 0x5412
        bit = lambda i: (bits >> i) & 1 == 1
        n = self.size
        for i in range(6):
            self.set_fn(8, i, bit(i))
        self.set_fn(8, 7, bit(6))
        self.set_fn(8, 8, bit(7))
        self.set_fn(7, 8, bit(8))
        for i in range(9, 15):
            self.set_fn(14 - i, 8, bit(i))
        for i in range(8):
            self.set_fn(n - 1 - i, 8, bit(i))
        for i in range(8, 15):
            self.set_fn(8, n - 15 + i, bit(i))
        self.set_fn(8, n - 8, True)                  # dark module

    def place(self, codewords):
        n, i, total = self.size, 0, len(codewords) * 8
        right = n - 1
        while right >= 1:
            if right == 6:
                right = 5
            for vert in range(n):
                for j in range(2):
                    x = right - j
                    y = n - 1 - vert if ((right + 1) & 2) == 0 else vert
                    if not self.fn[y][x] and i < total:
                        self.mod[y][x] = (codewords[i >> 3] >> (7 - (i & 7))) & 1 == 1
                        i += 1
            right -= 2

    def apply_mask(self, mask):
        f = _MASKS[mask]
        for y in range(self.size):
            for x in range(self.size):
                if not self.fn[y][x] and f(x, y):
                    self.mod[y][x] = not self.mod[y][x]

    def penalty(self):
        n, m, score = self.size, self.mod, 0

        def finder_count(hist):
            k = hist[1]
            core = k > 0 and hist[2] == k and hist[3] == k * 3 and hist[4] == k and hist[5] == k
            return ((1 if core and hist[0] >= k * 4 and hist[6] >= k else 0)
                    + (1 if core and hist[6] >= k * 4 and hist[0] >= k else 0))

        def add_hist(run, hist):
            if hist[0] == 0:
                run += n
            hist.insert(0, run)
            hist.pop()

        def terminate(color, run, hist):
            if color:
                add_hist(run, hist)
                run = 0
            run += n
            add_hist(run, hist)
            return finder_count(hist)

        for line in [[m[y][x] for x in range(n)] for y in range(n)] + [[m[y][x] for y in range(n)] for x in range(n)]:
            color, run, hist = False, 0, [0] * 7
            for c in line:
                if c == color:
                    run += 1
                    if run == 5:
                        score += _PENALTY[0]
                    elif run > 5:
                        score += 1
                else:
                    add_hist(run, hist)
                    if not color:
                        score += finder_count(hist) * _PENALTY[2]
                    color, run = c, 1
            score += terminate(color, run, hist) * _PENALTY[2]
        for y in range(n - 1):
            for x in range(n - 1):
                c = m[y][x]
                if c == m[y][x + 1] == m[y + 1][x] == m[y + 1][x + 1]:
                    score += _PENALTY[1]
        dark = sum(sum(r) for r in m)
        total = n * n
        k = (abs(dark * 20 - total * 10) + total - 1) // total - 1
        score += k * _PENALTY[3]
        return score


def qr_matrix(text, mask=None, version=None):
    """QR modules for `text` (UTF-8, byte mode, level M) as a list of rows of bools (True = dark)."""
    data = text.encode("utf-8")
    if version is None:
        version = next((v for v in _M_BLOCKS
                        if 4 + (8 if v < 10 else 16) + len(data) * 8 <= _capacity(v) * 8), None)
        if version is None:
            raise ValueError("text too long for qrsvg (max version 10-M)")
    codewords = _interleave(_data_codewords(data, version), version)
    mx = _Matrix(version)
    mx.place(codewords)
    if mask is None:
        best = None
        for msk in range(8):
            mx.apply_mask(msk)
            mx.draw_format(msk)
            p = mx.penalty()
            if best is None or p < best[0]:
                best = (p, msk)
            mx.apply_mask(msk)                       # undo (XOR)
        mask = best[1]
    mx.apply_mask(mask)
    mx.draw_format(mask)
    return mx.mod


def qr_svg(text, title="", quiet=4, css_class="qr-code"):
    """Inline SVG of the QR code: white quiet zone (so it scans on a black page) + one dark path."""
    m = qr_matrix(text)
    n = len(m)
    dim = n + 2 * quiet
    runs = []
    for y, row in enumerate(m):
        x = 0
        while x < n:
            if row[x]:
                s = x
                while x < n and row[x]:
                    x += 1
                runs.append(f"M{s + quiet} {y + quiet}h{x - s}")
            else:
                x += 1
    t = f"<title>{escape(title)}</title>" if title else ""
    return (f'<svg class="{css_class}" viewBox="0 0 {dim} {dim}" role="img" shape-rendering="crispEdges" '
            f'data-qr="{escape(text)}" xmlns="http://www.w3.org/2000/svg">{t}'
            f'<rect width="{dim}" height="{dim}" fill="#fff"/>'
            f'<path d="{"".join(runs)}" stroke="#000" stroke-width="1" transform="translate(0 .5)"/></svg>')


if __name__ == "__main__":
    import sys
    print(qr_svg(sys.argv[1] if len(sys.argv) > 1 else "https://www.kkirukstudio.com/"))
