from typing import Dict, List

import networkx as nx
import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1, fixed_image_standardization
from torch.utils.data.dataloader import DataLoader
from torchvision.transforms import Resize

from identity_clustering.dataset import VideoDataset
from identity_clustering.facedetector import FacenetDetector
from identity_clustering.utils import extract_crops


class FaceCluster:

    def __init__(
        self, crops=None, similarity_threshold: int = 0.85, device: str = "cpu"
    ):
        self.similarity_threshold = similarity_threshold
        self.device = torch.device(device)
        self.crops = crops

    def _set_crops(self, crops):
        self.crops = crops

    def _set_threshold(self, threshold):
        self.similarity_threshold = threshold

    def _preprocess_images(self, img, shape=[128, 128]):
        img = Resize(shape)(img)
        return img

    def _generate_connected_components(self, similarities):

        graph = nx.Graph()
        for i in range(len(similarities)):
            for j in range(len(similarities)):
                # take every face dot product value
                # with every other value except itself and compare with threshold, when
                # if the value is greater than the threshold then
                # add an edge between them to signify that they are the same face.
                if i != j and similarities[i, j] > self.similarity_threshold:
                    graph.add_edge(i, j)
        # get all the clustered components and add them to the resultant component list
        components_list = []
        for component in nx.connected_components(graph):
            components_list.append(list(component))
        # for memory optimization clear the graph that was created
        graph.clear()
        graph = None

        return components_list

    def cluster_faces(self, crops, threshold=None):

        if threshold:
            self._set_threshold(threshold)

        if crops:
            self._set_crops(crops)

        # Convert crops to PIL images
        crops_images = [row[1] for row in self.crops]

        # Extract the embeddings
        embeddings_extractor = (
            InceptionResnetV1(pretrained="vggface2").eval().to(self.device)
        )
        faces = [self._preprocess_images(face) for face in crops_images]
        faces = np.stack([np.uint8(face) for face in faces])
        faces = torch.as_tensor(faces)
        faces = faces.permute(0, 3, 1, 2).float()
        faces = fixed_image_standardization(faces)
        face_recognition_input = faces
        embeddings = []
        embeddings = embeddings_extractor(face_recognition_input.to(self.device))
        similarities = (
            torch.tensordot(embeddings, embeddings.T, dims=1).detach().cpu().numpy()
        )
        # dot product attention without scaling
        # similarities = np.dot(np.array(embeddings), np.array(embeddings).T)

        # use the helper function to generate clusters
        components = self._generate_connected_components(similarities)
        components = [sorted(component) for component in components]

        # assigning each cluster to a unique identity.
        clustered_faces = {}
        for identity_index, component in enumerate(components):
            for index, face_index in enumerate(component):
                component[index] = self.crops[face_index]

            clustered_faces[identity_index] = component

        return clustered_faces


def cluster(
    clust: FaceCluster,
    video_path: str,
    faces: List[tuple],
    pad_constant: int | tuple | None = 3,
) -> Dict[int, list]:
    crops = extract_crops(video_path, faces, pad_constant)
    clustered_faces = clust.cluster_faces(crops)
    return clustered_faces


def detect_faces(video_path, device):
    """
    video_path: str - Path to the video
    device: str - indicates whether to leverage CPU or GPU for processing
    """

    """
        We'll be using the facenet detector that is required to detect the faces
        present in each frame. This function is only responsible to return
        a dictionary that contains the bounding boxes of each frame.
        returns: 
            dict: dict template:
                {
                    frame_no: [[
                        [number, number, number, number],
                        [number, number, number, number],
                        ...
                        ...
                        [number, number, number, number]
                    ]]
                }
            int: fps of the video
    """
    detector = FacenetDetector(device=device)

    # Read the video and its information
    dataset = VideoDataset([video_path])
    loader = DataLoader(
        dataset, shuffle=False, num_workers=0, batch_size=1, collate_fn=lambda x: x
    )

    # Detect the faces
    for item in loader:
        bboxes = {}
        video, indices, fps, frames = item[0]
        """
            Update bboxes dict with the bounding boxes present in each frame with the 
            frame number as the index and 
            a two dimensional list containing the bounding boxes as the value. 
        """
        bboxes.update({i: b for i, b in zip(indices, detector._detect_faces(frames))})
        found_faces = False
        for key in list(bboxes.keys()):
            if isinstance(bboxes[key], list):
                found_faces = True
                break

        if not found_faces:
            return None, indices[-1]
    return bboxes, fps
