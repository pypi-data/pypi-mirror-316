import threading
import time
from queue import Queue

import cv2

from kano.profiler import FPSCounter


class VideoStreamer:
    """
    A class to stream video from a source (file or camera), continuously read frames, and store them in a queue.

    Args:
        source (str): Path to the video source or camera index.
        reconnect (bool): Whether to reconnect to the video source if the connection is lost. Default is True.
    """

    def __init__(self, source, reconnect=True):
        """
        Initializes the VideoStreamer class to stream video from the specified source.

        Args:
            source (str): The path to the video source or camera index.
            reconnect (bool): Whether to reconnect to the video source if the connection is lost.
        """
        self.source = source
        self.frame_queue = Queue(maxsize=5)
        thread = threading.Thread(target=self._read_frames)
        thread.start()
        self.stop = False
        self.reconnect = reconnect

    def _read_frames(self):
        """
        Continuously reads frames from the video source and stores them in a queue.

        If the video source is lost, it attempts to reconnect if `self.reconnect` is True.
        """
        cap = cv2.VideoCapture(self.source)

        if not cap.isOpened():
            raise ValueError("Error opening video source.")

        source_fps = cap.get(cv2.CAP_PROP_FPS)
        running = True
        fps_counter = FPSCounter()

        while running:
            ret, frame = cap.read()

            if not ret:
                if self.reconnect:
                    print("Reconnect...")
                    time.sleep(2)
                    cap = cv2.VideoCapture(self.source)
                    fps_counter = FPSCounter()
                    continue
                break

            fps_counter.update()
            fps_counter.keep_target_fps(source_fps)

            try:
                self.frame_queue.put_nowait(frame)
            except:
                pass

        cap.release()

    def get_latest_frame(self):
        """
        Retrieves the latest frame from the queue.

        Returns:
            frame (ndarray): The most recent frame from the video source.
        """
        return self.frame_queue.get()
