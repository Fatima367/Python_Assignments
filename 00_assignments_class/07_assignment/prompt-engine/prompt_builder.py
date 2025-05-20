class Prompt:
    """Class representing an AI prompt with its components."""
    
    def __init__(self, content="", context="", instructions="", examples=None):
        self.content = content
        self.context = context
        self.instructions = instructions
        self.examples = examples or []
    
    def build(self):
        """Builds the complete prompt from its components."""
        prompt_parts = []
        
        if self.context:
            prompt_parts.append(f"Context: {self.context}")
        
        if self.instructions:
            prompt_parts.append(f"Instructions: {self.instructions}")
        
        if self.examples:
            examples_text = "\n".join([f"- {example}" for example in self.examples])
            prompt_parts.append(f"Examples:\n{examples_text}")
        
        if self.content:
            prompt_parts.append(f"Content: {self.content}")
        
        return "\n\n".join(prompt_parts)


class UseCase:
    """Class representing a specific use case for prompt generation."""
    
    def __init__(self, id, name, questions=None):
        self.id = id
        self.name = name
        self.questions = questions or []
    
    def get_question_by_id(self, question_id):
        """Retrieves a question by its ID."""
        for question in self.questions:
            if question.get('id') == question_id:
                return question
        return None


class PromptBuilder:
    """Class responsible for building prompts based on use cases and user answers."""
    
    def __init__(self):
        self.use_cases = self._initialize_use_cases()
    
    def _initialize_use_cases(self):
        """Initialize the available use cases."""
        return {
            'email': UseCase('email', 'Write Email', [
                {'id': 'recipient', 'label': 'Who is the recipient?', 'type': 'text'},
                {'id': 'purpose', 'label': 'What is the purpose of the email?', 'type': 'text_area'},
                {'id': 'tone', 'label': 'What tone would you like?', 'type': 'select', 
                 'options': ['Professional', 'Friendly', 'Urgent', 'Formal']}
            ]),
            'summary': UseCase('summary', 'Summarize Article', [
                {'id': 'article', 'label': 'Paste the article text', 'type': 'text_area'},
                {'id': 'length', 'label': 'Desired summary length', 'type': 'select', 
                 'options': ['Brief (1-2 sentences)', 'Short (paragraph)', 'Detailed (multiple paragraphs)']}
            ]),
            'social': UseCase('social', 'Social Media Post', [
                {'id': 'platform', 'label': 'Which platform?', 'type': 'select', 
                 'options': ['Twitter/X', 'LinkedIn', 'Instagram', 'Facebook']},
                {'id': 'topic', 'label': 'What is the post about?', 'type': 'text_area'},
                {'id': 'goal', 'label': 'What do you want to achieve?', 'type': 'select', 
                 'options': ['Engagement', 'Information', 'Promotion', 'Entertainment']}
            ])
        }
    
    def get_use_cases(self):
        """Returns all available use cases."""
        return self.use_cases
    
    def get_use_case(self, use_case_id):
        """Get a use case by its ID."""
        return self.use_cases.get(use_case_id)
    
    def build_prompt(self, use_case_id, answers):
        """Build a prompt based on the use case and user answers."""
        use_case = self.get_use_case(use_case_id)
        if not use_case:
            return None
        
        # Build the prompt based on the use case
        if use_case_id == 'email':
            return self._build_email_prompt(answers)
        elif use_case_id == 'summary':
            return self._build_summary_prompt(answers)
        elif use_case_id == 'social':
            return self._build_social_prompt(answers)
        
        return None
    
    def _build_email_prompt(self, answers):
        """Build a prompt for email writing."""
        prompt = Prompt()
        
        recipient = answers.get('recipient', '')
        purpose = answers.get('purpose', '')
        tone = answers.get('tone', '')
        
        prompt.instructions = f"Write an email to {recipient} about {purpose}. Use a {tone.lower()} tone."
        
        return prompt.build()
    
    def _build_summary_prompt(self, answers):
        """Build a prompt for article summarization."""
        prompt = Prompt()
        
        article = answers.get('article', '')
        length = answers.get('length', '')
        
        prompt.content = article
        prompt.instructions = f"Summarize the above article. Make the summary {length.lower()}."
        
        return prompt.build()
    
    def _build_social_prompt(self, answers):
        """Build a prompt for social media post creation."""
        prompt = Prompt()
        
        platform = answers.get('platform', '')
        topic = answers.get('topic', '')
        goal = answers.get('goal', '')
        
        prompt.instructions = f"Create a {platform} post about {topic}. The post should aim to {goal.lower()} the audience."
        
        if platform == 'Twitter/X':
            prompt.instructions += " Keep it under 280 characters."
        
        return prompt.build()