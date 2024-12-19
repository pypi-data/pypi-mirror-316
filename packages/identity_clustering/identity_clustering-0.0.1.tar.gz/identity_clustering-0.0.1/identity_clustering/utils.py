import cv2
from PIL import Image


def _get_frames(video_path):
    """
    This function gets the video path, reads the video, stores
    the frames in a list and then returns
    """

    # List to store the video frames
    frames = []

    # Read and store video Frames
    capture = cv2.VideoCapture(video_path)
    frames_num = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    for _ in range(frames_num):
        capture.grab()
        success, frame = capture.retrieve()
        if not success:
            continue
        frames.append(frame)
    return frames


def _get_crop(frame, bbox, pad_constant: int | tuple):
    """
    This function takes a frame and a bounding box and outputs the region of the image
    given by the bounding box with padding applied to all four sides.

    Args:
        - frame (np.ndarray): The image frame containing the faces to be cropped.
        - bbox (list): The bounding box (xmin, ymin, xmax, ymax) for cropping.
        - pad_constant (int | tuple): The constant to control the padding.
          If an integer is provided, the same padding is applied in all directions.
          If a tuple (pad_w, pad_h) is provided, different padding is
          applied to width and height.

    Returns:
        - crop (np.ndarray): The cropped face region from the frame with padding.
    """

    # Extract bounding box coordinates
    xmin, ymin, xmax, ymax = [int(b * 2) for b in bbox]

    # Handle padding logic
    if isinstance(pad_constant, int):
        p_w = p_h = pad_constant
    elif isinstance(pad_constant, tuple) and len(pad_constant) == 2:
        p_w, p_h = pad_constant
    else:
        raise ValueError(
            "pad_constant should be either an int or a tuple of two values."
        )

    # Define padded crop area
    crop_ymin = max(ymin - p_h, 0)  # Ensure it doesn't go below 0
    crop_xmin = max(xmin - p_w, 0)  # Ensure it doesn't go left of 0
    crop_ymax = min(
        ymax + p_h, frame.shape[0]
    )  # Ensure it doesn't go beyond image height
    crop_xmax = min(
        xmax + p_w, frame.shape[1]
    )  # Ensure it doesn't go beyond image width

    # Extract the cropped region from the frame
    crop = frame[crop_ymin:crop_ymax, crop_xmin:crop_xmax]

    return crop


def extract_crops(video_path, bboxes_dict, pad_constant: int | tuple = 50):

    frames = _get_frames(video_path)
    crops = []
    keys = [int(x) for x in list(bboxes_dict.keys())]
    for i in range(0, len(frames)):
        frame = frames[i]
        if i not in keys:
            continue
        bboxes = bboxes_dict[i]
        if not bboxes:
            continue
        for bbox in bboxes:
            crop = _get_crop(frame, bbox, pad_constant)
            fram = _get_crop(frame, bbox, 0)

            # Add the extracted face to the list
            crops.append((i, Image.fromarray(crop), bbox, Image.fromarray(fram)))

    return crops
