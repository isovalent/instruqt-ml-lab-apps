from flask import Flask, request, jsonify
import ollama
import subprocess
import os

app = Flask(__name__)

SYSTEM_PROMPT = """You are a helpful AI assistant. 
You can help users with questions and tasks."""

@app.route('/query', methods=['POST'])
def query():
    user_prompt = request.json.get('prompt', '')
    
    # Call Ollama
    response = ollama.chat(model='tinyllama', messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt}
    ])
    
    ai_response = response['message']['content']
    
    # VULNERABLE: Check if AI suggests a command and execute it
    if 'EXECUTE:' in ai_response:
        # Better parsing: get the line with EXECUTE: and extract the command
        lines = ai_response.split('\n')
        for line in lines:
            if 'EXECUTE:' in line:
                # Extract everything after EXECUTE: on that line
                command = line.split('EXECUTE:')[1].strip()
                # Remove ALL quotes (single and double) and common punctuation
                command = command.strip().strip('"`\'.,;')
                # Also strip quotes from inside if they wrap the whole command
                if (command.startswith('"') and command.endswith('"')) or \
                   (command.startswith("'") and command.endswith("'")):
                    command = command[1:-1]
                
                try:
                    result = subprocess.run(
                        command, 
                        shell=True, 
                        capture_output=True, 
                        text=True,
                        timeout=5
                    )
                    return jsonify({
                        'response': ai_response,
                        'command_executed': command,
                        'output': result.stdout,
                        'error': result.stderr
                    })
                except Exception as e:
                    return jsonify({'error': str(e), 'response': ai_response})
                break
    
    return jsonify({'response': ai_response})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)