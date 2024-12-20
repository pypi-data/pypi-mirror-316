from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import List

import cv2
from facenet_pytorch.models.mtcnn import MTCNN
from PIL import Image
from torch.utils.data.dataloader import DataLoader, Dataset


class VideoFaceDetector(ABC):

    def __init__(self, **kwargs) -> None:
        super().__init__()

    @property
    @abstractmethod
    def _batch_size(self) -> int:
        pass

    @abstractmethod
    def _detect_faces(self, frames) -> List:
        pass


class FacenetDetector(VideoFaceDetector):

    def __init__(self, device="cuda:0") -> None:
        super().__init__()

        self.detector = MTCNN(
            device=device,
            thresholds=[0.85, 0.95, 0.95],
            margin=0,
        )

    def _detect_faces(self, frames) -> List:
        """
        passes all the frames of a video and then returns the bboxes
        of each frame into batch_boxes.
        """
        batch_boxes, *_ = self.detector.detect(frames, landmarks=False)
        if batch_boxes is None:
            return []
        return [b.tolist() if b is not None else None for b in batch_boxes]

    @property
    def _batch_size(self):
        return 32
