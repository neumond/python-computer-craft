from ._base import BasePeripheral


__all__ = ('SpeakerPeripheral', )


class SpeakerPeripheral(BasePeripheral):
    TYPE = 'speaker'

    def playNote(self, instrument: str, volume: int = 1, pitch: int = 1) -> bool:
        # instrument:
        # https://minecraft.gamepedia.com/Note_Block#Instruments
        # bass
        # basedrum
        # bell
        # chime
        # flute
        # guitar
        # hat
        # snare
        # xylophone
        # iron_xylophone
        # pling
        # banjo
        # bit
        # didgeridoo
        # cow_bell

        # volume 0..3
        # pitch 0..24
        return self._call(b'playNote', instrument, volume, pitch).take_bool()

    def playSound(self, sound: str, volume: int = 1, pitch: int = 1) -> bool:
        # volume 0..3
        # pitch 0..2
        return self._call(b'playSound', sound, volume, pitch).take_bool()
