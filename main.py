import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tiles
import numpy as np
import cv2
from imgaug.augmenters import *

img = cv2.imread('cat.png', cv2.IMREAD_UNCHANGED)
print img.dtype
batch = np.tile(img[None], (64, 1, 1, 1))
print batch.dtype

def on_aug_file_modified():
    print 'File changed'
    with open('aug.txt', 'r') as f:
        code = f.read()
        try:
            seq = eval(code)
            print 'Updating ..'
            out_batch = seq.augment_images(batch)
            out_img = tiles.tiles(out_batch, 8, 8, 10, 10).astype(np.uint8)
            a = float(out_img.shape[0]) / float(out_img.shape[1])
            cv2.imshow('augmented batch', cv2.resize(out_img, (1500, int(a*1500.) )) )
        except Exception as e:
            print 'Exception'
            print e

on_aug_file_modified()
if __name__ == "__main__":

    class Handler(FileSystemEventHandler):

        @staticmethod
        def on_any_event(event):
            if event.event_type == 'modified' and event.src_path == './aug.txt':
                on_aug_file_modified()

    path = '.'
    observer = Observer()
    observer.schedule(Handler(), path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
            k = cv2.waitKey(100)
            if k == 32:
                on_aug_file_modified()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()