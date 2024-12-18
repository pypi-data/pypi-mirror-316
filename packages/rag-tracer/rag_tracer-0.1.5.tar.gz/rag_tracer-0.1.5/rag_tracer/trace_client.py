import threading

import requests


class TraceClient:
    _TEST_URL = "http://xyz.rag-workflow.test.ke.com/api/tracer"

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def publish(self, trace_data):
        thread = threading.Thread(target=self._send_request, args=(trace_data,))
        thread.start()

    def _send_request(self, trace_data):
        try:
            requests.post(f"{self._TEST_URL}/publish", json=trace_data)
        except Exception as e:
            print(f"Request failed: {e}")
