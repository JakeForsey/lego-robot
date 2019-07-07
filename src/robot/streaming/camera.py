import io
import struct

import picamera

from robot.streaming.base import StreamBase


class ImageStream(StreamBase):

    def __init__(self, resolution="640x480", framerate=24, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._resolution = resolution
        self._framerate = framerate

    def _on_enter(self):
        self._camera = picamera.PiCamera(
            resolution=self._resolution,
            framerate=self._framerate
        )

    def _on_exit(self):
        self._camera.close()

    async def stream(self):
        connection = self.get_socket().makefile("wb")
        stream = io.BytesIO()

        try:
            for _ in self._camera.capture_continuous(
                    stream,
                    'jpeg',
                    use_video_port=True
            ):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                stream.seek(0)
                stream.truncate()

            connection.write(struct.pack('<L', 0))
        finally:
            connection.close()
