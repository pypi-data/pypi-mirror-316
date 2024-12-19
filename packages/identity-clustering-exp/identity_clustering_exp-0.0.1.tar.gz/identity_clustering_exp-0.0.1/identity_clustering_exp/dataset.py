from collections import OrderedDict

import cv2
from PIL import Image
from torch.utils.data.dataloader import Dataset


class VideoDataset(Dataset):
    """
    Dataset class for fetching specific information about a video.
    The class requires a list of videos that it has to process.
    """

    def __init__(self, videos) -> None:
        super().__init__()
        self.videos = videos

    def __getitem__(self, index: int):
        """
        This function, picks a video and returns 4 values.
            str: Contains the name of the video
            list: List containing only the frame indices that are readable
            number: fps of the video
            list: a list containing all the frames as image arrays
        """
        video = self.videos[index]
        capture = cv2.VideoCapture(video)
        frames_num = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(capture.get(5))
        frames = OrderedDict()
        for i in range(frames_num):
            capture.grab()
            success, frame = capture.retrieve()
            if not success:
                continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = frame.resize(size=[s // 2 for s in frame.size])
            frames[i] = frame
        return video, list(frames.keys()), fps, list(frames.values())

    def __len__(self) -> int:
        return len(self.videos)
