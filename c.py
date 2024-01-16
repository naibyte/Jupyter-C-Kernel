from ipykernel.kernelbase import Kernel
import os
import subprocess

def compile_and_run(source_code):
    if os.path.isfile("/tmp/c_jupyter_kernel_program"):
        os.remove("/tmp/c_jupyter_kernel_program")

    open("/tmp/c_jupyter_kernel_code.c","w").write(source_code)
    output = ''
    try:
        proc_output = subprocess.check_output(["gcc", "-o", "/tmp/c_jupyter_kernel_program", "/tmp/c_jupyter_kernel_code.c"], stderr=subprocess.STDOUT)
        output += proc_output.decode()
    except Exception as exc:
        output += exc.output.decode()
        return output
        
    try:        
        proc_output += subprocess.check_output(["/tmp/c_jupyter_kernel_program"])
        output += proc_output.decode()
    except Exception as exc:
        output += exc.output.decode()
        return output
        
    return output

class C_Kernel(Kernel):
    implementation = 'C'
    implementation_version = '1.0'
    language = 'C'
    language_version = '3.6'
    language_info = {'name': 'C',
                     'mimetype': 'text/plain',
                     'extension': '.c'}
    banner = "C"

    def do_execute(self, code, silent,
                    store_history=True,
                    user_expressions=None,
                    allow_stdin=False):

        ##############################
        output = compile_and_run(code)
        ##############################

        if not silent:
            self.send_response(
                self.iopub_socket,
                'stream', {
                    'name': 'stdout',
                    'data': ''
                    }
            )

            content = {
                'source': 'kernel',
                'data': {
                    'text/plain': output
                },
                'metadata' : {
                    }
            }

            self.send_response(self.iopub_socket,
                'display_data', content)

        return {'status': 'ok',
                'execution_count':
                    self.execution_count,
                'payload': [],
                'user_expressions': {},
                }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(
        kernel_class=C_Kernel)