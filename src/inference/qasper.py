from collections import Counter
import numpy as np

def f1_score_single(prediction, ground_truth):
    prediction_tokens = prediction.split()
    ground_truth_tokens = ground_truth.split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    
    if num_same == 0:
        return 0

    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    
    return f1

def compute_f1_score(dataset, model_predictions, k):
    total_f1 = 0
    num_questions = len(dataset['qas']['question'])

    for i in range(min(num_questions, k)):
        ground_truth_answers = [answer['free_form_answer'] for answer in dataset['qas']['answers'][i]]
        prediction = model_predictions[i]

        # Compute F1 for each ground truth and take the maximum as the final F1 for this question
        question_f1_scores = [f1_score_single(prediction, truth) for truth in ground_truth_answers]
        max_f1 = max(question_f1_scores)
        
        total_f1 += max_f1

    # Average F1 score across all questions
    avg_f1 = total_f1 / min(num_questions, k)
    return avg_f1

# Example usage
dataset_example = {
    # ... (your dataset structure here)
}

model_predictions = [
    # ... (your model predictions here for each question)
]

k = 5  # Number of shots for in-context learning
f1 = compute_f1_score(dataset_example, model_predictions, k)
print(f1)
