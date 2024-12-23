import base64
import json

from pydantic import BaseModel

from pipecat.frames.frames import AudioRawFrame, Frame, InputAudioRawFrame, StartInterruptionFrame
from pipecat.serializers.base_serializer import FrameSerializer, FrameSerializerType
from pipecat.audio.utils import pcm_to_ulaw, ulaw_to_pcm


class PlivoFrameSerializer(FrameSerializer):
    class InputParams(BaseModel):
        plivo_sample_rate: int = 8000
        sample_rate: int = 16000

    def __init__(self, stream_id: str, params: InputParams = InputParams()):
        self._stream_id = stream_id
        self._params = params

    @property
    def type(self) -> FrameSerializerType:
        return FrameSerializerType.TEXT

    def serialize(self, frame: Frame) -> str | bytes | None:
        if isinstance(frame, AudioRawFrame):
            data = frame.audio
            # Frame.sample_rate is 16000

            serialized_data = pcm_to_ulaw(data, frame.sample_rate, self._params.plivo_sample_rate)
            payload = base64.b64encode(serialized_data).decode("utf-8")
            answer = {
                "event": "playAudio",
                "streamId": self._stream_id,
                "media": {
                    "payload": payload,
                    "contentType": "audio/x-mulaw",
                    "sampleRate": self._params.plivo_sample_rate,
                },
            }

            return json.dumps(answer)

        if isinstance(frame, StartInterruptionFrame):
            answer = {"event": "clearAudio", "streamId": self._stream_id}
            return json.dumps(answer)

    def deserialize(self, data: str | bytes) -> Frame | None:
        # print("Deserialising data", data)
        message = json.loads(data)

        if message["event"] != "media":
            return None
        else:
            payload_base64 = message["media"]["payload"]
            payload = base64.b64decode(payload_base64)

            deserialized_data = ulaw_to_pcm(
                payload, self._params.plivo_sample_rate, self._params.sample_rate
            )
            audio_frame = InputAudioRawFrame(
                audio=deserialized_data, num_channels=1, sample_rate=self._params.sample_rate
            )
            # print("Audio frame", audio_frame.audio)
            return audio_frame
