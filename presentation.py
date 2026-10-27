import lc.part_history  # noqa: F401
import lc.part_step  # noqa: F401
import lc.part_build  # noqa: F401
import lc.part_knot  # noqa: F401
import lc.part_types  # noqa: F401
import lc.part_fp  # noqa: F401
import lc.part_why  # noqa: F401
from lc.registry import ORDER as _ORDER

PUBLISHED = []
for _cls in _ORDER:
    _exposed = type(_cls.__name__, (_cls,), {"__module__": __name__})
    globals()[_cls.__name__] = _exposed
    PUBLISHED.append(_exposed)

for _i, _cls in enumerate(PUBLISHED, 1):
    _cls.idx = _i
    _cls.total = len(PUBLISHED)

ORDER = PUBLISHED
