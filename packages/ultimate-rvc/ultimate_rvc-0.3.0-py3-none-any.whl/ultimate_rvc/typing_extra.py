"""Extra typing for the Ultimate RVC project."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import IntEnum, StrEnum
from os import PathLike

type StrPath = str | PathLike[str]

type Json = Mapping[str, Json] | Sequence[Json] | str | int | float | bool | None


class SeparationModel(StrEnum):
    """The model to use for audio separation."""

    UVR_MDX_NET_VOC_FT = "UVR-MDX-NET-Voc_FT.onnx"
    UVR_MDX_NET_KARA_2 = "UVR_MDXNET_KARA_2.onnx"
    REVERB_HQ_BY_FOXJOY = "Reverb_HQ_By_FoxJoy.onnx"


class SegmentSize(IntEnum):
    """The segment size to use for audio separation."""

    SEG_64 = 64
    SEG_128 = 128
    SEG_256 = 256
    SEG_512 = 512
    SEG_1024 = 1024
    SEG_2048 = 2048


class F0Method(StrEnum):
    """The method to use for pitch detection."""

    RMVPE = "rmvpe"
    CREPE = "crepe"
    CREPE_TINY = "crepe-tiny"
    FCPE = "fcpe"


class EmbedderModel(StrEnum):
    """The model to use for audio embedding."""

    CONTENTVEC = "contentvec"
    CHINESE_HUBERT_BASE = "chinese-hubert-base"
    JAPANESE_HUBERT_BASE = "japanese-hubert-base"
    KOREAN_HUBERT_BASE = "korean-hubert-base"
    CUSTOM = "custom"


class RVCContentType(StrEnum):
    """The valid types of content to convert with RVC."""

    VOCALS = "vocals"
    VOICE = "voice"
    SPEECH = "speech"
    AUDIO = "audio"


class SampleRate(IntEnum):
    """The sample rate of an audio file."""

    HZ_16000 = 16000
    HZ_44100 = 44100
    HZ_48000 = 48000
    HZ_96000 = 96000
    HZ_192000 = 192000


class AudioExt(StrEnum):
    """Audio file formats."""

    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"
    AAC = "aac"
