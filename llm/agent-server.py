from flask import Flask, request, jsonify, Response
import ollama
import yaml
import os
import sys

app = Flask(__name__)

SYSTEM_PROMPT = """You are a helpful AI assistant that generates YAML configurations."""

@app.route('/query', methods=['POST'])
def query():
    # Log with timestamp
    import datetime
    print(f"\n[{datetime.datetime.now().isoformat()}] Received /query request", flush=True)
    user_prompt = request.json.get('prompt', '')
    
    # Call Ollama with response size limits
    response = ollama.chat(
        model='gemma2:2b', 
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt}
        ],
        options={
            'num_predict': 500,  # Maximum tokens to generate
            'temperature': 0.7,
            'top_p': 0.9
        }
    )

    print(f"[{datetime.datetime.now().isoformat()}] Received response from Ollama", flush=True)
    
    ai_response = response['message']['content']

    # Log the AI response
    print("="*50, flush=True)
    print("AI RESPONSE:", ai_response, flush=True)
    print("="*50, flush=True)
    sys.stdout.flush()

    # Check YAML config by parsing it
    
    import re
    # Look for YAML code blocks (```yaml or just ```)
    yaml_pattern = r'```(?:yaml)?\s*\n(.*?)\n```'
    yaml_matches = re.findall(yaml_pattern, ai_response, re.DOTALL)
    
    if yaml_matches:
        try:
            # Use the first YAML block found
            yaml_content = yaml_matches[0].strip()
            configs = yaml.load_all(yaml_content, Loader=yaml.Loader)
            if configs is not None:
                yaml_output = yaml.dump_all(configs, default_flow_style=False, allow_unicode=True)
                return Response(yaml_output, mimetype='text/yaml')
        except Exception as e:
            return jsonify({'error': f'Failed to parse generated YAML: {str(e)}', 'response': ai_response, 'yaml_content': yaml_content})
    
    # Try to parse the output directly
    try:
        configs = yaml.load_all(ai_response, Loader=yaml.Loader)
        if configs is not None:
            yaml_output = yaml.dump_all(configs, default_flow_style=False, allow_unicode=True)
            return Response(yaml_output, mimetype='text/yaml')
    except Exception as e:
        return jsonify({'error': f'Failed to parse generated YAML: {str(e)}', 'response': ai_response, 'yaml_content': ai_response})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)