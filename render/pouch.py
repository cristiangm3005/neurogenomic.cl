"""Geometría compartida de la bolsa stand-up (textura y escena usan el mismo mapeo)."""
import math

W = 0.135        # ancho frontal (m)
H = 0.235        # alto
D0 = 0.078       # fondo del fuelle en la base
P = 3.2          # exponente superelipse (frente plano, cantos suaves)
NT = 220         # segmentos alrededor
NZ = 140         # anillos en altura
SEAL = 0.205     # desde aquí la bolsa queda plana (sello superior)


def depth(z):
    if z >= SEAL:
        return 0.0025
    k = z / SEAL
    d = D0 * (1 - k ** 2.4) ** 0.9
    # base: leve redondeo en los primeros mm
    if z < 0.008:
        d *= 0.86 + 0.14 * math.sin(z / 0.008 * math.pi / 2)
    return max(0.0025, d)


def width(z):
    w = W
    if z > SEAL:  # el sello superior es algo más ancho y plano
        w = W * 1.004
    if z < 0.006:
        w *= 0.97 + 0.03 * (z / 0.006)
    return w


def se(t, a, b):
    c, s = math.cos(t), math.sin(t)
    x = a * math.copysign(abs(c) ** (2 / P), c)
    y = b * math.copysign(abs(s) ** (2 / P), s)
    return x, y


def bulge(x, z):
    """Abombamiento del frente/espalda por el café que contiene."""
    if z >= SEAL:
        return 0.0
    k = max(0.0, 1 - (2 * x / W) ** 2)
    return 0.0065 * math.sin(math.pi * min(1.0, z / SEAL) ** 0.85) * k ** 1.4


def ring(z):
    """Puntos del anillo en z, desde la espalda (t=-3π/2) dando la vuelta; frente en t=-π/2 (y<0)."""
    a, b = width(z) / 2, depth(z) / 2
    pts = []
    for i in range(NT + 1):
        t = -1.5 * math.pi + 2 * math.pi * i / NT
        x, y = se(t, a, b)
        if b > 0:
            y += math.copysign(bulge(x, z), y) * min(1.0, abs(y) / b)
        pts.append((x, y))
    return pts


def arc_from_front(pts):
    """Longitud de arco firmada desde el centro frontal (positivo hacia +x)."""
    acc = [0.0]
    for i in range(1, len(pts)):
        acc.append(acc[-1] + math.dist(pts[i], pts[i - 1]))
    front = acc[NT // 2]
    return [a - front for a in acc]


# Perímetro máximo (base) define el ancho de la textura
_base = ring(0.02)
C0 = arc_from_front(_base)[-1] - arc_from_front(_base)[0]
TEX_X = (-C0 / 2, C0 / 2)


def point_at(X, Z):
    """Punto 3D (sin rotación de objeto) sobre la superficie a arco X desde el centro frontal y altura Z."""
    pts = ring(Z)
    s = arc_from_front(pts)
    for i in range(1, len(s)):
        if s[i - 1] <= X <= s[i]:
            f = (X - s[i - 1]) / (s[i] - s[i - 1] or 1)
            x = pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f
            y = pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f
            return (x, y, Z)
    return (pts[NT // 2][0], pts[NT // 2][1], Z)
