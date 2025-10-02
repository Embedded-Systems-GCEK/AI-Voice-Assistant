#!/usr/bin/env python3


import server

from ai_assistant import ai_singleton

if ai_singleton.is_initialized():
    assistant = ai_singleton.get_assistant()
else:
    ai_singleton.initialize_assistant(name="Minix")
    assistant = ai_singleton.get_assistant()

print(f"Starting server with AI Assistant: {assistant.name}")

server.app.run(
    host='0.0.0.0', 
    port=5000,
    debug=True,
    threaded=True,
    use_reloader=False
)
