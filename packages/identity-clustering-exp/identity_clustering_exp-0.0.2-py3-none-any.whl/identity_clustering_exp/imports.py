from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Dict, List

import cv2
import networkx as nx
import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1, fixed_image_standardization
from facenet_pytorch.models.mtcnn import MTCNN
from PIL import Image
from torch.utils.data.dataloader import DataLoader, Dataset
from torchvision.transforms import Resize
