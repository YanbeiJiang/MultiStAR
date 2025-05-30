import os
from tqdm import tqdm
import random
import json
from collections import defaultdict
import numpy as np
from pathlib import Path
import argparse

root_path = './dataset'
output_dir = 'logical_chain_questions.json'

parser = argparse.ArgumentParser()

parser.add_argument('--question_num', default=10, type=int,
                    help="The number of different templates that should be instantiated " +
                         "on each image")
args = parser.parse_args()

def sample_dataset():
    dataset_path = Path("dataset")
    samples_per_config = args.question_num
    total_data_points = count_subfolders_os("./dataset/center_single")
    
    # Get all configuration directories
    configurations = [d for d in dataset_path.iterdir() if d.is_dir()]
    sampled_paths = []
    
    for config in configurations:
        # Generate list of available data numbers (assuming 0-999 or 1-1000)
        available_data_nums = []
        for i in range(total_data_points):  # Check both 0-based and 1-based numbering
            question_path = config / str(i) / "question.json"
            if question_path.exists():
                available_data_nums.append(i)
        
        sample_size = samples_per_config
        
        # Randomly sample data numbers
        sampled_nums = random.sample(available_data_nums, sample_size)
        
        # Create file paths
        for data_num in sampled_nums:
            file_path = f"./dataset/{config.name}/{data_num}/question.json"
            sampled_paths.append(file_path)

    return sampled_paths

def count_subfolders_os(folder_path):
    if not os.path.exists(folder_path):
        return 0
    
    count = 0
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            count += 1
    return count

# Function to load JSON files and collect all questions
def load_questions_from_json(file_paths):
    final_output = []
    for file_path in file_paths:
        output = {}
        output["file_path"] = file_path
        output["questions"] = []
        with open(file_path, 'r') as f:
            data = json.load(f)
            if data["questions"][0]["config"] == "center_single" or data["questions"][0]["config"] == "distribute_four" or data["questions"][0]["config"] == "distribute_nine":
                for attribute in ["number", "position", "shape", "color", "size"]:
                    for i in range(3):
                        stage = "single_panel"
                        question, choices, correct_answer, config, image_path = generate_question_answer(data, i, stage, attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config, "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)
                    for i in range(2):
                        stage = "two_panels"
                        question, choices, correct_answer, config, image_path = generate_question_answer(data, i, stage, attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config, "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                    stage = "one_row"
                    question, choices, correct_answer, config, image_path = generate_question_answer(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config, "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "two_rows"
                    question, choices, correct_answer, config, image_path = generate_question_answer(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config, "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)
            elif data["questions"][0]["config"] == "left_center_single_right_center_single":
                for attribute in ["number", "position", "shape", "color", "size"]:
                    for i in range(3):
                        stage = "single_panel_left"
                        question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                        stage = "single_panel_right"
                        question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                    for i in range(2):
                        stage = "two_panels_left"
                        question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                        stage = "two_panels_right"
                        question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                    stage = "one_row_left"
                    question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "one_row_right"
                    question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "two_rows_left"
                    question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "two_rows_right"
                    question, choices, correct_answer, config, image_path = generate_question_answer_LR(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)
            elif data["questions"][0]["config"] == "up_center_single_down_center_single":
                for attribute in ["number", "position", "shape", "color", "size"]:
                    for i in range(3):
                        stage = "single_panel_top"
                        question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                        stage = "single_panel_bottom"
                        question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                    for i in range(2):
                        stage = "two_panels_top"
                        question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                        stage = "two_panels_bottom"
                        question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                    stage = "one_row_top"
                    question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "one_row_bottom"
                    question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "two_rows_top"
                    question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "two_rows_bottom"
                    question, choices, correct_answer, config, image_path = generate_question_answer_TD(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)
            elif data["questions"][0]["config"] == "in_center_single_out_center_single" or data["questions"][0]["config"] == "in_distribute_four_out_center_single":
                for attribute in ["number", "position", "shape", "color", "size"]:
                    for i in range(3):
                        stage = "single_panel_in"
                        question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                        stage = "single_panel_out"
                        question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                    for i in range(2):
                        stage = "two_panels_in"
                        question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                        stage = "two_panels_out"
                        question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                         attribute)
                        question_answer_pair = {"question": question, "choices": choices,
                                                "correct_answer": correct_answer, "config": config,
                                                "image_path": image_path, "stage": stage, "attribute": attribute}
                        output["questions"].append(question_answer_pair)

                    stage = "one_row_in"
                    question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "one_row_out"
                    question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "two_rows_in"
                    question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)

                    stage = "two_rows_out"
                    question, choices, correct_answer, config, image_path = generate_question_answer_in_out(data, i, stage,
                                                                                                     attribute)
                    question_answer_pair = {"question": question, "choices": choices,
                                            "correct_answer": correct_answer, "config": config,
                                            "image_path": image_path,
                                            "stage": stage, "attribute": attribute}
                    output["questions"].append(question_answer_pair)
            output["original_filename"] = data["questions"][0]["filename"]
        final_output.append(output)
    return final_output


def generate_question_answer(data, panel_index, stage, attribute):
    question, all_choices, correct_answer, config, new_path = None, None, None, None, None
    if attribute == "number":
        if stage == "single_panel":
            # Get the number of objects in the specified panel
            correct_answer = len(data["panels"][panel_index])

            # Sample three random choices from 1 to 9 excluding the correct answer
            choices = set()
            while len(choices) < 3:
                choice = random.randint(1, 9)
                if choice != correct_answer:
                    choices.add(choice)

            # Combine the correct answer with the other choices and shuffle them
            all_choices = list(choices) + [correct_answer]
            random.shuffle(all_choices)

            # Generate the question
            question = f"How many objects are in the panel?"

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_{panel_index+1}.png"
            new_path = os.path.join(directory, new_filename)
            # Return the question and the list of answer choices
        elif stage == "two_panels":
            # Get the number of objects in the specified panel
            if len(data["panels"][panel_index]) == len(data["panels"][panel_index+1]):
                correct_answer = "The same"
            elif len(data["panels"][panel_index]) < len(data["panels"][panel_index+1]):
                correct_answer = "Fewer"
            else:
                correct_answer = "More"

            # Combine the correct answer with the other choices and shuffle them
            all_choices = ["The same", "More", "Fewer"]
            random.shuffle(all_choices)

            # Generate the question
            question = f"Does the left panel contain the same number of objects, more objects, or fewer objects than the right panel?"

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_combination_{panel_index+1}_{panel_index+2}.png"
            new_path = os.path.join(directory, new_filename)
        elif stage == "one_row":
            for question in data["questions"]:
                if "reasoning_first" in question["template_filename"]:
                    for choice in question["choices"]:
                        if "The number of objects" in choice:
                            return (question["question"], question["choices"], question["answer"], question["config"],
                                    os.path.join(root_path, question["config"], question["image_filename"]))
        elif stage == "two_rows":
            for question in data["questions"]:
                if "reasoning_second" in question["template_filename"]:
                    for choice in question["choices"]:
                        if "The number of objects" in choice:
                            return (question["question"], question["choices"], question["answer"], question["config"],
                                    os.path.join(root_path, question["config"], question["image_filename"]))
    elif attribute == "position":
        if stage == "single_panel":
            # Get the number of objects in the specified panel
            selected_object = random.choice(data["panels"][panel_index])
            correct_answer = selected_object['position']

            all_choices = sample_positions(correct_answer, data["questions"][0]["config"])

            random.shuffle(all_choices)

            # Generate the question
            question = f"Where is the {selected_object['shape']} positioned in the panel?"

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_{panel_index+1}.png"
            new_path = os.path.join(directory, new_filename)
            # Return the question and the list of answer choices
        elif stage == "two_panels":
            # Extract positions from each object in both panels
            left_panel = data['panels'][panel_index]
            right_panel = data['panels'][panel_index + 1]
            left_positions = [obj['position'] for obj in left_panel]
            right_positions = [obj['position'] for obj in right_panel]

            # Check if both panels have the same number of objects and their positions match
            if len(left_positions) == len(right_positions) and sorted(left_positions) == sorted(right_positions):
                correct_answer = "Yes"
            else:
                correct_answer = "No"
            # Combine the correct answer with the other choices and shuffle them
            all_choices = ["Yes", "No"]
            random.shuffle(all_choices)

            # Generate the question
            question = f"Is the position of all the objects in the left panel the same as the objects in the right panel?"

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_combination_{panel_index+1}_{panel_index+2}.png"
            new_path = os.path.join(directory, new_filename)
        elif stage == "one_row":
            for question in data["questions"]:
                if "reasoning_first" in question["template_filename"] and "the position of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
        elif stage == "two_rows":
            for question in data["questions"]:
                if "reasoning_second" in question["template_filename"] and "the position of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
    elif attribute == "shape":
        if stage == "single_panel":
            # Get the number of objects in the specified panel
            selected_object = random.choice(data["panels"][panel_index])
            correct_answer = selected_object['shape']
            position = selected_object["position"]
            shapes = ["triangle", "square", "pentagon", "hexagon", "circle"]
            shapes.remove(correct_answer)

            # Randomly sample 3 incorrect answers from the remaining shapes
            incorrect_answers = random.sample(shapes, 3)
            all_choices = incorrect_answers + [correct_answer]
            random.shuffle(all_choices)

            # Generate the question
            question = f"What is the shape of the object at {position} in the panel?"

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_{panel_index+1}.png"
            new_path = os.path.join(directory, new_filename)
            # Return the question and the list of answer choices
        elif stage == "two_panels":
            # Extract positions from each object in both panels
            left_panel = data['panels'][panel_index]
            right_panel = data['panels'][panel_index + 1]

            def check_shape_consistency(panel):
                # Extract the sizes of all objects in the panel
                shapes = [obj['shape'] for obj in panel]

                # Check if all sizes in the panel are the same
                if all(shape == shapes[0] for shape in shapes):
                    return shapes[0]  # Return the consistent size
                else:
                    return None  # Return None if sizes are inconsistent

            shape_to_num = {"triangle": 1, "square": 2, "pentagon": 3, "hexagon": 4, "circle": 5}
            left_shape = check_shape_consistency(left_panel)
            right_shape = check_shape_consistency(right_panel)
            if left_shape is None or right_shape is None:
                correct_answer = "Not Comparable"
            elif left_shape == right_shape:
                correct_answer = "Same"
            elif shape_to_num[left_shape] < shape_to_num[right_shape]:
                correct_answer = "Fewer"
            else:
                correct_answer = "More"

            # Combine the correct answer with the other choices and shuffle them
            all_choices = ["The same", "Fewer", "More", "Not comparable"]
            random.shuffle(all_choices)

            # Generate the question
            question = (f"Is the shape of all the objects in the left panel have the same, more, or fewer edges "
                        f"compared to the objects in the right panel? "
                        f"If the shapes within either panel are already different from each other, select 'Not Comparable.' "
                        f"(Note: The edge number increases in the following order: triangle, square, pentagon, hexagon, circle)")

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
            new_path = os.path.join(directory, new_filename)
        elif stage == "one_row":
            for question in data["questions"]:
                if "reasoning_first" in question["template_filename"] and "the shape of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
        elif stage == "two_rows":
            for question in data["questions"]:
                if "reasoning_second" in question["template_filename"] and "the shape of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
    elif attribute == "size":
        if stage == "single_panel":
            sizes = [obj['size'] for obj in data['panels'][panel_index]]
            if len(sizes) == 1:
                correct_answer =  "Only one object"
            elif all(size == sizes[0] for size in sizes):
                correct_answer = "Yes"
            else:
                correct_answer = "No"

            # Combine the correct answer with the other choices and shuffle them
            all_choices = ["Yes", "No", "Only one object"]
            random.shuffle(all_choices)

            # Generate the question
            question = f"Are all objects in the panel of the same size?"

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_{panel_index+1}.png"
            new_path = os.path.join(directory, new_filename)
            # Return the question and the list of answer choices
        elif stage == "two_panels":
            # Extract positions from each object in both panels
            left_panel = data['panels'][panel_index]
            right_panel = data['panels'][panel_index + 1]

            def check_size_consistency(panel):
                # Extract the sizes of all objects in the panel
                sizes = [obj['size'] for obj in panel]

                # Check if all sizes in the panel are the same
                if all(size == sizes[0] for size in sizes):
                    return sizes[0]  # Return the consistent size
                else:
                    return None  # Return None if sizes are inconsistent

            left_size = check_size_consistency(left_panel)
            right_size = check_size_consistency(right_panel)
            if left_size is None or right_size is None:
                correct_answer = "Not Comparable"
            elif left_size == right_size:
                correct_answer = "Same"
            elif left_size < right_size:
                correct_answer = "Smaller"
            else:
                correct_answer = "Larger"

            # Combine the correct answer with the other choices and shuffle them
            all_choices = ["The same", "Smaller", "Larger", "Not comparable"]
            random.shuffle(all_choices)

            # Generate the question
            question = (f"Is the size of all the objects in the left panel the same as, smaller "
                        f"or larger than the objects in the right panel? "
                        f"If the sizes within either panel are already different from each other, select 'Not Comparable.")

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
            new_path = os.path.join(directory, new_filename)
        elif stage == "one_row":
            for question in data["questions"]:
                if "reasoning_first" in question["template_filename"] and "the size of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
        elif stage == "two_rows":
            for question in data["questions"]:
                if "reasoning_second" in question["template_filename"] and "the size of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
    elif attribute == "color":
        if stage == "single_panel":
            colors = [obj['color'] for obj in data['panels'][panel_index]]
            if len(colors) == 1:
                correct_answer =  "Only one object"
            elif all(color == colors[0] for color in colors):
                correct_answer = "Yes"
            else:
                correct_answer = "No"

            # Combine the correct answer with the other choices and shuffle them
            all_choices = ["Yes", "No", "Only one object"]
            random.shuffle(all_choices)

            # Generate the question
            question = f"Are all objects in the panel of the same color?"

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_{panel_index+1}.png"
            new_path = os.path.join(directory, new_filename)
            # Return the question and the list of answer choices
        elif stage == "two_panels":
            # Extract positions from each object in both panels
            left_panel = data['panels'][panel_index]
            right_panel = data['panels'][panel_index + 1]

            def check_color_consistency(panel):
                # Extract the sizes of all objects in the panel
                colors = [obj['color'] for obj in panel]

                # Check if all sizes in the panel are the same
                if all(color == colors[0] for color in colors):
                    return colors[0]  # Return the consistent size
                else:
                    return None  # Return None if sizes are inconsistent

            left_color = check_color_consistency(left_panel)
            right_color = check_color_consistency(right_panel)
            if left_color is None or right_color is None:
                correct_answer = "Not Comparable"
            elif left_color == right_color:
                correct_answer = "Same"
            elif left_color < right_color:
                correct_answer = "Darker"
            else:
                correct_answer = "Brighter"

            # Combine the correct answer with the other choices and shuffle them
            all_choices = ["The same", "Darker", "Brighter", "Not comparable"]
            random.shuffle(all_choices)

            # Generate the question
            question = (f"Is the color of all the objects in the left panel the same as, "
                        f"darker or brighter than the objects in the right panel? "
                        f"If the colors within either panel are already different from each other, select 'Not Comparable.'")

            config = data["questions"][0]["config"]
            image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
            directory = os.path.dirname(image_path)
            new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
            new_path = os.path.join(directory, new_filename)
        elif stage == "one_row":
            for question in data["questions"]:
                if "reasoning_first" in question["template_filename"] and "the color of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
        elif stage == "two_rows":
            for question in data["questions"]:
                if "reasoning_second" in question["template_filename"] and "the color of" in question["question"]:
                    return (question["question"], question["choices"], question["answer"], question["config"],
                            os.path.join(root_path, question["config"], question["image_filename"]))
    assert (question is not None and all_choices is not None and correct_answer is not None and config is not None and new_path is not None)
    return question, all_choices, correct_answer, config, new_path


def generate_question_answer_LR(data, panel_index, stage, attribute):
    question, all_choices, correct_answer, config, new_path = None, None, None, None, None
    if "left" in stage:
        stage = "_".join(stage.split("_")[:-1])
        if attribute == "number":
            if "single_panel" in stage:
                # Get the number of objects in the specified panel
                correct_answer = 1

                # Sample three random choices from 1 to 9 excluding the correct answer
                choices = set()
                while len(choices) < 3:
                    choice = random.randint(1, 9)
                    if choice != correct_answer:
                        choices.add(choice)

                # Combine the correct answer with the other choices and shuffle them
                all_choices = list(choices) + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"How many objects are in the left part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index+1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif "two_panels" in stage:

                correct_answer = "The same"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "More", "Fewer"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the left part of the two panels in the image. "
                            f"Does the left panel contain the same number of objects, more objects, or fewer objects than the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index+1}_{panel_index+2}.png"
                new_path = os.path.join(directory, new_filename)
            elif "one_row" in stage:
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the left" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (question["question"], question["choices"], question["answer"], question["config"],
                                        os.path.join(root_path, question["config"], question["image_filename"]))
            elif "two_rows" in stage:
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the left" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (question["question"], question["choices"], question["answer"], question["config"],
                                        os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "position":
            if "single_panel" in stage:
                # Get the number of objects in the specified panel
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "left":
                        selected_object = object
                        break
                correct_answer = selected_object['position']

                all_choices = sample_positions(correct_answer, data["questions"][0]["config"])

                random.shuffle(all_choices)

                # Generate the question
                question = f"Where is the {selected_object['shape']} positioned in the left part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index+1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif "two_panels" in stage:

                correct_answer = "Yes"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the left part of the two panels in the image. "
                            f"Is the position of all the objects in the left panel the same as the objects in the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index+1}_{panel_index+2}.png"
                new_path = os.path.join(directory, new_filename)
            elif "one_row" in stage:
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the position of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif "two_rows" in stage:
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the position of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "shape":
            if "single_panel" in stage:
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "left":
                        selected_object = object
                        break
                correct_answer = selected_object['shape']
                shapes = ["triangle", "square", "pentagon", "hexagon", "circle"]
                shapes.remove(correct_answer)

                # Randomly sample 3 incorrect answers from the remaining shapes
                incorrect_answers = random.sample(shapes, 3)
                all_choices = incorrect_answers + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"What is the shape of the object in the left part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index+1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif "two_panels" in stage:
                shape_to_num = {"triangle": 1, "square": 2, "pentagon": 3, "hexagon": 4, "circle": 5}
                left_shape = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "left":
                        left_shape = object['shape']
                        break
                right_shape = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "left":
                        right_shape = object['shape']
                        break
                assert (left_shape is not None and right_shape is not None)
                if left_shape == right_shape:
                    correct_answer = "Same"
                elif shape_to_num[left_shape] < shape_to_num[right_shape]:
                    correct_answer = "Fewer"
                else:
                    correct_answer = "More"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Fewer", "More", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the left part of the two panels in the image. "
                            f"Is the shape of all the objects in the left panel have the same, more, or fewer edges "
                            f"compared to the objects in the right panel? "
                            f"If the shapes within either panel are already different from each other, select 'Not Comparable.' "
                            f"(Note: The edge number increases in the following order: triangle, square, pentagon, hexagon, circle)")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif "one_row" in stage:
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the shape of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif "two_rows" in stage:
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the shape of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "size":
            if "single_panel" in stage:
                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the left part of the panel of the same size?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index+1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif "two_panels" in stage:

                left_size = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "left":
                        left_size = object['size']
                        break
                right_size = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "left":
                        right_size = object['size']
                        break
                assert (left_size is not None and right_size is not None)

                if left_size == right_size:
                    correct_answer = "Same"
                elif left_size < right_size:
                    correct_answer = "Smaller"
                else:
                    correct_answer = "Larger"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Smaller", "Larger", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the left part of the two panels in the image. "
                            f"Is the size of all the objects in the left panel the same as, smaller "
                            f"or larger than the objects in the right panel? "
                            f"If the sizes within either panel are already different from each other, select 'Not Comparable.")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif "one_row" in stage:
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the size of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif "two_rows" in stage:
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the size of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "color":
            if "single_panel" in stage:
                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the left part of the panel of the same color?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index+1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif "two_panels" in stage:
                left_color = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "left":
                        left_color = object['color']
                        break
                right_color = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "left":
                        right_color = object['color']
                        break
                assert (left_color is not None and right_color is not None)

                if left_color == right_color:
                    correct_answer = "Same"
                elif left_color < right_color:
                    correct_answer = "Darker"
                else:
                    correct_answer = "Brighter"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Darker", "Brighter", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the left part of the two panels in the image. "
                            f"Is the color of all the objects in the left panel the same as, "
                            f"darker or brighter than the objects in the right panel? "
                            f"If the colors within either panel are already different from each other, select 'Not Comparable.'")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif "one_row" in stage:
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the color of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif "two_rows" in stage:
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the color of" in question["question"] and "the left" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
    else:
        stage = "_".join(stage.split("_")[:-1])
        if attribute == "number":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                correct_answer = 1

                # Sample three random choices from 1 to 9 excluding the correct answer
                choices = set()
                while len(choices) < 3:
                    choice = random.randint(1, 9)
                    if choice != correct_answer:
                        choices.add(choice)

                # Combine the correct answer with the other choices and shuffle them
                all_choices = list(choices) + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"How many objects are in the right part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "The same"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "More", "Fewer"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the right part of the two panels in the image. "
                            f"Does the left panel contain the same number of objects, more objects, or fewer objects than the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the right" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the right" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "position":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "right":
                        selected_object = object
                        break
                correct_answer = selected_object['position']

                all_choices = sample_positions(correct_answer, data["questions"][0]["config"])

                random.shuffle(all_choices)

                # Generate the question
                question = f"Where is the {selected_object['shape']} positioned in the right part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "Yes"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the right part of the two panels in the image. "
                            f"Is the position of all the objects in the left panel the same as the objects in the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the position of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the position of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "shape":
            if stage == "single_panel":
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "right":
                        selected_object = object
                        break
                correct_answer = selected_object['shape']
                shapes = ["triangle", "square", "pentagon", "hexagon", "circle"]
                shapes.remove(correct_answer)

                # Randomly sample 3 incorrect answers from the remaining shapes
                incorrect_answers = random.sample(shapes, 3)
                all_choices = incorrect_answers + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"What is the shape of the object in the right part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                shape_to_num = {"triangle": 1, "square": 2, "pentagon": 3, "hexagon": 4, "circle": 5}
                left_shape = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "right":
                        left_shape = object['shape']
                        break
                right_shape = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "right":
                        right_shape = object['shape']
                        break
                assert (left_shape is not None and right_shape is not None)
                if left_shape == right_shape:
                    correct_answer = "Same"
                elif shape_to_num[left_shape] < shape_to_num[right_shape]:
                    correct_answer = "Fewer"
                else:
                    correct_answer = "More"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Fewer", "More", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the right part of the two panels in the image. "
                            f"Is the shape of all the objects in the left panel have the same, more, or fewer edges "
                            f"compared to the objects in the right panel? "
                            f"If the shapes within either panel are already different from each other, select 'Not Comparable.' "
                            f"(Note: The edge number increases in the following order: triangle, square, pentagon, hexagon, circle)")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "size":
            if stage == "single_panel":

                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the right part of the panel of the same size?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                left_size = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "right":
                        left_size = object['size']
                        break
                right_size = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "right":
                        right_size = object['size']
                        break
                assert (left_size is not None and right_size is not None)

                if left_size == right_size:
                    correct_answer = "Same"
                elif left_size < right_size:
                    correct_answer = "Smaller"
                else:
                    correct_answer = "Larger"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Smaller", "Larger", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the right part of the two panels in the image. "
                            f"Is the size of all the objects in the left panel the same as, smaller "
                            f"or larger than the objects in the right panel? "
                            f"If the sizes within either panel are already different from each other, select 'Not Comparable.")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the size of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the size of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "color":
            if stage == "single_panel":
                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the right part of the panel of the same color?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":
                left_color = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "right":
                        left_color = object['color']
                        break
                right_color = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "right":
                        right_color = object['color']
                        break
                assert (left_color is not None and right_color is not None)

                if left_color == right_color:
                    correct_answer = "Same"
                elif left_color < right_color:
                    correct_answer = "Darker"
                else:
                    correct_answer = "Brighter"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Darker", "Brighter", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the right part of the two panels in the image. "
                            f"Is the color of all the objects in the left panel the same as, "
                            f"darker or brighter than the objects in the right panel? "
                            f"If the colors within either panel are already different from each other, select 'Not Comparable.'")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the color of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the color of" in question[
                        "question"] and "the right" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
    assert (question is not None and all_choices is not None and correct_answer is not None and config is not None and new_path is not None)
    return question, all_choices, correct_answer, config, new_path


def generate_question_answer_TD(data, panel_index, stage, attribute):
    question, all_choices, correct_answer, config, new_path = None, None, None, None, None
    if "top" in stage:
        stage = "_".join(stage.split("_")[:-1])
        if attribute == "number":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                correct_answer = 1

                # Sample three random choices from 1 to 9 excluding the correct answer
                choices = set()
                while len(choices) < 3:
                    choice = random.randint(1, 9)
                    if choice != correct_answer:
                        choices.add(choice)

                # Combine the correct answer with the other choices and shuffle them
                all_choices = list(choices) + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"How many objects are in the top part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "The same"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "More", "Fewer"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the top part of the two panels in the image. "
                            f"Does the left panel contain the same number of objects, more objects, or fewer objects than the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the top" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the top" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "position":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "top":
                        selected_object = object
                        break
                correct_answer = selected_object['position']

                all_choices = sample_positions(correct_answer, data["questions"][0]["config"])

                random.shuffle(all_choices)

                # Generate the question
                question = f"Where is the {selected_object['shape']} positioned in the top part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "Yes"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the top part of the two panels in the image. "
                            f"Is the position of all the objects in the left panel the same as the objects in the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the position of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the position of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "shape":
            if stage == "single_panel":
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "top":
                        selected_object = object
                        break
                correct_answer = selected_object['shape']
                shapes = ["triangle", "square", "pentagon", "hexagon", "circle"]
                shapes.remove(correct_answer)

                # Randomly sample 3 incorrect answers from the remaining shapes
                incorrect_answers = random.sample(shapes, 3)
                all_choices = incorrect_answers + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"What is the shape of the object in the top part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                shape_to_num = {"triangle": 1, "square": 2, "pentagon": 3, "hexagon": 4, "circle": 5}
                left_shape = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "top":
                        left_shape = object['shape']
                        break
                right_shape = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "top":
                        right_shape = object['shape']
                        break
                assert (left_shape is not None and right_shape is not None)
                if left_shape == right_shape:
                    correct_answer = "Same"
                elif shape_to_num[left_shape] < shape_to_num[right_shape]:
                    correct_answer = "Fewer"
                else:
                    correct_answer = "More"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Fewer", "More", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the top part of the two panels in the image. "
                            f"Is the shape of all the objects in the left panel have the same, more, or fewer edges "
                            f"compared to the objects in the right panel? "
                            f"If the shapes within either panel are already different from each other, select 'Not Comparable.' "
                            f"(Note: The edge number increases in the following order: triangle, square, pentagon, hexagon, circle)")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "size":
            if stage == "single_panel":

                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the top part of the panel of the same size?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                left_size = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "top":
                        left_size = object['size']
                        break
                right_size = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "top":
                        right_size = object['size']
                        break
                assert (left_size is not None and right_size is not None)

                if left_size == right_size:
                    correct_answer = "Same"
                elif left_size < right_size:
                    correct_answer = "Smaller"
                else:
                    correct_answer = "Larger"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Smaller", "Larger", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the top part of the two panels in the image. "
                            f"Is the size of all the objects in the left panel the same as, smaller "
                            f"or larger than the objects in the right panel? "
                            f"If the sizes within either panel are already different from each other, select 'Not Comparable.")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the size of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the size of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "color":
            if stage == "single_panel":
                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the top part of the panel of the same color?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":
                left_color = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "top":
                        left_color = object['color']
                        break
                right_color = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "top":
                        right_color = object['color']
                        break
                assert (left_color is not None and right_color is not None)

                if left_color == right_color:
                    correct_answer = "Same"
                elif left_color < right_color:
                    correct_answer = "Darker"
                else:
                    correct_answer = "Brighter"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Darker", "Brighter", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the top part of the two panels in the image. "
                            f"Is the color of all the objects in the left panel the same as, "
                            f"darker or brighter than the objects in the right panel? "
                            f"If the colors within either panel are already different from each other, select 'Not Comparable.'")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the color of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the color of" in question[
                        "question"] and "the top" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
    else:
        stage = "_".join(stage.split("_")[:-1])
        if attribute == "number":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                correct_answer = 1

                # Sample three random choices from 1 to 9 excluding the correct answer
                choices = set()
                while len(choices) < 3:
                    choice = random.randint(1, 9)
                    if choice != correct_answer:
                        choices.add(choice)

                # Combine the correct answer with the other choices and shuffle them
                all_choices = list(choices) + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"How many objects are in the bottom part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "The same"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "More", "Fewer"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the bottom part of the two panels in the image. "
                            f"Does the left panel contain the same number of objects, more objects, or fewer objects than the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the bottom" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                    question["question"], question["choices"], question["answer"], question["config"],
                                    os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the bottom" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                    question["question"], question["choices"], question["answer"], question["config"],
                                    os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "position":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "bottom":
                        selected_object = object
                        break
                correct_answer = selected_object['position']

                all_choices = sample_positions(correct_answer, data["questions"][0]["config"])

                random.shuffle(all_choices)

                # Generate the question
                question = f"Where is the {selected_object['shape']} positioned in the bottom part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "Yes"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the bottom part of the two panels in the image. "
                            f"Is the position of all the objects in the left panel the same as the objects in the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the position of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the position of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "shape":
            if stage == "single_panel":
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "bottom":
                        selected_object = object
                        break
                correct_answer = selected_object['shape']
                shapes = ["triangle", "square", "pentagon", "hexagon", "circle"]
                shapes.remove(correct_answer)

                # Randomly sample 3 incorrect answers from the remaining shapes
                incorrect_answers = random.sample(shapes, 3)
                all_choices = incorrect_answers + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"What is the shape of the object in the bottom part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                shape_to_num = {"triangle": 1, "square": 2, "pentagon": 3, "hexagon": 4, "circle": 5}
                left_shape = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "bottom":
                        left_shape = object['shape']
                        break
                right_shape = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "bottom":
                        right_shape = object['shape']
                        break
                assert (left_shape is not None and right_shape is not None)
                if left_shape == right_shape:
                    correct_answer = "Same"
                elif shape_to_num[left_shape] < shape_to_num[right_shape]:
                    correct_answer = "Fewer"
                else:
                    correct_answer = "More"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Fewer", "More", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the bottom part of the two panels in the image. "
                            f"Is the shape of all the objects in the left panel have the same, more, or fewer edges "
                            f"compared to the objects in the right panel? "
                            f"If the shapes within either panel are already different from each other, select 'Not Comparable.' "
                            f"(Note: The edge number increases in the following order: triangle, square, pentagon, hexagon, circle)")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "size":
            if stage == "single_panel":

                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the bottom part of the panel of the same size?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                left_size = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "bottom":
                        left_size = object['size']
                        break
                right_size = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "bottom":
                        right_size = object['size']
                        break
                assert (left_size is not None and right_size is not None)

                if left_size == right_size:
                    correct_answer = "Same"
                elif left_size < right_size:
                    correct_answer = "Smaller"
                else:
                    correct_answer = "Larger"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Smaller", "Larger", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the bottom part of the two panels in the image. "
                            f"Is the size of all the objects in the left panel the same as, smaller "
                            f"or larger than the objects in the right panel? "
                            f"If the sizes within either panel are already different from each other, select 'Not Comparable.")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the size of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the size of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "color":
            if stage == "single_panel":
                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the bottom part of the panel of the same color?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":
                left_color = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "bottom":
                        left_color = object['color']
                        break
                right_color = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "bottom":
                        right_color = object['color']
                        break
                assert (left_color is not None and right_color is not None)

                if left_color == right_color:
                    correct_answer = "Same"
                elif left_color < right_color:
                    correct_answer = "Darker"
                else:
                    correct_answer = "Brighter"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Darker", "Brighter", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the bottom part of the two panels in the image. "
                            f"Is the color of all the objects in the left panel the same as, "
                            f"darker or brighter than the objects in the right panel? "
                            f"If the colors within either panel are already different from each other, select 'Not Comparable.'")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the color of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the color of" in question[
                        "question"] and "the bottom" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
    assert (question is not None and all_choices is not None and correct_answer is not None and config is not None and new_path is not None)
    return question, all_choices, correct_answer, config, new_path


def generate_question_answer_in_out(data, panel_index, stage, attribute):
    question, all_choices, correct_answer, config, new_path = None, None, None, None, None
    if "out" in stage:
        stage = "_".join(stage.split("_")[:-1])
        if attribute == "number":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                correct_answer = 1

                # Sample three random choices from 1 to 9 excluding the correct answer
                choices = set()
                while len(choices) < 3:
                    choice = random.randint(1, 9)
                    if choice != correct_answer:
                        choices.add(choice)

                # Combine the correct answer with the other choices and shuffle them
                all_choices = list(choices) + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"How many objects are in the outer part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "The same"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "More", "Fewer"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the outer part of the two panels in the image. "
                            f"Does the left panel contain the same number of objects, more objects, or fewer objects than the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the outer" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the outer" in question["question"]:
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "position":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "outer-part":
                        selected_object = object
                        break
                correct_answer = selected_object['position']

                all_choices = sample_positions(correct_answer, data["questions"][0]["config"])

                random.shuffle(all_choices)

                # Generate the question
                question = f"Where is the {selected_object['shape']} positioned in the outer part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                correct_answer = "Yes"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the outer part of the two panels in the image. "
                            f"Is the position of all the objects in the left panel the same as the objects in the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the position of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the position of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "shape":
            if stage == "single_panel":
                selected_object = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "outer-part":
                        selected_object = object
                        break
                correct_answer = selected_object['shape']
                shapes = ["triangle", "square", "pentagon", "hexagon", "circle"]
                shapes.remove(correct_answer)

                # Randomly sample 3 incorrect answers from the remaining shapes
                incorrect_answers = random.sample(shapes, 3)
                all_choices = incorrect_answers + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"What is the shape of the object in the outer part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                shape_to_num = {"triangle": 1, "square": 2, "pentagon": 3, "hexagon": 4, "circle": 5}
                left_shape = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "outer-part":
                        left_shape = object['shape']
                        break
                right_shape = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "outer-part":
                        right_shape = object['shape']
                        break
                assert (left_shape is not None and right_shape is not None)
                if left_shape == right_shape:
                    correct_answer = "Same"
                elif shape_to_num[left_shape] < shape_to_num[right_shape]:
                    correct_answer = "Fewer"
                else:
                    correct_answer = "More"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Fewer", "More", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the outer part of the two panels in the image. "
                            f"Is the shape of all the objects in the left panel have the same, more, or fewer edges "
                            f"compared to the objects in the right panel? "
                            f"If the shapes within either panel are already different from each other, select 'Not Comparable.' "
                            f"(Note: The edge number increases in the following order: triangle, square, pentagon, hexagon, circle)")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the shape of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "size":
            if stage == "single_panel":

                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the outer part of the panel of the same size?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                left_size = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "outer-part":
                        left_size = object['size']
                        break
                right_size = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "outer-part":
                        right_size = object['size']
                        break
                assert (left_size is not None and right_size is not None)

                if left_size == right_size:
                    correct_answer = "Same"
                elif left_size < right_size:
                    correct_answer = "Smaller"
                else:
                    correct_answer = "Larger"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Smaller", "Larger", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the outer part of the two panels in the image. "
                            f"Is the size of all the objects in the left panel the same as, smaller "
                            f"or larger than the objects in the right panel? "
                            f"If the sizes within either panel are already different from each other, select 'Not Comparable.")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the size of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the size of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "color":
            if stage == "single_panel":
                correct_answer = "Only one object"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the outer part of the panel of the same color?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":
                left_color = None
                for object in data["panels"][panel_index]:
                    if object["position"] == "outer-part":
                        left_color = object['color']
                        break
                right_color = None
                for object in data["panels"][panel_index + 1]:
                    if object["position"] == "outer-part":
                        right_color = object['color']
                        break
                assert (left_color is not None and right_color is not None)

                if left_color == right_color:
                    correct_answer = "Same"
                elif left_color < right_color:
                    correct_answer = "Darker"
                else:
                    correct_answer = "Brighter"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Darker", "Brighter", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the outer part of the two panels in the image. "
                            f"Is the color of all the objects in the left panel the same as, "
                            f"darker or brighter than the objects in the right panel? "
                            f"If the colors within either panel are already different from each other, select 'Not Comparable.'")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the color of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the color of" in question[
                        "question"] and "the outer" in question["question"]:
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
    else:
        stage = "_".join(stage.split("_")[:-1])
        if attribute == "number":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                correct_answer = 0
                for object in data["panels"][panel_index]:
                    if "inner" in object["position"]:
                        correct_answer += 1

                # Sample three random choices from 1 to 9 excluding the correct answer
                choices = set()
                while len(choices) < 3:
                    choice = random.randint(1, 9)
                    if choice != correct_answer:
                        choices.add(choice)

                # Combine the correct answer with the other choices and shuffle them
                all_choices = list(choices) + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"How many objects are in the inner part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":
                left_num = 0
                for object in data["panels"][panel_index]:
                    if "inner" in object["position"]:
                        left_num += 1
                right_num = 0
                for object in data["panels"][panel_index + 1]:
                    if "inner" in object["position"]:
                        right_num += 1
                if left_num == right_num:
                    correct_answer = "The same"
                elif left_num < right_num:
                    correct_answer = "Fewer"
                else:
                    correct_answer = "More"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "More", "Fewer"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the inner part of the two panels in the image. "
                            f"Does the left panel contain the same number of objects, more objects, or fewer objects than the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and ("inner" in question["question"] or "interior" in question["question"]):
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                    question["question"], question["choices"], question["answer"], question["config"],
                                    os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and ("inner" in question["question"] or "interior" in question["question"]):
                        for choice in question["choices"]:
                            if "The number of objects" in choice:
                                return (
                                    question["question"], question["choices"], question["answer"], question["config"],
                                    os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "position":
            if stage == "single_panel":
                # Get the number of objects in the specified panel
                selected_objects = []
                for object in data["panels"][panel_index]:
                    if "inner" in object["position"]:
                        selected_objects.append(object)
                selected_object = random.choice(selected_objects)


                correct_answer = selected_object['position']

                all_choices = sample_positions(correct_answer, data["questions"][0]["config"])

                random.shuffle(all_choices)

                # Generate the question
                question = f"Where is the {selected_object['shape']} positioned in the inner part of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                left_panel = data['panels'][panel_index]
                right_panel = data['panels'][panel_index + 1]
                left_positions = [obj['position'] for obj in left_panel]
                right_positions = [obj['position'] for obj in right_panel]

                # Check if both panels have the same number of objects and their positions match
                if len(left_positions) == len(right_positions) and sorted(left_positions) == sorted(right_positions):
                    correct_answer = "Yes"
                else:
                    correct_answer = "No"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the inner part of the two panels in the image. "
                            f"Is the position of all the objects in the left panel the same as the objects in the right panel?")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the position of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the position of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "shape":
            if stage == "single_panel":
                selected_objects = []
                for object in data["panels"][panel_index]:
                    if "inner" in object["position"]:
                        selected_objects.append(object)
                selected_object = random.choice(selected_objects)
                position = selected_object["position"]
                correct_answer = selected_object['shape']

                shapes = ["triangle", "square", "pentagon", "hexagon", "circle"]
                shapes.remove(correct_answer)

                # Randomly sample 3 incorrect answers from the remaining shapes
                incorrect_answers = random.sample(shapes, 3)
                all_choices = incorrect_answers + [correct_answer]
                random.shuffle(all_choices)

                # Generate the question
                question = f"What is the shape of the object in the {position} of the panel?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                left_panel = [obj for obj in data['panels'][panel_index] if "inner" in obj["position"]]
                right_panel = [obj for obj in data['panels'][panel_index + 1] if "inner" in obj["position"]]

                def check_shape_consistency(panel):
                    # Extract the sizes of all objects in the panel
                    shapes = [obj['shape'] for obj in panel]

                    # Check if all sizes in the panel are the same
                    if all(shape == shapes[0] for shape in shapes):
                        return shapes[0]  # Return the consistent size
                    else:
                        return None  # Return None if sizes are inconsistent

                shape_to_num = {"triangle": 1, "square": 2, "pentagon": 3, "hexagon": 4, "circle": 5}
                left_shape = check_shape_consistency(left_panel)
                right_shape = check_shape_consistency(right_panel)

                if left_shape is None or right_shape is None:
                    correct_answer = "Not Comparable"
                elif left_shape == right_shape:
                    correct_answer = "Same"
                elif shape_to_num[left_shape] < shape_to_num[right_shape]:
                    correct_answer = "Fewer"
                else:
                    correct_answer = "More"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Fewer", "More", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the inner part of the two panels in the image. "
                            f"Is the shape of all the objects in the left panel have the same, more, or fewer edges "
                            f"compared to the objects in the right panel? "
                            f"If the shapes within either panel are already different from each other, select 'Not Comparable.' "
                            f"(Note: The edge number increases in the following order: triangle, square, pentagon, hexagon, circle)")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the shape of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the shape of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "size":
            if stage == "single_panel":

                sizes = [obj['size'] for obj in data['panels'][panel_index] if "inner" in obj["position"]]
                if len(sizes) == 1:
                    correct_answer = "Only one object"
                elif all(size == sizes[0] for size in sizes):
                    correct_answer = "Yes"
                else:
                    correct_answer = "No"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the inner part of the panel of the same size?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":

                left_panel = [obj for obj in data['panels'][panel_index] if "inner" in obj["position"]]
                right_panel = [obj for obj in data['panels'][panel_index + 1] if "inner" in obj["position"]]
                assert (len(left_panel) > 0 and len(right_panel) > 0)
                def check_size_consistency(panel):
                    # Extract the sizes of all objects in the panel
                    sizes = [obj['size'] for obj in panel]

                    # Check if all sizes in the panel are the same
                    if all(size == sizes[0] for size in sizes):
                        return sizes[0]  # Return the consistent size
                    else:
                        return None  # Return None if sizes are inconsistent

                left_size = check_size_consistency(left_panel)
                right_size = check_size_consistency(right_panel)

                if left_size is None or right_size is None:
                    correct_answer = "Not Comparable"
                elif left_size == right_size:
                    correct_answer = "Same"
                elif left_size < right_size:
                    correct_answer = "Smaller"
                else:
                    correct_answer = "Larger"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Smaller", "Larger", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the inner part of the two panels in the image. "
                            f"Is the size of all the objects in the left panel the same as, smaller "
                            f"or larger than the objects in the right panel? "
                            f"If the sizes within either panel are already different from each other, select 'Not Comparable.")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the size of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the size of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
        elif attribute == "color":
            if stage == "single_panel":
                colors = [obj['size'] for obj in data['panels'][panel_index] if "inner" in obj["position"]]
                if len(colors) == 1:
                    correct_answer = "Only one object"
                elif all(color == colors[0] for color in colors):
                    correct_answer = "Yes"
                else:
                    correct_answer = "No"
                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["Yes", "No", "Only one object"]
                random.shuffle(all_choices)

                # Generate the question
                question = f"Are all objects in the inner part of the panel of the same color?"

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_{panel_index + 1}.png"
                new_path = os.path.join(directory, new_filename)
                # Return the question and the list of answer choices
            elif stage == "two_panels":
                left_panel = [obj for obj in data['panels'][panel_index] if "inner" in obj["position"]]
                right_panel = [obj for obj in data['panels'][panel_index + 1] if "inner" in obj["position"]]

                def check_color_consistency(panel):
                    # Extract the sizes of all objects in the panel
                    colors = [obj['color'] for obj in panel]

                    # Check if all sizes in the panel are the same
                    if all(color == colors[0] for color in colors):
                        return colors[0]  # Return the consistent size
                    else:
                        return None  # Return None if sizes are inconsistent

                left_color = check_color_consistency(left_panel)
                right_color = check_color_consistency(right_panel)

                if left_color is None or right_color is None:
                    correct_answer = "Not Comparable"
                elif left_color == right_color:
                    correct_answer = "Same"
                elif left_color < right_color:
                    correct_answer = "Darker"
                else:
                    correct_answer = "Brighter"

                # Combine the correct answer with the other choices and shuffle them
                all_choices = ["The same", "Darker", "Brighter", "Not comparable"]
                random.shuffle(all_choices)

                # Generate the question
                question = (f"Consider only the inner part of the two panels in the image. "
                            f"Is the color of all the objects in the left panel the same as, "
                            f"darker or brighter than the objects in the right panel? "
                            f"If the colors within either panel are already different from each other, select 'Not Comparable.'")

                config = data["questions"][0]["config"]
                image_path = os.path.join(root_path, config, data["questions"][0]["image_filename"])
                directory = os.path.dirname(image_path)
                new_filename = f"panel_combination_{panel_index + 1}_{panel_index + 2}.png"
                new_path = os.path.join(directory, new_filename)
            elif stage == "one_row":
                for question in data["questions"]:
                    if "reasoning_first" in question["template_filename"] and "the color of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
            elif stage == "two_rows":
                for question in data["questions"]:
                    if "reasoning_second" in question["template_filename"] and "the color of" in question[
                        "question"] and ("inner" in question["question"] or "interior" in question["question"]):
                        return (question["question"], question["choices"], question["answer"], question["config"],
                                os.path.join(root_path, question["config"], question["image_filename"]))
    assert (question is not None and all_choices is not None and correct_answer is not None and config is not None and new_path is not None)
    return question, all_choices, correct_answer, config, new_path

def sample_positions(correct_answer, config):
    answers_number = {
      "center_single": 4,
      "distribute_four": 4,
      "distribute_nine": 4,
      "left_center_single_right_center_single": 2,
      "up_center_single_down_center_single": 2,
      "in_center_single_out_center_single": 2,
      "in_distribute_four_out_center_single": 4
    }
    answer_space = {
      "center_single": ["center", "top-left", "top-right", "bottom-left", "bottom-right"],
      "distribute_four": ["top-left", "top-right", "bottom-left", "bottom-right"],
      "distribute_nine": ["top-left", "top-center", "top-right", "middle-left", "middle-center", "middle-right", "bottom-left", "bottom-center", "bottom-right"],
      "left_center_single_right_center_single": ["left", "right"],
      "up_center_single_down_center_single": ["top", "down"],
      "in_center_single_out_center_single": ["the outer part", "the inner part"],
      "in_distribute_four_out_center_single": ["the outer part", "top-left of the inner part", "top-right of the inner part", "bottom-left of the inner part", "bottom-right of the inner part"]
    }
    all_positions = answer_space[config]
    sample_num = answers_number[config]
    choices = random.sample(all_positions, sample_num)
    if correct_answer not in choices:
        choices[random.randint(0, answers_number[config]-1)] = correct_answer

    return choices

random.seed(42)
# with open("logical_chain.json", "r") as json_file:
#     sampled_files = json.load(json_file)
sampled_files = sample_dataset()
print(len(sampled_files))
logical_chain_questions = load_questions_from_json(sampled_files)

# with open(output_dir, "w") as json_file:
#     json.dump(final_output, json_file, indent=4)

# with open("logical_chain_questions.json", "r") as json_file:
#     data = json.load(json_file)
data = logical_chain_questions
root_dir = "./RAVEN"
for instance in data:
    npz_file_name = instance["original_filename"].split(".")[0] + ".npz"
    config = instance["questions"][0]["config"]
    npz_file_path = os.path.join(root_dir, config, npz_file_name)
        
    npz_file = np.load(npz_file_path)
    answer = npz_file['target']
    prompt = "You are presented with a 3x3 grid of panels, called the 'Problem Matrix.' The last panel is missing and marked with a '?' symbol. "
    
    if config == "in_center_single_out_center_single" or config == "in_distribute_four_out_center_single":
        prompt += "Each panel is divided into two regions: an outer structure and an inner structure, with rules applied separately to each section. "
    elif config == "left_center_single_right_center_single":
        prompt += "Each panel divided into two sections by a vertical line, separating the left side from the right side, with rules applied separately to each section. "
    elif config == "up_center_single_down_center_single":
        prompt += "Each panel is split by a horizontal line, separating the top side from the bottom side, with rules applied separately to each section. "
    prompt += "Below the matrix, there is a set of 8 possible answer options labeled from 1 to 8. Your task is to determine which panel from the answer set (1-8) correctly fits the missing position in the problem matrix. The pattern in the matrix follows some hidden rules that apply row by row (horizontally). Please select the number (from 1 to 8) of the panel that completes the pattern."
    
    final_question = {"question": prompt,
                    "correct_answer": int(answer),
                    "config": config,
                    "image_path": os.path.join(os.path.dirname(instance["questions"][0]["image_path"]), "combined.png"),
                    "stage": "final"}
    instance["questions"].append(final_question)
    
# with open("logical_chain_questions_final.json", "w") as json_file:
#     json.dump(data, json_file)

# with open("logical_chain_questions_final.json", "r") as json_file:
#     data = json.load(json_file)


def update_stage_with_panel(data):
    for instance in data:
        for item in instance["questions"]:
            image_path = item['image_path']

            # Extract the panel number from the image filename
            panel_name = os.path.basename(image_path).split('.')[
                0]  # Get the filename without extension (e.g., panel_3)

            # Check if stage includes 'single_panel' or 'two_panels'
            if 'single_panel' in item['stage']:
                # Extract panel number from panel name and append it to the stage
                panel_number = panel_name.split('_')[-1]  # Get the last part of the panel name (e.g., 3 from panel_3)
                if "right" in item['stage'].split('_')[-1] or "left" in item['stage'].split('_')[-1]:
                    item['stage'] = f"single_panel_{panel_number}_right" if 'right' in item[
                        'stage'] else f"single_panel_{panel_number}_left"
                elif "top" in item['stage'].split('_')[-1] or "bottom" in item['stage'].split('_')[-1]:
                    item['stage'] = f"single_panel_{panel_number}_top" if 'top' in item[
                        'stage'] else f"single_panel_{panel_number}_bottom"
                elif "out" in item['stage'].split('_')[-1] or "in" in item['stage'].split('_')[-1]:
                    item['stage'] = f"single_panel_{panel_number}_out" if 'out' in item[
                        'stage'] else f"single_panel_{panel_number}_in"
                else:
                    item['stage'] = f"single_panel_{panel_number}"
            elif 'two_panels' in item['stage']:
                # Extract both panel numbers for two panels and append them to the stage
                panel_numbers = panel_name.split('_')[
                                -2:]  # Get the last two parts (e.g., 1_2 from panel_combination_1_2)
                if "right" in item['stage'].split('_')[-1] or "left" in item['stage'].split('_')[-1]:
                    item['stage'] = f"two_panels_{'_'.join(panel_numbers)}_right" if 'right' in item[
                        'stage'] else f"two_panels_{'_'.join(panel_numbers)}_left"
                elif "top" in item['stage'].split('_')[-1] or "bottom" in item['stage'].split('_')[-1]:
                    item['stage'] = f"two_panels_{'_'.join(panel_numbers)}_top" if 'top' in item[
                        'stage'] else f"two_panels_{'_'.join(panel_numbers)}_bottom"
                elif "out" in item['stage'].split('_')[-1] or "in" in item['stage'].split('_')[-1]:
                    item['stage'] = f"two_panels_{'_'.join(panel_numbers)}_out" if 'out' in item[
                        'stage'] else f"two_panels_{'_'.join(panel_numbers)}_in"
                else:
                    item['stage'] = f"two_panels_{'_'.join(panel_numbers)}"

    return data


# Apply the function to update the stages
updated_data = update_stage_with_panel(data)

# # Save the updated data back to a JSON file (if needed)
# with open("logical_chain_questions_final_updated.json", "w") as outfile:
#     json.dump(updated_data, outfile, indent=4)

# with open("logical_chain_questions_final_updated.json", "r") as json_file:
#     data = json.load(json_file)


def update_stage_with_panel(data):
    for instance in data:
        for item in instance["questions"]:
            if "choices" not in item:
                continue
            choices = item["choices"]
            correct_answer = item["correct_answer"]
            if correct_answer == "Same":
                correct_answer = "The same"
            if correct_answer == "Not Comparable":
                correct_answer = "Not comparable"
            if not any(isinstance(choice, str) and choice.startswith(('A:', 'B:', 'C:', 'D:')) for choice in choices):
                # Reformat the choices to include A:, B:, C:, D:
                updated_choices = [f"{chr(65 + i)}: {str(choice)}" for i, choice in enumerate(choices)]
                item["choices"] = updated_choices

                # Update the correct answer
                for i, choice in enumerate(updated_choices):
                    # Strip the prefix to match the correct answer with the original choices
                    if str(correct_answer) == str(choices[i]):
                        item["correct_answer"] = f"{chr(65 + i)}"
                        break

    return data


# Apply the function to update the stages
updated_data = update_stage_with_panel(updated_data)

# Save the updated data back to a JSON file (if needed)
with open(output_dir, "w") as outfile:
    json.dump(updated_data, outfile, indent=4)