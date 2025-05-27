# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import json, os, math
from collections import defaultdict
from collections import Counter
import ast
"""
Utilities for working with function program representations of questions.

Some of the metadata about what question node types are available etc are stored
in a JSON metadata file.
"""


# Handlers for answering questions. Each handler receives the scene structure
# that was output from Blender, the node, and a list of values that were output
# from each of the node's inputs; the handler should return the computed output
# value from this node.


def scene_handler(instance_struct, inputs, side_inputs):
  # Just return all objects in the scene
  return instance_struct['panels']


def make_filter_handler(attribute):
  def filter_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 1
    assert len(side_inputs) == 1
    value = side_inputs[0]
    output = []
    for obj in inputs[0]:
      atr = obj[attribute]
      if value == atr or value in atr:
        output.append(obj)
    return output
  return filter_handler


def unique_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  if len(inputs[0]) != 1:
    return '__INVALID__'
  return inputs[0][0]


def vg_relate_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 1
  output = set()
  for rel in scene_struct['relationships']:
    if rel['predicate'] == side_inputs[0] and rel['subject_idx'] == inputs[0]:
      output.add(rel['object_idx'])
  return sorted(list(output))



def relate_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 1
  relation = side_inputs[0]
  return scene_struct['relationships'][relation][inputs[0]]
    

def union_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  return sorted(list(set(inputs[0]) | set(inputs[1])))


def intersect_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  return sorted(list(set(inputs[0]) & set(inputs[1])))


def count_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  return len(inputs[0])


def make_same_attr_handler(attribute):
  def same_attr_handler(scene_struct, inputs, side_inputs):
    cache_key = '_same_%s' % attribute
    if cache_key not in scene_struct:
      cache = {}
      for i, obj1 in enumerate(scene_struct['objects']):
        same = []
        for j, obj2 in enumerate(scene_struct['objects']):
          if i != j and obj1[attribute] == obj2[attribute]:
            same.append(j)
        cache[i] = same
      scene_struct[cache_key] = cache

    cache = scene_struct[cache_key]
    assert len(inputs) == 1
    assert len(side_inputs) == 0
    return cache[inputs[0]]
  return same_attr_handler


def make_query_handler(attribute):
  def query_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 1
    assert len(side_inputs) == 0
    obj = inputs[0]
    assert attribute in obj
    val = obj[attribute]
    if type(val) == list and len(val) != 1:
      return '__INVALID__'
    elif type(val) == list and len(val) == 1:
      return val[0]
    else:
      return val
  return query_handler

def panel_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 1
  return scene_struct['panels'][side_inputs[0]]

def left_position_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 0
  output = []
  for obj in inputs[0]:
    atr = obj["position"]
    if atr == 'left':
      output.append(obj)
  return output


def right_position_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 0
  output = []
  for obj in inputs[0]:
    atr = obj["position"]
    if atr == 'right':
      output.append(obj)
  return output


def top_position_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 0
  output = []
  for obj in inputs[0]:
    atr = obj["position"]
    if atr == 'top':
      output.append(obj)
  return output


def down_position_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 0
  output = []
  for obj in inputs[0]:
    atr = obj["position"]
    if atr == 'bottom':
      output.append(obj)
  return output

def inner_position_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 0
  output = []
  for obj in inputs[0]:
    atr = obj["position"]
    if 'inner' in atr:
      output.append(obj)
  return output

def outer_position_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 0
  output = []
  for obj in inputs[0]:
    atr = obj["position"]
    if 'outer' in atr:
      output.append(obj)
  return output

def exist_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  assert len(side_inputs) == 0
  if len(inputs[0]) > 0:
    return "Yes"
  else:
    return "No"


def equal_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  if inputs[0] == inputs[1]:
    return "Yes"
  else:
    return "No"

def less_than_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  return inputs[0] < inputs[1]


def greater_than_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  return inputs[0] > inputs[1]

def compare_size_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  if inputs[0] == inputs[1]:
    return "The same"
  elif inputs[0] < inputs[1]:
    return "Smaller"
  else:
    return "Larger"

def compare_color_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  if inputs[0] == inputs[1]:
    return "The same"
  elif inputs[0] < inputs[1]:
    return "Darker"
  else:
    return "Brighter"

def compare_shape_handler(scene_struct, inputs, side_inputs):
  edge_order = {"triangle": 3, "square": 4, "pentagon": 5, "hexagon": 6, "circle": 7}
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  if edge_order[inputs[0]] == edge_order[inputs[1]]:
    return "The same"
  elif edge_order[inputs[0]] < edge_order[inputs[1]]:
    return "Fewer"
  else:
    return "More"

def compare_number_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  if inputs[0] == inputs[1]:
    return "The same"
  elif inputs[0] < inputs[1]:
    return "Fewer"
  else:
    return "More"
def compare_position_handler(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  if inputs[0] == "left" and inputs[1] == "right":
    return "Left"
  elif inputs[0] == "right" and inputs[1] == "left":
    return "Right"
  elif inputs[0] == "top" and inputs[1] == "bottom":
    return "Above"
  elif inputs[0] == "bottom" and inputs[1] == "top":
    return "Below"
  elif inputs[0] == "top-left":
    if inputs[1] == "top-right" or inputs[1] == "top-center":
      return "Left"
    elif inputs[1] == "bottom-left" or inputs[1] == "middle-left":
      return "Above"
    elif inputs[1] == "bottom-right" or inputs[1] == "middle-right" or inputs[1] == "bottom-center" or inputs[1] == "middle-center":
      return "Left and above"
  elif inputs[0] == "top-right":
    if inputs[1] == "top-left" or inputs[1] == "top-center":
      return "Right"
    elif inputs[1] == "bottom-right" or inputs[1] == "middle-right":
      return "Above"
    elif inputs[1] == "bottom-left" or inputs[1] == "middle-left" or inputs[1] == "bottom-center" or inputs[1] == "middle-center":
      return "Right and above"
  elif inputs[0] == "bottom-left":
    if inputs[1] == "top-left" or inputs[1] == "middle-left":
      return "Below"
    elif inputs[1] == "top-right" or inputs[1] == "middle-right" or inputs[1] == "middle-center" or inputs[1] == "top-center":
      return "Left and below"
    elif inputs[1] == "bottom-right" or inputs[1] == "bottom-center":
      return "Left"
  elif inputs[0] == "bottom-right":
    if inputs[1] == "top-left" or inputs[1] == "middle-left" or inputs[1] == "middle-center" or inputs[1] == "top-center":
      return "Right and below"
    elif inputs[1] == "top-right" or inputs[1] == "middle-right":
      return "Below"
    elif inputs[1] == "bottom-left" or inputs[1] == "bottom-center":
      return "Right"
  elif inputs[0] == "top-center":
    if inputs[1] == "top-left":
      return "Right"
    elif inputs[1] == "top-right":
      return "Left"
    elif inputs[1] == "bottom-center" or inputs[1] == "middle-center":
      return "Above"
    elif inputs[1] == "bottom-left" or inputs[1] == "middle-left":
      return "Right and above"
    elif inputs[1] == "bottom-right" or inputs[1] == "middle-right":
      return "Left and above"
  elif inputs[0] == "bottom-center":
    if inputs[1] == "bottom-left":
      return "Right"
    elif inputs[1] == "bottom-right":
      return "Left"
    elif inputs[1] == "top-left" or inputs[1] == "middle-left":
      return "Right and below"
    elif inputs[1] == "top-right" or inputs[1] == "middle-right":
      return "Left and below"
    elif inputs[1] == "top-center" or inputs[1] == "middle-center":
      return "Below"
  elif inputs[0] == "middle-left":
    if inputs[1] == "bottom-left":
      return "Above"
    elif inputs[1] == "top-left":
      return "Below"
    elif inputs[1] == "top-center" or inputs[1] == "top-right":
      return "Right and above"
    elif inputs[1] == "bottom-center" or inputs[1] == "bottom-right":
      return "Right and below"
    elif inputs[1] == "middle-center" or inputs[1] == "middle-right":
      return "Left"
  elif inputs[0] == "middle-right":
    if inputs[1] == "bottom-right":
      return "Above"
    elif inputs[1] == "top-right":
      return "Below"
    elif inputs[1] == "top-center" or inputs[1] == "top-left":
      return "Left and above"
    elif inputs[1] == "bottom-center" or inputs[1] == "bottom-left":
      return "Left and below"
    elif inputs[1] == "middle-left" or inputs[1] == "middle-center":
      return "Right"
  elif inputs[0] == "middle-center":
    if inputs[1] == "middle-right":
      return "Left"
    elif inputs[1] == "middle-left":
      return "Right"
    elif inputs[1] == "top-center":
      return "Below"
    elif inputs[1] == "bottom-center":
      return "Above"
    elif inputs[1] == "top-left":
      return "Right and below"
    elif inputs[1] == "bottom-right":
      return "Left and above"
    elif inputs[1] == "top-right":
      return "Left and below"
    elif inputs[1] == "bottom-left":
      return "Right and above"

  elif inputs[0] == "outer-part":
    return "Outside"
  elif inputs[0] == "inner-part" and inputs[1] == "outer-part":
    return "Inside"
  elif inputs[0] == "top-left of the inner part":
    if inputs[1] == "top-right of the inner part":
      return "Left"
    elif inputs[1] == "bottom-left of the inner part":
      return "Above"
    elif inputs[1] == "bottom-right of the inner part":
      return "Left and above"
    elif inputs[1] == "outer-part":
      return "Inside"
  elif inputs[0] == "top-right of the inner part":
    if inputs[1] == "top-left of the inner part":
      return "Right"
    elif inputs[1] == "bottom-right of the inner part":
      return "Above"
    elif inputs[1] == "bottom-left of the inner part":
      return "Right and above"
    elif inputs[1] == "outer-part":
      return "Inside"
  elif inputs[0] == "bottom-left of the inner part":
    if inputs[1] == "top-left of the inner part":
      return "Below"
    elif inputs[1] == "bottom-right of the inner part":
      return "Right"
    elif inputs[1] == "top-right of the inner part":
      return "Left and below"
    elif inputs[1] == "outer-part":
      return "Inside"
  elif inputs[0] == "bottom-right of the inner part":
    if inputs[1] == "top-left of the inner part":
      return "Right and below"
    elif inputs[1] == "bottom-left of the inner part":
      return "Right"
    elif inputs[1] == "top-right of the inner part":
      return "Below"
    elif inputs[1] == "outer-part":
      return "Inside"


def all_color_equal_comparison(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  first_color = inputs[0][0]['color']
  if len(inputs[0]) == 1:
    return "__INVALID__"
  # Check if all objects have the same color
  if all(obj['color'] == first_color for obj in inputs[0]):
    return "Yes"
  else:
    return "No"

def all_shape_equal_comparison(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  first_shape = inputs[0][0]['shape']
  if len(inputs[0]) == 1:
    return "__INVALID__"
  # Check if all objects have the same color
  if all(obj['shape'] == first_shape for obj in inputs[0]):
    return "Yes"
  else:
    return "No"

def all_size_equal_comparison(scene_struct, inputs, side_inputs):
  assert len(inputs) == 1
  first_size = inputs[0][0]['size']
  if len(inputs[0]) == 1:
    return "__INVALID__"
  if inputs[0][0]['position'] == 'outer-part':
    return "No"
  # Check if all objects have the same color
  if all(obj['size'] == first_size for obj in inputs[0]):
    return "Yes"
  else:
    return "No"

def two_panel_shape_equal_comparison(scene_struct, inputs, side_inputs):
  edge_order = {"triangle": 3, "square": 4, "pentagon": 5, "hexagon": 6, "circle": 7}
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  first_shape = list(set([obj['shape'] for obj in inputs[0]]))
  second_shape = list(set([obj['shape'] for obj in inputs[1]]))
  if len(first_shape) > 1 or len(second_shape) > 1:
    return "Not comparable"
  elif edge_order[first_shape[0]] == edge_order[second_shape[0]]:
    return "The same"
  elif edge_order[first_shape[0]] < edge_order[second_shape[0]]:
    return "Fewer"
  else:
    return "More"

def two_panel_color_equal_comparison(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  first_color = list(set([obj['color'] for obj in inputs[0]]))
  second_color = list(set([obj['color'] for obj in inputs[1]]))
  if len(first_color) > 1 or len(second_color) > 1:
    return "Not comparable"
  elif first_color[0] == second_color[0]:
    return "The same"
  elif first_color[0] < second_color[0]:
    return "Darker"
  else:
    return "Brighter"

def two_panel_size_equal_comparison(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  first_size = list(set([obj['size'] for obj in inputs[0]]))
  second_size = list(set([obj['size'] for obj in inputs[1]]))
  if len(first_size) > 1 or len(second_size) > 1:
    return "Not comparable"
  elif first_size[0] == second_size[0]:
    return "The same"
  elif first_size[0] < second_size[0]:
    return "Smaller"
  else:
    return "Larger"

def two_panel_position_equal_comparison(scene_struct, inputs, side_inputs):
  assert len(inputs) == 2
  assert len(side_inputs) == 0
  first_position = list(set([obj['position'] for obj in inputs[0]]))
  second_position = list(set([obj['position'] for obj in inputs[1]]))
  if Counter(first_position) == Counter(second_position):
    return "Yes"
  else:
    return "No"

def query_number_rule_handler(scene_struct, inputs, side_inputs):
  assert len(side_inputs) == 1

  num_objects_in_first_panel = len(scene_struct['panels'][0])

  # Check if all other panels have the same number of objects
  for panel in scene_struct['panels']:
    if len(panel) != num_objects_in_first_panel:
      if side_inputs[0] == "Normal":
        rules = scene_struct['rules'][0]
        uniformity = ast.literal_eval(rules['uniformity'])['Grid']

      elif side_inputs[0] == "Left" or side_inputs[0] == "Up" or side_inputs[0] == "Out":
        rules = scene_struct['rules'][0]
        uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

      else:
        rules = scene_struct['rules'][1]
        uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

      for rule in rules['rules']:
        if 'Number' in rule['attr']:
          return describe_rule(rule['name'], rule['value'], 'Number')

      return "No clear rule is present."

  return "The number of objects remains constant."
def query_position_rule_handler(scene_struct, inputs, side_inputs):
  assert len(side_inputs) == 1
  if side_inputs[0] == "Normal":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])['Grid']

  elif side_inputs[0] == "Left" or side_inputs[0] == "Up" or side_inputs[0] == "Out":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  else:
    rules = scene_struct['rules'][1]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  for rule in rules['rules']:
    if 'Position' in rule['attr']:
      return describe_rule(rule['name'], rule['value'], 'Position')
  return "No clear rule is present."

def query_shape_rule_handler(scene_struct, inputs, side_inputs):
  assert len(side_inputs) == 1
  if side_inputs[0] == "Normal":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])['Grid']

  elif side_inputs[0] == "Left" or side_inputs[0] == "Up" or side_inputs[0] == "Out":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  else:
    rules = scene_struct['rules'][1]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  for rule in rules['rules']:
    if 'Type' in rule['attr']:
      first_rule_name = rules['rules'][0]['name']
      first_rule_type = rules['rules'][0]['attr']
      if uniformity == False and rule['name'] == 'Constant':
        if (first_rule_type == 'Position' and first_rule_name == 'Arithmetic') or (first_rule_type == 'Number'):
          return "No clear rule is present."
      return describe_rule(rule['name'], rule['value'], 'Type')
  return "No clear rule is present."

def query_size_rule_handler(scene_struct, inputs, side_inputs):
  assert len(side_inputs) == 1
  if side_inputs[0] == "Normal":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])['Grid']

  elif side_inputs[0] == "Left" or side_inputs[0] == "Up" or side_inputs[0] == "Out":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  else:
    rules = scene_struct['rules'][1]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  for rule in rules['rules']:
    if 'Size' in rule['attr']:
      first_rule_name = rules['rules'][0]['name']
      first_rule_type = rules['rules'][0]['attr']
      if uniformity == False and rule['name'] == 'Constant':
        if (first_rule_type == 'Position' and first_rule_name == 'Arithmetic') or (first_rule_type == 'Number'):
          return "No clear rule is present."
      return describe_rule(rule['name'], rule['value'], 'Size')
  return "No clear rule is present."

def query_color_rule_handler(scene_struct, inputs, side_inputs):
  assert len(side_inputs) == 1
  if side_inputs[0] == "Normal":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])['Grid']

  elif side_inputs[0] == "Left" or side_inputs[0] == "Up" or side_inputs[0] == "Out":
    rules = scene_struct['rules'][0]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  else:
    rules = scene_struct['rules'][1]
    uniformity = ast.literal_eval(rules['uniformity'])[side_inputs[0]]

  for rule in rules['rules']:
    if 'Color' in rule['attr']:
      first_rule_name = rules['rules'][0]['name']
      first_rule_type = rules['rules'][0]['attr']
      if uniformity == False and rule['name'] == 'Constant':
        if (first_rule_type == 'Position' and first_rule_name == 'Arithmetic') or (first_rule_type == 'Number'):
          return "No clear rule is present."
      return describe_rule(rule['name'], rule['value'], 'Color')
  return "No clear rule is present."

def describe_rule(name, value, type):
  if type == "Number":
    if name == "Progression":
      if value == "1":
        return "The number of objects gradually increases by 1."
      else:
        return "The number of objects gradually decreases by 1."
    elif name == "Arithmetic":
      if value == "1":
        return "The number of objects in the last panel equals the sum of the objects in the previous two panels."
      else:
        return "The number of objects in the last panel equals the difference between the objects in the previous two panels."
    elif name == "Distribute_Three":
      return "The number of objects distributes three distinct values across panels, rotating through each possible permutation of these values."
    elif name == "Constant":
      return "The number of objects remains constant."
  elif type == "Position":
    if name == "Arithmetic":
      if value == "-1":
        return "If an object is in the first panel but not in the second at corresponding position, it appears in the third panel."
      else:
        return "The position of objects in the last panel is the union of positions from the previous two panels."
    elif name == "Distribute_Three":
      return "Three distinct position settings across panels, rotating through each possible permutation of these settings."
    elif name == "Constant":
      return "The position of objects does not change across panels."
  elif type == "Type":
    if name == "Progression":
      if value == "1":
        return "The edge number of shape gradually increases by 1."
      else:
        return "The edge number of shape gradually decreases by 1."
    elif name == "Distribute_Three":
      return "Three distinct shapes across panels, rotating through each possible permutation of these shapes."
    elif name == "Constant":
      return "The shape remains constant."
  elif type == "Size":
    if name == "Progression":
      if value == "1":
        return "The size of objects gradually increases by a constant amount each time."
      else:
        return "The size of objects gradually decreases by a constant amount each time."
    elif name == "Arithmetic":
      if value == "1":
        return "The size of objects in the last panel is the sum of the sizes in the previous two panels."
      else:
        return "The size of objects in the last panel is the difference between the sizes in the previous two panels."
    elif name == "Distribute_Three":
      return "Three distinct sizes across panels, rotating through each possible permutation of these sizes."
    elif name == "Constant":
      return "The size remains constant."
  elif type == "Color":
    if name == "Progression":
      if value == "1":
        return "The color of objects gradually darkens by a constant amount each time."
      else:
        return "The color of objects gradually brightens by a constant amount each time."
    elif name == "Arithmetic":
      if value == "1":
        return "The color of objects in the last panel is the sum of the colors in the previous two panels."
      else:
        return "The color of objects in the last panel is the difference between the colors in the previous two panels."
    elif name == "Distribute_Three":
      return "Three distinct colors across panels, rotating through each possible permutation of these colors."
    elif name == "Constant":
      return "The color remains constant."

# Register all of the answering handlers here.
# TODO maybe this would be cleaner with a function decorator that takes
# care of registration? Not sure. Also what if we want to reuse the same engine
# for different sets of node types?
execute_handlers = {
  'scene': scene_handler,
  'filter_color': make_filter_handler('color'),
  'filter_shape': make_filter_handler('shape'),
  'filter_position': make_filter_handler('position'),
  'filter_size': make_filter_handler('size'),
  'filter_objectcategory': make_filter_handler('objectcategory'),
  'unique': unique_handler,
  'relate': relate_handler,
  'union': union_handler,
  'intersect': intersect_handler,
  'count': count_handler,
  'query_panel': panel_handler,
  'left_position_handler': left_position_handler,
  'right_position_handler': right_position_handler,
  'top_position_handler': top_position_handler,
  'down_position_handler': down_position_handler,
  'inner_position_handler': inner_position_handler,
  'outer_position_handler': outer_position_handler,
  'query_color': make_query_handler('color'),
  'query_shape': make_query_handler('shape'),
  'query_size': make_query_handler('size'),
  'query_position': make_query_handler('position'),
  'exist': exist_handler,
  'equal_color': equal_handler,
  'equal_shape': equal_handler,
  'equal_integer': equal_handler,
  'equal_material': equal_handler,
  'equal_size': equal_handler,
  'equal_object': equal_handler,
  'less_than': less_than_handler,
  'greater_than': greater_than_handler,
  'same_color': make_same_attr_handler('color'),
  'same_shape': make_same_attr_handler('shape'),
  'same_size': make_same_attr_handler('size'),
  'same_material': make_same_attr_handler('material'),
  'compare_size': compare_size_handler,
  'compare_color': compare_color_handler,
  'compare_position': compare_position_handler,
  'compare_shape': compare_shape_handler,
  'compare_number': compare_number_handler,
  'all_color_equal_comparison': all_color_equal_comparison,
  'all_shape_equal_comparison': all_shape_equal_comparison,
  'all_size_equal_comparison': all_size_equal_comparison,
  'two_panel_shape_equal_comparison': two_panel_shape_equal_comparison,
  'two_panel_color_equal_comparison': two_panel_color_equal_comparison,
  'two_panel_position_equal_comparison': two_panel_position_equal_comparison,
  'two_panel_size_equal_comparison': two_panel_size_equal_comparison,
  'query_number_rule': query_number_rule_handler,
  'query_shape_rule': query_shape_rule_handler,
  'query_color_rule': query_color_rule_handler,
  'query_size_rule': query_size_rule_handler,
  'query_position_rule': query_position_rule_handler,
}


def answer_question(question, metadata, instance_struct, all_outputs=False,
                    cache_outputs=True):
  """
  Use structured scene information to answer a structured question. Most of the
  heavy lifting is done by the execute handlers defined above.

  We cache node outputs in the node itself; this gives a nontrivial speedup
  when we want to answer many questions that share nodes on the same scene
  (such as during question-generation DFS). This will NOT work if the same
  nodes are executed on different scenes.
  """
  all_input_types, all_output_types = [], []
  node_outputs = []
  for node in question['nodes']:
    if cache_outputs and '_output' in node:
      node_output = node['_output']
    else:
      node_type = node['type']
      msg = 'Could not find handler for "%s"' % node_type
      assert node_type in execute_handlers, msg
      handler = execute_handlers[node_type]
      node_inputs = [node_outputs[idx] for idx in node['inputs']]
      side_inputs = node.get('side_inputs', [])
      node_output = handler(instance_struct, node_inputs, side_inputs)
      if cache_outputs:
        node['_output'] = node_output
    node_outputs.append(node_output)
    if node_output == '__INVALID__':
      break

  if all_outputs:
    return node_outputs
  else:
    return node_outputs[-1]


def insert_scene_node(nodes, idx):
  # First make a shallow-ish copy of the input
  new_nodes = []
  for node in nodes:
    new_node = {
      'type': node['type'],
      'inputs': node['inputs'],
    }
    if 'side_inputs' in node:
      new_node['side_inputs'] = node['side_inputs']
    new_nodes.append(new_node)

  # Replace the specified index with a scene node
  new_nodes[idx] = {'type': 'scene', 'inputs': []}

  # Search backwards from the last node to see which nodes are actually used
  output_used = [False] * len(new_nodes)
  idxs_to_check = [len(new_nodes) - 1]
  while idxs_to_check:
    cur_idx = idxs_to_check.pop()
    output_used[cur_idx] = True
    idxs_to_check.extend(new_nodes[cur_idx]['inputs'])

  # Iterate through nodes, keeping only those whose output is used;
  # at the same time build up a mapping from old idxs to new idxs
  old_idx_to_new_idx = {}
  new_nodes_trimmed = []
  for old_idx, node in enumerate(new_nodes):
    if output_used[old_idx]:
      new_idx = len(new_nodes_trimmed)
      new_nodes_trimmed.append(node)
      old_idx_to_new_idx[old_idx] = new_idx

  # Finally go through the list of trimmed nodes and change the inputs
  for node in new_nodes_trimmed:
    new_inputs = []
    for old_idx in node['inputs']:
      new_inputs.append(old_idx_to_new_idx[old_idx])
    node['inputs'] = new_inputs

  return new_nodes_trimmed


def is_degenerate(question, metadata, scene_struct, answer=None, verbose=False):
  """
  A question is degenerate if replacing any of its relate nodes with a scene
  node results in a question with the same answer.
  """
  if answer is None:
    answer = answer_question(question, metadata, scene_struct)

  for idx, node in enumerate(question['nodes']):
    if node['type'] == 'relate':
      new_question = {
        'nodes': insert_scene_node(question['nodes'], idx)
      }
      new_answer = answer_question(new_question, metadata, scene_struct)
      if verbose:
        print('here is truncated question:')
        for i, n in enumerate(new_question['nodes']):
          name = n['type']
          if 'side_inputs' in n:
            name = '%s[%s]' % (name, n['side_inputs'][0])
          print(i, name, n['_output'])
        print('new answer is: ', new_answer)

      if new_answer == answer:
        return True

  return False

