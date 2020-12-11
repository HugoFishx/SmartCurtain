
# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Example using PyCoral to detect objects in a given image.
B
To run this code, you must attach an Edge TPU attached to the host and
install the Edge TPU runtime (`libedgetpu.so`) and `tflite_runtime`. For
device setup instructions, see coral.ai/docs/setup.

Example usage:
```
python3 detect_image.py \
  --model test_data/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels test_data/coco_labels.txt \
  --input test_data/grace_hopper.bmp \
  --output ${HOME}/grace_hopper_processed.bmp
```
"""

import argparse
import time
import sys
import os
from PIL import Image
from PIL import ImageDraw
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter


def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red')
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill='red')


def detect_func():

 ## parser = argparse.ArgumentParser(
     ## formatter_class=argparse.ArgumentDefaultsHelpFormatter)
 ## parser.add_argument('-m', '--model', required=True,
 ##                     help='File path of .tflite file')
 # parser.add_argument('-i', '--input', required=True,
   #                   help='File path of image to process')
 # parser.add_argument('-l', '--labels', help='File path of labels file')
 # parser.add_argument('-t', '--threshold', type=float, default=0.4,
  #                    help='Score threshold for detected objects')
 # parser.add_argument('-o', '--output',
  #                    help='File path for the result image with annotations')
 # parser.add_argument('-c', '--count', type=int, default=5,
 #                     help='Number of times to run inference')
#  args = parser.parse_args()

  labels = read_label_file('test_data/coco_labels.txt')
  interpreter = make_interpreter('test_data/ssd_mobilenet_v2_coco_quant_postprocess.tflite')
  interpreter.allocate_tensors()

  image = Image.open('pic.jpg')
  _, scale = common.set_resized_input(
      interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))

  print('----INFERENCE TIME----')
  print('Note: The first inference is slow because it includes',
        'loading the model into Edge TPU memory.')
  for _ in range(5):
    start = time.perf_counter()
    interpreter.invoke()
    inference_time = time.perf_counter() - start
    objs = detect.get_objects(interpreter, 0.4, scale)
    print('%.2f ms' % (inference_time * 1000))

  print('-------RESULTS--------')
  if not objs:
    print('No objects detected')
  
  people_flag = 0
  for obj in objs:
    if obj.id == 0:
        print('people detected!')
        people_flag = 1
    print(labels.get(obj.id, obj.id))
    print('  id:    ', obj.id)
    print('  score: ', obj.score)
    print('  bbox:  ', obj.bbox)

#  if args.output:
#    image = image.convert('RGB')
#    draw_objects(ImageDraw.Draw(image), objs, labels)
#   image.save(args.output)
#    image.show()

    return people_flag
if __name__ == '__main__':
  detect_func()
