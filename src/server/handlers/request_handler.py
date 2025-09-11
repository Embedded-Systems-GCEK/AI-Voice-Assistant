from flask import request, jsonify
from typing import Dict, Any, Tuple, Optional

class RequestHandler:
    """Handler for processing incoming requests"""
    
    @staticmethod
    def get_json_data() -> Dict[str, Any]:
        """Get JSON data from request"""
        try:
            return request.get_json() or {}
        except Exception as e:
            print(f"Error parsing JSON data: {e}")
            return {}
    
    @staticmethod
    def get_query_params() -> Dict[str, str]:
        """Get query parameters from request"""
        return dict(request.args)
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Tuple[bool, str]:
        """Validate that required fields are present in data"""
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"{field} is required"
        return True, ""

class ResponseHandler:
    """Handler for creating standardized responses"""
    
    @staticmethod
    def success(message: str, data: Optional[Dict[str, Any]] = None, status_code: int = 200):
        """Create success response"""
        response = {'message': message}
        if data:
            response.update(data)
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str, status_code: int = 400):
        """Create error response"""
        return jsonify({'error': message}), status_code
    
    @staticmethod
    def not_found(resource: str = "Resource"):
        """Create not found response"""
        return jsonify({'error': f'{resource} not found'}), 404
    
    @staticmethod
    def validation_error(message: str):
        """Create validation error response"""
        return jsonify({'error': message}), 400
    
    @staticmethod
    def server_error(message: str = "Internal server error"):
        """Create server error response"""
        return jsonify({'error': message}), 500
    
    @staticmethod
    def conflict(message: str):
        """Create conflict response"""
        return jsonify({'error': message}), 409

class CORSHandler:
    """Handler for CORS preflight requests"""
    
    @staticmethod
    def handle_preflight():
        """Handle preflight OPTIONS requests"""
        if request.method == "OPTIONS":
            response = jsonify({'status': 'ok'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
            response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
            return response
        return None
