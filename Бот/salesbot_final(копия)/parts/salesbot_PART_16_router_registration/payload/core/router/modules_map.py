
MODULES_MAP = {
    "exam_autocheck": {"preferred": "modules.exam_autocheck.v1.routes", "fallbacks": []},
    "errors_manager": {"preferred": "modules.errors_manager.v1.routes", "fallbacks": []},
    "arena": {"preferred": "modules.arena.v3.routes", "fallbacks": ["modules.arena.v2.routes","modules.arena.v1.routes"]},
    "sleeping_dragon": {"preferred": "modules.sleeping_dragon.v3.routes", "fallbacks": ["modules.sleeping_dragon.v2.routes"]},
}
