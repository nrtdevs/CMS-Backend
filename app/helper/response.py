from flask import Flask, jsonify, request
def success_response(data, message="Request processed successfully", status_code=200, meta=None):
    response = {
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
        "meta": meta
    }
    return jsonify(response), status_code

def error_response(message="An error occurred", errors=None, status_code=400):
    response = {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors
    }
    return jsonify(response), status_code