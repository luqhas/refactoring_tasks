import time

# Заглушки middleware

def send_http(req):
    return "response"

# Bit flags version

def execute_flags(req, flags):
    result = send_http(req)
    if flags & 0x01:
        result = result
    if flags & 0x02:
        result = result
    if flags & 0x04:
        result = result
    if flags & 0x08:
        result = result
    if flags & 0x10:
        result = result
    return result

# Decorator chain

class Null:
    def handle(self, req):
        return send_http(req)

class BaseMiddleware:
    def __init__(self, next_handler):
        self.next = next_handler

    def handle(self, req):
        return self.next.handle(req)

class M1(BaseMiddleware): pass
class M2(BaseMiddleware): pass
class M3(BaseMiddleware): pass
class M4(BaseMiddleware): pass
class M5(BaseMiddleware): pass


def build_chain():
    handler = Null()
    handler = M5(handler)
    handler = M4(handler)
    handler = M3(handler)
    handler = M2(handler)
    handler = M1(handler)
    return handler

# Benchmark

req = object()
iterations = 100000

# Bit flags benchmark
start = time.time()
for _ in range(iterations):
    execute_flags(req, 0b11111)
end = time.time()
flags_time = end - start

# Decorator benchmark
chain = build_chain()
start = time.time()
for _ in range(iterations):
    chain.handle(req)
end = time.time()
decorator_time = end - start

print("Bit flags time:", flags_time)
print("Decorator time:", decorator_time)
print("Overhead ratio:", decorator_time / flags_time)