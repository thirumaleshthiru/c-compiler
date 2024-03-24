import sys
import subprocess
from io import StringIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def compile_and_run_c_code(code, input_data=None):
    try:
        # Redirect stdout to capture the output
        sys.stdout = result_output = StringIO()

        # Write the C code to a temporary file
        with open('temp.c', 'w') as f:
            f.write(code)

        # Prepare input data if provided
        input_bytes = None
        if input_data:
            input_bytes = input_data.encode()

        # Compile the C code using GCC
        compile_process = subprocess.run(['gcc', 'temp.c', '-o', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input_bytes)

        if compile_process.returncode == 0:
            # If compilation is successful, execute the compiled program
            execution_process = subprocess.run(['./temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input_bytes)
            output_text = execution_process.stdout.decode('utf-8')
            return {'success': True, 'output': output_text}
        else:
            # If compilation fails, return the compilation error
            compile_error = compile_process.stderr.decode('utf-8')
            return {'success': False, 'error': compile_error}
    except Exception as e:
        # If any error occurs during compilation or execution, return the error message
        return {'success': False, 'error': str(e)}
    finally:
        # Reset stdout to its default value
        sys.stdout = sys.__stdout__
        # Clean up temporary files
        subprocess.run(['rm', 'temp.c', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@app.route('/compile-run-c', methods=['POST'])
def compile_run_c():
    data = request.json
    code = data.get('code')
    input_data = data.get('input')

    if code:
        # Call the function to compile and run the provided C code
        result = compile_and_run_c_code(code, input_data)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
