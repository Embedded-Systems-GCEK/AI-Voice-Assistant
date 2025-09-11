# from flask import Flask, render_template
# import threading

# class UI:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.setup_routes()
#         self.run()

#     def setup_routes(self):
#         @self.app.route('/')
#         def index():
#             return render_template('index.html')
#         @self.app.route('/health')
#         def health_check():
#             return "OK", 200

#     def run(self, host='0.0.0.0', port=5000):
#         threading.Thread(target=lambda: self.app.run(host=host, port=port)).start()
        