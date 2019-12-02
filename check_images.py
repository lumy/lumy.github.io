#!/usr/bin/env python3

import os
from pelicanconf import HEADER_COVERS, HEADER_COVER

IMAGES_DIR = "content/images"
CONTENT_ARTICLE = "content/"
CATEGORIES = []
USED_IMAGES = []
IMAGES = []

for dirpath, dirnames, filenames in os.walk(CONTENT_ARTICLE):
  if dirpath == CONTENT_ARTICLE or dirpath == "content/extra":
    continue
  elif dirpath == IMAGES_DIR:
    for file in filenames:
      IMAGES.append(os.path.join("images", file))
  else:
    for file in filenames:
      with open(os.path.join(dirpath, file), 'r') as f:
        for line in f.readlines():
          if "Category: " in line:
            cat = line[line.find(" "):line.find("\\")]
            if cat not in CATEGORIES:
              CATEGORIES.append(cat)
          else:
            if "images" in line:
              USED_IMAGES.append(line)
USED=[]
UNUSED = IMAGES.copy()
USED.append(HEADER_COVER[1:])
UNUSED.remove(HEADER_COVER[1:])
for cover in HEADER_COVERS.values():
  if cover:
    USED.append(cover[1:])
    UNUSED.remove(cover[1:])
for image in IMAGES:
  if any(image in used for used in USED_IMAGES):
    USED.append(image)
    UNUSED.remove(image)
print("Warning: There might be unused IMAGES. Please do not commit them if you don't use them")
for unused in UNUSED:
  print("Warning: %s might not be used" % unused)
if len(sys.argv) > 2:
  print("Used Images:")
  print(" ".join(USED))