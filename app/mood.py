from __future__ import annotations

import io

from PIL import Image, ImageChops, ImageStat, UnidentifiedImageError


MAX_IMAGE_BYTES = 20 * 1024 * 1024
MIN_WIDTH = 640
MIN_HEIGHT = 360
ANALYSIS_EDGE = 160
SATURATION_FLOOR = 24

SUFFIX_BY_FORMAT = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
    "TIFF": ".tif",
}

BRIGHTNESS_BANDS = (
    (0.22, "깊은 어둠", "midnight darkness with deep shadows",
     "very slow tempo, low register piano voicings, sparse muted arrangement"),
    (0.40, "어두운 저녁", "dim late-evening light",
     "slow tempo, warm mid-register piano, soft brushed drums"),
    (0.62, "차분한 실내광", "soft indoor lighting",
     "relaxed medium-slow tempo, balanced piano and bass interplay"),
    (1.01, "밝고 열린 빛", "bright open daylight",
     "light easy swing feel, brighter piano voicings, airy phrasing"),
)

SATURATION_BANDS = (
    (0.12, "절제된 색감", "muted desaturated palette",
     "restrained harmony with minimal ornamentation"),
    (0.26, "은은한 색감", "gentle restrained colors",
     "gentle extended chords and unhurried melodic lines"),
    (1.01, "선명한 색감", "vivid saturated colors",
     "rich extended jazz harmony and expressive melodic lines"),
)

CONTRAST_BANDS = (
    (0.25, "부드러운 대비", "hazy soft contrast",
     "even soft dynamics throughout"),
    (0.55, "고른 대비", "balanced contrast",
     "natural dynamic shaping between sections"),
    (1.01, "강한 명암", "dramatic high contrast",
     "wide dynamic range with expressive solo passages"),
)

WARMTH_BANDS = (
    (0.35, "차가운 색조", "cool blue tones",
     "spacious reverb and cool shimmering electric piano touches"),
    (0.65, "중립 색조", "neutral balanced tones",
     "natural acoustic room tone"),
    (1.01, "따뜻한 색조", "warm amber tones",
     "warm analog tone with close-miked upright bass"),
)


def select_band(bands: tuple, value: float) -> tuple[str, str, str]:
    for threshold, tag, visual, musical in bands:
        if value < threshold:
            return tag, visual, musical
    return bands[-1][1:]


def load_thumbnail(data: bytes) -> tuple[Image.Image, str]:
    if not data:
        raise ValueError("썸네일 이미지가 비어 있습니다.")
    if len(data) > MAX_IMAGE_BYTES:
        limit_mb = MAX_IMAGE_BYTES / 1_000_000
        raise ValueError(f"썸네일 이미지는 {limit_mb:.0f}MB 이하만 등록할 수 있습니다.")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
        raise ValueError("썸네일 이미지를 읽을 수 없습니다. JPG, PNG, WEBP 파일을 사용해 주세요.") from error

    suffix = SUFFIX_BY_FORMAT.get(image.format or "")
    if suffix is None:
        raise ValueError("지원하지 않는 이미지 형식입니다. JPG, PNG, WEBP 파일을 사용해 주세요.")
    if image.width < MIN_WIDTH or image.height < MIN_HEIGHT:
        raise ValueError(
            f"썸네일 이미지가 너무 작습니다. 최소 {MIN_WIDTH}×{MIN_HEIGHT} 이상이 필요합니다."
        )
    return image.convert("RGB"), suffix


def measure_chroma(hsv: Image.Image) -> float:
    """Mean absolute colorfulness.

    HSV saturation stays high on near-black colors, so a deep navy cover would
    read as vivid. Chroma is ``max - min`` of the RGB bands, which matches how
    washed out the picture actually looks.
    """
    chroma = ImageChops.multiply(hsv.getchannel(1), hsv.getchannel(2))
    return ImageStat.Stat(chroma).mean[0] / 255


def measure_warmth(hsv: Image.Image) -> float:
    hues = hsv.getchannel(0).tobytes()
    saturations = hsv.getchannel(1).tobytes()
    warm = 0.0
    cool = 0.0
    for hue, saturation in zip(hues, saturations):
        if saturation < SATURATION_FLOOR:
            continue
        weight = saturation / 255
        if hue < 43 or hue >= 234:
            warm += weight
        elif 106 <= hue < 200:
            cool += weight
    total = warm + cool
    if total == 0:
        return 0.5
    return warm / total


def dominant_palette(sample: Image.Image, colors: int = 5) -> list[str]:
    reduced = sample.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    palette = reduced.getpalette() or []
    counted = sorted(reduced.getcolors() or [], reverse=True)
    return [
        "#%02x%02x%02x" % tuple(palette[index * 3:index * 3 + 3])
        for _, index in counted
        if len(palette) >= index * 3 + 3
    ]


def analyze_mood(image: Image.Image) -> dict:
    sample = image.copy()
    sample.thumbnail((ANALYSIS_EDGE, ANALYSIS_EDGE), Image.Resampling.LANCZOS)

    hsv = sample.convert("HSV")
    luminance_stat = ImageStat.Stat(sample.convert("L"))
    brightness = luminance_stat.mean[0] / 255
    contrast = min(1.0, luminance_stat.stddev[0] / 64)
    saturation = measure_chroma(hsv)
    warmth = measure_warmth(hsv)

    axes = (
        select_band(BRIGHTNESS_BANDS, brightness),
        select_band(SATURATION_BANDS, saturation),
        select_band(CONTRAST_BANDS, contrast),
        select_band(WARMTH_BANDS, warmth),
    )
    tags = [tag for tag, _, _ in axes]
    visuals = [visual for _, visual, _ in axes]
    musical = [phrase for _, _, phrase in axes]

    return {
        "brightness": round(brightness, 3),
        "saturation": round(saturation, 3),
        "contrast": round(contrast, 3),
        "warmth": round(warmth, 3),
        "palette": dominant_palette(sample),
        "tags": tags,
        "summary": " · ".join(tags),
        "visualPhrase": ", ".join(visuals),
        "musicPhrase": ", ".join(musical),
        "width": image.width,
        "height": image.height,
    }


def analyze_thumbnail(data: bytes) -> tuple[Image.Image, str, dict]:
    image, suffix = load_thumbnail(data)
    return image, suffix, analyze_mood(image)
