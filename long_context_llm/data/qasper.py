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

def prepare_k_shot_prompt(articles, k):
    """
    Args:
    articles (list of dict): A list of dictionaries, each containing the title, abstract, questions, and answers of an article.
    k (int): The number of examples (articles) to include in the prompt.

    Returns:
    str: A formatted string k-shot learning prompt from multiple QASPER dataset articles
    """
    prompt = ""

    # Ensure we do not exceed the number of available articles
    k = min(k, len(articles))

    # Process each article
    for i in range(k):
        article = articles[i]
        
        # Adding Title
        prompt += f"Article {i+1}:\n[Title] " + article['title'] + "\n"

        # Adding Abstract
        prompt += "[Abstract] " + article['abstract'] + "\n"

        # Adding Full Text
        full_text_sections = article['full_text']['section_name']
        full_text_paragraphs = article['full_text']['paragraphs']
        
        for j, (section_name, paragraphs) in enumerate(zip(full_text_sections, full_text_paragraphs)):
            prompt += f"\n[Section {j+1}] {section_name}\n"
            for paragraph in paragraphs:
                prompt += f"{paragraph}\n"

        # Adding Questions and Answers
        for l, (question, answer_block) in enumerate(zip(article['qas']['question'], article['qas']['answers'])):
            
            prompt += f"[Q{l+1}] {question}\n"

            answers = answer_block['answer']

            if answers[0]['free_form_answer'] != '': # free answer
                max_free = answers[0]['free_form_answer']
                for answer in answers:
                    if len(answer['free_form_answer']) > len(max_free):
                        max_free = answer['free_form_answer']
                answer_text = max_free
            elif answers[0]['extractive_spans']: # Extractive
                max_span = answers[0]['extractive_spans']
                for answer in answers:
                    if len(answer['extractive_spans']) > len(max_span): # compare len of lists
                        max_span = answer['extractive_spans']
                answer_text = "; ".join(max_span).strip()
            else:
                raise ValueError('Both free_form and extractive are empty')
                
            prompt += f"[A{l+1}] {answer_text}\n"

        # Separator between articles
        if i < k - 1:
            prompt += "\n---\n\n"

    # remove unwanted characters
    for char in ['“', '”', '’', '|', '%', '&', '/']:
        prompt = prompt.replace(char, '')
        
    return prompt
