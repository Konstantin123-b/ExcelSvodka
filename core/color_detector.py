from __future__ import annotations

import colorsys

from openpyxl.styles import PatternFill


class ColorDetector:

    @staticmethod
    def _rgb(fill: PatternFill) -> tuple[int, int, int] | None:

        if fill is None:
            return None

        color = fill.fgColor

        if color is None:
            return None

        if color.type != "rgb":
            return None

        rgb = color.rgb

        if rgb is None:
            return None

        # ARGB -> RGB
        if len(rgb) == 8:
            rgb = rgb[2:]

        try:
            return (
                int(rgb[0:2], 16),
                int(rgb[2:4], 16),
                int(rgb[4:6], 16),
            )
        except Exception:
            return None

    @classmethod
    def detect(cls, fill):

        rgb = cls._rgb(fill)

        if rgb is None:
            return None

        r, g, b = rgb

        # без заливки
        if (r, g, b) == (0, 0, 0):
            return None

        # RGB -> HSV
        h, s, v = colorsys.rgb_to_hsv(
            r / 255,
            g / 255,
            b / 255,
        )

        hue = h * 360
        sat = s * 100
        val = v * 100

        print(
            f"[HSV] RGB={rgb}  H={hue:.1f}  S={sat:.1f}  V={val:.1f}"
        )

        # слишком серый/бледный
        if sat < 30:
            return None

        # -----------------------------
        # Красный (ав)
        # -----------------------------
        if hue <= 20 or hue >= 340:
            print(" -> ав")
            return "ав"

        # -----------------------------
        # Коричневый (пл)
        # -----------------------------
        if 20 < hue <= 45:
            print(" -> пл")
            return "пл"

        # -----------------------------
        # Фиолетовый (з)
        # -----------------------------
        if 260 <= hue <= 320:
            print(" -> з")
            return "з"

        print(" -> ???")

        return None