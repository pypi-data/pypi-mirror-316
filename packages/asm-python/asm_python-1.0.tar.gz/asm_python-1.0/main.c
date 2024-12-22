#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static PyObject* py_asm(PyObject* self, PyObject* args) {
    const char* code;  // Chuỗi mã assembly từ Python
    FILE *asm_file;
    char* asm_filename = "temp.asm";
    char* obj_filename = "temp.o";
    char* exec_filename = "temp_exec";
    char cmd[1024];
    long result = 0;

    // Nhận mã assembly từ Python
    if (!PyArg_ParseTuple(args, "s", &code)) {
        return NULL;  // Nếu không nhận được chuỗi mã assembly hợp lệ
    }

    // Tạo file tạm để lưu mã assembly
    asm_file = fopen(asm_filename, "w");
    if (asm_file == NULL) {
        PyErr_SetString(PyExc_IOError, "Unable to create ASM file.");
        return NULL;
    }

    fprintf(asm_file, "%s", code);
    fclose(asm_file);

    // Kiểm tra hệ điều hành và áp dụng cách biên dịch phù hợp
    #if defined(__APPLE__) && defined(__MACH__)  // macOS
        // Biên dịch mã assembly cho macOS với clang
        snprintf(cmd, sizeof(cmd), "clang -target x86_64-apple-macos10.9 -c -o %s %s", obj_filename, asm_filename);
        if (system(cmd) != 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to assemble the code on macOS.");
            return NULL;
        }

        // Liên kết mã object với clang cho macOS
        snprintf(cmd, sizeof(cmd), "clang -o %s %s", exec_filename, obj_filename);
        if (system(cmd) != 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to link the object file on macOS.");
            return NULL;
        }
    
    #elif defined(__linux__)  // Linux
        // Biên dịch mã assembly cho Linux với clang
        snprintf(cmd, sizeof(cmd), "clang -c -o %s %s", obj_filename, asm_filename);
        if (system(cmd) != 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to assemble the code on Linux.");
            return NULL;
        }

        // Liên kết mã object với clang cho Linux
        snprintf(cmd, sizeof(cmd), "clang -o %s %s", exec_filename, obj_filename);
        if (system(cmd) != 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to link the object file on Linux.");
            return NULL;
        }
    
    #elif defined(_WIN32) || defined(_WIN64)  // Windows
        // Biên dịch mã assembly cho Windows với clang
        snprintf(cmd, sizeof(cmd), "clang -c -o %s %s", obj_filename, asm_filename);
        if (system(cmd) != 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to assemble the code on Windows.");
            return NULL;
        }

        // Liên kết mã object với clang cho Windows
        snprintf(cmd, sizeof(cmd), "clang -o %s %s", exec_filename, obj_filename);
        if (system(cmd) != 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to link the object file on Windows.");
            return NULL;
        }
    
    #else
        PyErr_SetString(PyExc_RuntimeError, "Unsupported operating system.");
        return NULL;
    #endif

    // Thực thi chương trình đã biên dịch và liên kết
    snprintf(cmd, sizeof(cmd), "./%s", exec_filename);
    FILE *fp = popen(cmd, "r");
    if (fp == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to execute the assembled code.");
        return NULL;
    }

    // Đọc kết quả trả về từ chương trình đã thực thi
    if (fscanf(fp, "%ld", &result) != 1) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to read the result of the execution.");
        fclose(fp);
        return NULL;
    }

    fclose(fp);

    // Xóa các file tạm sau khi thực thi
    remove(asm_filename);
    remove(obj_filename);
    remove(exec_filename);

    // Trả kết quả về cho Python
    return PyLong_FromLong(result);
}

static PyMethodDef methods[] = {
    {"asm", py_asm, METH_VARARGS, "Execute assembly code."},
    {NULL, NULL, 0, NULL}  
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "asm_python",   // Tên mô-đun
    "A module that executes assembly code.",  
    -1,
    methods
};

PyMODINIT_FUNC PyInit_asm_python(void) {
    return PyModule_Create(&module);
}
