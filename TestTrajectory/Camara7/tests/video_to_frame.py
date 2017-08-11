from contextlib import closing
from videosequence import VideoSequence
import pdb

with closing(VideoSequence("got.mp4")) as frames:
  for idx, frame in enumerate(frames[100:]):
    if (idx % 60 == 0):
      frame.save("./frames/frame{:05d}.jpg".format(idx))