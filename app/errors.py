from flask import jsonify

def not_found_error(error):
    return jsonify({"msg": "Resource not found"}), 404

def internal_error(error):
    # In a real app, you would log the error
    return jsonify({"msg": "An internal error occurred"}), 500

def bad_request_error(error):
    description = getattr(error, 'description', 'Bad request')
    return jsonify({"msg": str(description)}), 400

def register_error_handlers(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(400, bad_request_error)