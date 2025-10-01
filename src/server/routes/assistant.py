from flask import Blueprint, jsonify
from logging import getLogger as get_logger



# from .routes import device_list, home_page_view

# Initialize logger
logger = get_logger("api")

# Create API blueprint
assistant_bp = Blueprint("api", __name__)



@assistant_bp.route("/api/health")
def healthz():
    return jsonify({"ok": True}), 200




# @api_bp.route("/api/devices", methods=["GET"])
# def get_devices():
#     """Get list of connected devices"""
#     try:
#         logger.info("Requesting device list")
#         # Use real device list if available; otherwise fall back to mock
#         try:
#             devices: list[Device] = dmg.get_devices()
#         except Exception:
#             logger.warning("Falling back to mock device data for /api/devices")
#             devices = dmg.get_mock_data()
#         json_devices = [device.to_dict() for device in devices]

#         logger.info(f"Returning {len(json_devices)} devices")
#         return jsonify(
#             {
#                 "success": True,
#                 "data": json_devices,
#                 "devices": json_devices,
#                 "count": len(json_devices),
#             }
#         )

#     except (DeviceError, PlatformIOError) as e:
#         logger.error(f"Device error: {str(e)}")
#         return jsonify({"success": False, "error": str(e), "type": "device_error"}), 500

#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}")
#         return (
#             jsonify(
#                 {
#                     "success": False,
#                     "error": "Internal server error",
#                     "type": "server_error",
#                 }
#             ),
#             500,
#         )


# @api_bp.route("/api/save_program", methods=["POST"])
# def save_program():
#     return save_program_to_file(logger)


# @api_bp.route("/api/load_program/<program_name>")
# def load_program(program_name):
#     return load_program_from_file(logger, program_name)


# @api_bp.route("/api/list_programs")
# def list_programs():
#     return list_all_programs(logger)


# @api_bp.route("/api/health", methods=["GET"])
# def health_check():
#     """Health check endpoint"""
#     return jsonify(
#         {
#             "success": True,
#             "status": "healthy",
#             "message": "IoT Remote Lab server is running",
#         }
#     )


# @api_bp.route("/api/upload_firmware", methods=["POST"])
# def upload_firmware():
#     """Upload firmware to a device"""
#     import os

#     from flask import request

#     data = request.get_json()
#     device: dict[str, str] = data.get("device", {})
#     if not device or "port" not in device:
#         return (
#             jsonify(
#                 {
#                     "success": False,
#                     "error": "Device information with valid port is required",
#                     "type": "invalid_device",
#                 }
#             ),
#             400,
#         )

#     program_name: str = data.get("program_name")
#     port: str = device.get("port").strip()
#     print("device is", port)
#     device_obj = dmg.get_device_by_port(port.strip())
#     print("device obj is", device_obj, " ids", id(device_obj))

#     path = os.path.join(os.getcwd(), "programs", program_name)
#     if not os.path.exists(path):
#         return (
#             jsonify(
#                 {
#                     "success": False,
#                     "error": f"Program {program_name} does not exist",
#                     "type": "program_not_found",
#                 }
#             ),
#             404,
#         )
#     status, err = dmg.upload_firmware(device=device_obj, build_path=path, env="")
#     if err != "" or not status:
#         return (
#             jsonify(
#                 {
#                     "success": False,
#                     "error": err,
#                     "type": "upload_error",
#                 }
#             ),
#             500,
#         )
#     print(status, err)
#     print("path is", path)
#     return jsonify(
#         {
#             "success": status,
#             "message": f"Firmware upload {device} with program {program_name} initiated",
#         }
#     )


# # Serial Monitor API endpoints
# @api_bp.route("/api/serial/connect", methods=["POST"])
# def serial_connect():
#     """Connect to a device for serial monitoring"""
#     from flask import request

#     try:
#         data = request.get_json()
#         device_data = data.get("device")
#         baud_rate = data.get("baud_rate", 115200)

#         if not device_data:
#             return (
#                 jsonify({"success": False, "error": "Device information is required"}),
#                 400,
#             )

#         # Here you would implement actual serial connection logic
#         # For now, return a mock success response
#         logger.info(
#             f"Serial connect request for device: {device_data.get('name', 'Unknown')}"
#         )

#         return (
#             jsonify(
#                 {
#                     "success": True,
#                     "message": f"Connected to {device_data.get('name', 'device')}",
#                     "session_id": "mock_session_123",  # Generate actual session ID
#                 }
#             ),
#             200,
#         )

#     except Exception as e:
#         logger.error(f"Serial connect error: {str(e)}")
#         return jsonify({"success": False, "error": "Failed to connect to device"}), 500


# @api_bp.route("/api/serial/disconnect", methods=["POST"])
# def serial_disconnect():
#     """Disconnect from serial device"""
#     from flask import request

#     try:
#         data = request.get_json()
#         device_data = data.get("device")

#         logger.info(
#             f"Serial disconnect request for device: {device_data.get('name', 'Unknown') if device_data else 'Unknown'}"
#         )

#         # Here you would implement actual disconnection logic

#         return jsonify({"success": True, "message": "Disconnected from device"}), 200

#     except Exception as e:
#         logger.error(f"Serial disconnect error: {str(e)}")
#         return (
#             jsonify({"success": False, "error": "Failed to disconnect from device"}),
#             500,
#         )


# @api_bp.route("/api/serial/send", methods=["POST"])
# def serial_send():
#     """Send data to serial device"""
#     from flask import request

#     try:
#         data = request.get_json()
#         device_data = data.get("device")
#         serial_data = data.get("data")

#         if not serial_data:
#             return jsonify({"success": False, "error": "Data is required"}), 400

#         logger.info(f"Serial send request: {len(serial_data)} bytes")

#         # Here you would implement actual data sending logic

#         return jsonify({"success": True, "message": "Data sent successfully"}), 200

#     except Exception as e:
#         logger.error(f"Serial send error: {str(e)}")
#         return jsonify({"success": False, "error": "Failed to send data"}), 500


# @api_bp.route("/api/serial/baud_rate", methods=["POST"])
# def serial_baud_rate():
#     """Update baud rate for serial connection"""
#     from flask import request

#     try:
#         data = request.get_json()
#         device_data = data.get("device")
#         baud_rate = data.get("baud_rate")

#         if not baud_rate:
#             return jsonify({"success": False, "error": "Baud rate is required"}), 400

#         logger.info(f"Serial baud rate update request: {baud_rate}")

#         # Here you would implement actual baud rate update logic

#         return (
#             jsonify({"success": True, "message": f"Baud rate updated to {baud_rate}"}),
#             200,
#         )

#     except Exception as e:
#         logger.error(f"Serial baud rate error: {str(e)}")
#         return jsonify({"success": False, "error": "Failed to update baud rate"}), 500
