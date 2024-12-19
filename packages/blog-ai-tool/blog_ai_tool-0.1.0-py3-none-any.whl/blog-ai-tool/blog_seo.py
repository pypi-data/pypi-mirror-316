import frontmatter
import os
from openai import OpenAI
from typing import Dict, Optional
import json
import re

class HugoBlogProcessor:
    def __init__(self, api_key: str, base_url: str, model: str, language: str, config: dict):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.language = language
        self.config = config
        if self.config["metadata"]["language"] == "auto":
            self.language = "the same as the blog content"

    def generate_metadata(self, content: str) -> Dict[str, str]:
        """Generate metadata using OpenAI based on content"""
        metadata_config = self.config["metadata"]
        prompt = f"""Based on the following blog content, generate:
1. A concise title (max {metadata_config['max_title_length']} chars)
2. A brief description (max {metadata_config['max_description_length']} chars)
3. {metadata_config['keyword_count']} relevant keywords (space-separated)
The language should be {self.language}.

Content:
{content}

Format response as JSON with keys: title, description, keywords"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        
        # Simplified regular expression to extract JSON content
        json_pattern = r'\{.*?\}'

        # Search for JSON in the response
        match = re.search(json_pattern, response.choices[0].message.content, re.DOTALL)
        
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                print("Failed to parse JSON from the extracted content.")
        
        print("No valid JSON found in the response.")
        return {}

    def process_markdown(self, file_path: str) -> None:
        """Process a markdown file and update its front matter"""
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        content = post.content
        metadata = post.metadata

        # Check for missing metadata
        needs_update = False
        if not metadata.get('title') or not metadata.get('description') or not metadata.get('keywords'):
            print(f"Generating metadata for {file_path}")
            generated = self.generate_metadata(content)
            needs_update = True

            # Update missing fields only
            if not metadata.get('title'):
                metadata['title'] = generated['title']
            if not metadata.get('description'):
                metadata['description'] = generated['description']
            if not metadata.get('keywords'):
                metadata['keywords'] = generated['keywords']

        if needs_update:
            # Create new post with updated metadata
            new_post = frontmatter.Post(content, **metadata)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(new_post))

def process_blog_directory(directory: str, api_key: str, base_url: str, model: str, language: str, config: dict):
    """Process all markdown files in a directory"""
    processor = HugoBlogProcessor(api_key, base_url, model, language, config)
    retry_count = config["system"]["retry_count"]
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                attempts = retry_count
                while attempts > 0:
                    try:
                        file_path = os.path.join(root, file)
                        processor.process_markdown(file_path) 
                        break
                    except Exception as e:
                        print(f"Failed to process {file_path}: {e}")
                        print(f"Attempts remaining: {attempts-1}")
                        attempts -= 1
