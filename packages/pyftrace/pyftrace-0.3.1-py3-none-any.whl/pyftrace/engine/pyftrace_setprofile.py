import sys
import os
import time
import sysconfig
from ..tracer import PyftraceBase
from ..utils import *

class PyftraceSetprofile(PyftraceBase):
    """
    sys.setprofile based tracer
    """
    def setup_tracing(self):
        sys.setprofile(self.profile_func)

    def cleanup_tracing(self):
        sys.setprofile(None)

    def run_python_script(self, script_path, script_args):
        if self.output_stream:
            print(f"Running script: {script_path}", file=self.output_stream)

        self.script_name = os.path.abspath(script_path)
        self.script_dir = os.path.dirname(self.script_name)

        # For use import_end_line to start tracing after imports
        self.import_end_line = find_import_end_line(script_path)

        with open(script_path, "r") as file:
            script_code = file.read()
            code_object = compile(script_code, script_path, 'exec')

        old_sys_path = sys.path.copy()
        old_sys_argv = sys.argv.copy()
        sys.path.insert(0, self.script_dir)
        sys.argv = [script_path] + script_args

        self.tracing_started = False

        self.setup_tracing()

        try:
            exec(code_object, {"__file__": script_path, "__name__": "__main__"})
        finally:
            self.tracing_started = False
            self.cleanup_tracing()
            sys.path = old_sys_path
            sys.argv = old_sys_argv

    def profile_func(self, frame, event, arg):
        if event == "call":
            self.handle_call_event(frame, arg)
        elif event == "return":
            self.handle_return_event(frame, arg, is_c_return=False)
        elif event == "c_call":
            self.handle_call_event(frame, arg, is_c_call=True)
        elif event == "c_return":
            self.handle_return_event(frame, arg, is_c_return=True)
        elif event == "c_exception":
            pass
        else:
            pass

    def handle_call_event(self, frame, arg, is_c_call=False):
        if is_c_call:
            # Get the '__name__' attribute of 'arg', or use str(arg) if '__name__' is not present
            func_name = getattr(arg, '__name__', str(arg))
            # Retrieve the '__module__' attribute of 'arg', or use '' if it's not available
            module_name = getattr(arg, '__module__', '') or ''
            code = None
            filename = None
            caller_frame = frame
        else:
            code = frame.f_code
            func_name = code.co_name
            # Retrieve the module's name from frame's globals, defaulting to '' if not available
            module_name = frame.f_globals.get('__name__', '') or ''
            filename = resolve_filename(code, None)
            caller_frame = frame.f_back

        # print(f"[DEBUG] handle_call_event: event={'c_call' if is_c_call else 'call'}, func_name={func_name}, module_name={module_name}, filename={filename}")

        if filename:
            filename = os.path.abspath(filename)

        if filename and filename.startswith(self.tracer_dir):
            return

        if not self.tracing_started:
            start_tracing = False
            if filename == self.script_name and code and frame.f_lineno > self.import_end_line:
                start_tracing = True
            else:
                if caller_frame and caller_frame.f_code:
                    caller_filename = resolve_filename(caller_frame.f_code, None)
                    if caller_filename:
                        caller_filename = os.path.abspath(caller_filename)
                    if (caller_filename == self.script_name
                        and caller_frame.f_lineno > self.import_end_line):
                        start_tracing = True

            if not start_tracing:
                return
            self.tracing_started = True

        if func_name == '<module>':
            return

        trace_this = False

        if self.is_stdlib_code(filename):
            if not self.verbose:
                return
            trace_this = True
        else:
            if filename is None:
                # filename is None: C-extension or similar. If verbose, trace anyway.
                if self.verbose:
                    trace_this = True
            else:
                # Normal logic for user-defined or third-party code
                if self.should_trace(filename):
                    trace_this = True
                elif self.verbose and module_name == 'builtins':
                    trace_this = True

        if trace_this:
            self.call_stack.append(func_name)
            indent = "    " * self.current_depth()

            if not is_c_call and code:
                func_def_lineno = code.co_firstlineno
            else:
                func_def_lineno = ''

            if caller_frame:
                call_lineno = caller_frame.f_lineno
                call_filename = resolve_filename(caller_frame.f_code, None)
                if call_filename:
                    call_filename = os.path.abspath(call_filename)
            else:
                call_lineno = ''
                call_filename = ''

            if self.show_path:
                if func_def_lineno:
                    func_location = f"{func_name}@{filename}:{func_def_lineno}" if filename else func_name
                else:
                    func_location = f"{func_name}@{filename}" if filename else func_name
                if call_filename and call_lineno:
                    call_location = f"from {call_filename}:{call_lineno}"
                else:
                    call_location = f"from line {call_lineno}"
            else:
                func_location = func_name
                call_location = f"from line {call_lineno}"

            if not self.report_mode and self.output_stream:
                if self.max_depth is None or self.current_depth() <= self.max_depth:
                    print(f"{indent}Called {func_location} {call_location}", file=self.output_stream)

            if self.report_mode:
                start_time = time.time()
                if func_name in self.execution_report:
                    _, total_time, call_count = self.execution_report[func_name]
                    self.execution_report[func_name] = (start_time, total_time, call_count + 1)
                else:
                    self.execution_report[func_name] = (start_time, 0, 1)

    def handle_return_event(self, frame, arg, is_c_return):
        if not self.tracing_started:
            return

        if is_c_return:
            func_name = getattr(arg, '__name__', str(arg))
            module_name = getattr(arg, '__module__', '') or ''
            code = None
            filename = None
        else:
            code = frame.f_code
            func_name = code.co_name
            module_name = frame.f_globals.get('__name__', '') or ''
            filename = resolve_filename(code, None)

        # # print(f"[DEBUG] handle_return_event: event={'c_return' if is_c_return else 'return'}, func_name={func_name}, module_name={module_name}, filename={filename}")

        if filename:
            filename = os.path.abspath(filename)

        if filename and filename.startswith(self.tracer_dir):
            return

        if func_name == '<module>':
            return

        trace_this = False

        if self.is_stdlib_code(filename):
            if not self.verbose:
                return
            trace_this = True
        else:
            if filename is None:
                if self.verbose and self.call_stack and self.call_stack[-1] == func_name:
                    trace_this = True
            else:
                if self.call_stack and self.call_stack[-1] == func_name:
                    trace_this = True
                else:
                    if self.verbose and module_name == 'builtins':
                        if self.call_stack and self.call_stack[-1] == func_name:
                            trace_this = True

        if trace_this and self.call_stack and self.call_stack[-1] == func_name:
            indent = "    " * self.current_depth()

            if self.show_path:
                file_info = f" @ {filename}" if filename else ""
            else:
                file_info = ""

            if not self.report_mode and self.output_stream:
                if self.max_depth is None or self.current_depth() <= self.max_depth:
                    return_value = ''
                    if not is_c_return:
                        return_value = f"-> {arg}"
                    print(f"{indent}Returning {func_name}{return_value}{file_info}", file=self.output_stream)

            if self.report_mode and func_name in self.execution_report:
                start_time, total_time, call_count = self.execution_report[func_name]
                exec_time = time.time() - start_time
                self.execution_report[func_name] = (start_time, total_time + exec_time, call_count)

            self.call_stack.pop()

