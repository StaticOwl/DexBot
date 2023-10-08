import json
import os

input_file_path = "database/RC_2015-01"
output_file_path = "low_data_output.txt"
row_counter = 0
json_obj = {}

with open(input_file_path, 'r', encoding='utf8') as input_file, open(output_file_path, 'w', encoding='utf8') as output_file:
    for row in input_file:
        if row_counter >= 100:
            break
        row_obj = json.loads(row)
        row_obj_keys = row_obj.keys()
        json_obj_keys = json_obj.keys()
        duplicate_key = None
        for index, key in enumerate(row_obj_keys):
            if key in json_obj_keys:
                duplicate_key = index
                break
        if duplicate_key is not None:
            row_object_minimized = {}
            for index, key in enumerate(row_obj_keys):
                if index < duplicate_key:
                    row_object_minimized[key] = row_obj[key]
                else:
                    break
            json_obj.update(row_object_minimized)
            rearranged_json_obj = {}
            desired_key_order = ["name", "id", "body", "score", "ups", "downs", "gilded", "parent_id", "created_utc", "link_id", 
                                 "subreddit_id", "author_flair_css_class", "author_flair_text", "edited",
                                  "controversiality", "subreddit", "score_hidden", "author", "distinguished", "archived", 
                                  "retrieved_on"
                                ]
            rearranged_json_obj = {key: json_obj[key] for key in desired_key_order if key in json_obj}
            output_file.write(json.dumps(rearranged_json_obj)+"\n")
            json_obj = {}
            for index, key in enumerate(row_obj_keys):
                if index >= duplicate_key:
                    json_obj[key] = row_obj[key]
                else:
                    continue
        else:
            json_obj.update(row_obj)
        row_counter += 1

