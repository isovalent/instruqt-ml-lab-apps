from flask import Flask, request, jsonify
import ollama
import yaml
import os

app = Flask(__name__)

SYSTEM_PROMPT = """You are a helpful AI assistant that generates YAML configurations."""

@app.route('/query', methods=['POST'])
def query():
    user_prompt = request.json.get('prompt', '')
    
    # Call Ollama
    response = ollama.chat(model='gemma2:2b', messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt}
    ])
    
    ai_response = response['message']['content']

    # Log the AI response
    print("AI Response:", ai_response)

    # Check YAML config by parsing it
    
    import re
    # Look for YAML code blocks (```yaml or just ```)
    yaml_pattern = r'```(?:yaml)?\s*\n(.*?)\n```'
    yaml_matches = re.findall(yaml_pattern, ai_response, re.DOTALL)
    
    if yaml_matches:
        try:
            # Use the first YAML block found
            yaml_content = yaml_matches[0].strip()
            
            # Parse YAML - THIS IS DANGEROUS with default Loader!
            config = yaml.load(yaml_content, Loader=yaml.Loader)  # Unsafe loader
            
            return config
        except Exception as e:
            return jsonify({'error': f'Failed to parse YAML: {str(e)}', 'response': ai_response, 'yaml_content': yaml_content})
    
    # Try to parse the output directly
    try:
        config = yaml.load(ai_response, Loader=yaml.Loader)  # Unsafe loader
        return config
    except Exception as e:
        return jsonify({'error': f'Failed to parse YAML: {str(e)}', 'response': ai_response, 'yaml_content': ai_response})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)