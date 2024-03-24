import sys
from io import StringIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def compile_and_run_python_code(code, input_data=None):
    try:
        # Redirect stdout and stdin
        sys.stdout = result_output = StringIO()
        if input_data:
            sys.stdin = StringIO(input_data)

        # Compile and execute the code
        compiled_output = compile(code, '<string>', 'exec')
        exec(compiled_output)

        # Get the captured output
        output_text = result_output.getvalue()
        return {'success': True, 'output': output_text}
    except Exception as e:
        # If any error occurs during compilation or execution, return the error message
        return {'success': False, 'error': str(e)}
    finally:
        # Reset stdout and stdin to their default values
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

@app.route('/compile-run', methods=['POST'])
def compile_run():
    data = request.json
    code = data.get('code')
    input_data = data.get('input')  # assuming input is provided in the request

    if code:
        # Call the function to compile and run the provided Python code
        result = compile_and_run_python_code(code, input_data)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080):this is a code for online compiler for python now i will give for c languge update the code for taking inputsimport sys
import subprocess
from io import StringIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def compile_and_run_c_code(code):
    try:
        # Redirect stdout to capture the output
        sys.stdout = result_output = StringIO()

        # Write the C code to a temporary file
        with open('temp.c', 'w') as f:
            f.write(code)

        # Compile the C code using GCC
        compile_process = subprocess.run(['gcc', 'temp.c', '-o', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if compile_process.returncode == 0:
            # If compilation is successful, execute the compiled program
            execution_process = subprocess.run(['./temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    if code:
        # Call the function to compile and run the provided C code
        result = compile_and_run_c_code(code)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
