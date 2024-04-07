# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_CCQgWBu0oliQ02SXPYyd02UR-zRvtyB
"""

import json
import re

relations_mapping = {
    "interact_with": "P1",
    "perform_in": "P2",
    "are_central_to": "P3",
    "utlises": "P4",
    "involved_in": "P5",
    "based_on": "P6",
    "relate_to": "P7",
    "require": "P8",
    "consider": "P9",
    "has_implications_for": "P10",
    "governs_or_guides": "P11",
    "is_affected_by": "P12",
    "certifies_or_validates": "P13",
    "regulates": "P14",
    "must_be": "P15",
    "must_not_be": "P16",
    "should_be": "P17",
    "should_not_be": "P18",
    "can_be": "P19",
    "cannot_be": "P20",
    "helps": "P21",
    "works_with": "P22",
    "contains": "P23",
    "applies_to": "P24",
    "does_not_apply_to": "P25"
}
# from google.colab import files

# labelStudioOutput = files.upload()

path = 'training_data/label_studio_data.json'
with open(path, "r") as file:
    data = json.load(file)


# print(data)

# for filename, content in labelStudioOutput.items():

#     json_string = content.decode('utf-8')
#     data = json.loads(json_string)
#     print("file loaded")

#     for item in data:
#       print(item)
# This splits the sents label by punctuation, so it'll split by whitespaces and punctuations like commas.
def split_text(text):
    return re.findall(r"[\w']+|[.,!?;]", text)


output_file = 'training_data/DocRed_format_of_labelStudio.json'
variable = []
title = "title: \"Legal text about AI\"\n"
variable.append(title)
DocRED_format = []

for item in data:

    title = "Legal text about AI"
    sentences = [split_text(item['data']['text'])]

    # The formatting for docRED
    vertex_set = []
    id_to_vertex_index = {}
    for annotation in item['annotations']:
        for result in annotation['result']:
            if 'value' in result and 'labels' in result['value']:
                for label in result['value']['labels']:
                    words = split_text(result['value']['text'])
                    word_found = False
                    for word in words:
                        if not word_found and word in sentences[0]:  # Check if the word is in the sentence
                            word_index = sentences[0].index(word)
                            word_count = len(words)
                            end_position = word_index + word_count
                            word_found = True
                            vertex = {
                                "pos": [word_index, end_position],
                                "type": label,
                                "sent_id": 0,
                                "name": result['value']['text']
                            }
                            id_to_vertex_index[result['id']] = len(vertex_set)
                            vertex_set.append([vertex])

    labels = []
    for annotation in item['annotations']:
        for result in annotation['result']:
            if result['type'] == 'relation' and len(result["labels"]) > 0 and result['labels'][0] in relations_mapping:
                if result['from_id'] in id_to_vertex_index and result['to_id'] in id_to_vertex_index:
                    label_info = {
                        "r": relations_mapping[result['labels'][0]],
                        "h": id_to_vertex_index[result['from_id']],
                        "t": id_to_vertex_index[result['to_id']],
                        "evidence": [0]
                    }
                    labels.append(label_info)

    # Construct the transformed item
    transformed_item = {
        "title": title,
        "sents": sentences,
        "vertexSet": vertex_set,
        "labels": labels
    }

    DocRED_format.append(transformed_item)

# Filter out relations with no labels
DocRED_format = [element for element in DocRED_format if len(element["labels"]) > 0]

with open(output_file, 'w') as outfile:
    json.dump(DocRED_format, outfile, indent=4)
