
The router loader can be used from startup.py:
    from core.router.loader import try_include
    loaded = try_include(app)
    print("[router.loader] included:", loaded)
