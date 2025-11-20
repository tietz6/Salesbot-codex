
import time, random, functools

def retry(tries: int=3, base_delay: float=0.5, max_delay: float=5.0, jitter: float=0.2):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            last = None
            for i in range(tries):
                try:
                    return fn(*a, **kw)
                except Exception as e:
                    last = e
                    if i == tries-1:
                        raise
                    delay = min(max_delay, base_delay * (2**i))
                    if jitter:
                        delay += random.uniform(0, jitter)
                    time.sleep(delay)
            raise last
        return wrapper
    return deco
