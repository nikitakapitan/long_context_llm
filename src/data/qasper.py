# Example usage with your dataset example
dataset_example = {
    'id': '1909.00694',  
    'title': 'Minimally Supervised Learning of Affective Events Using Discourse Relations',  
    'abstract': 'Recognizing affective events that trigger positive or negative sentiment has...',  
    'full_text': {  
        'section_name': ["Introduction", "Related Work"],  
        'paragraphs': [  
            ["intro_parag1_text", "intro_parag2_text"],  
            ["relatedWork_parag1_text"]
        ],
    },
    'qas': {  
        'question': ["What is minimally supervised learning?", "How are affective events recognized?"],  
    }
}

def prepare_prompt_for_inference(dataset_example):
    # Extract relevant fields from the dataset example
    title = dataset_example['title']
    abstract = dataset_example['abstract']
    full_text_sections = dataset_example['full_text']['section_name']
    full_text_paragraphs = dataset_example['full_text']['paragraphs']
    
    # Combine title, abstract, and selected full text into a single context string
    context = f"Title: {title}\nAbstract: {abstract}\n"
    for section_name, paragraphs in zip(full_text_sections, full_text_paragraphs):
        context += f"\nSection: {section_name}\n"
        for paragraph in paragraphs:
            context += f"{paragraph}\n"
    
    # Combine all questions into a single prompt
    prompt = context + "\nQuestions:\n"
    for question in dataset_example['qas']['question']:
        prompt += f"- {question}\n"
    
    return prompt



prompt = prepare_prompt_for_inference(dataset_example)
print(prompt)
