import re


class PatchContext:
    """Applies non-fatal anchored text transforms and records pass/fail per anchor."""

    def __init__(self, src: str):
        self.src = src
        self.module = "unknown"
        self.records = []

    def set_module(self, name: str):
        self.module = name

    def _record(self, label: str, ok: bool, detail: str = ""):
        self.records.append(
            {"module": self.module, "label": label, "ok": ok, "detail": detail}
        )

    def prepend(self, prefix: str, label: str = "prepend"):
        self.src = prefix + self.src
        self._record(label, True)

    def replace_exact(self, old: str, new: str, label: str):
        if old not in self.src:
            self._record(label, False, f"missing anchor: {old[:90]!r}")
            return False
        self.src = self.src.replace(old, new, 1)
        self._record(label, True)
        return True

    def replace_all(self, old: str, new: str, label: str, min_count: int = 0):
        cnt = self.src.count(old)
        if cnt < min_count:
            self._record(label, False, f"expected >= {min_count}, found {cnt} for {old[:60]!r}")
            return False
        self.src = self.src.replace(old, new)
        self._record(label, True, f"count={cnt}")
        return True

    def replace_span(
        self,
        start_anchor: str,
        end_anchor: str,
        new_block: str,
        label: str,
        include_end: bool = False,
    ):
        i = self.src.find(start_anchor)
        if i == -1:
            self._record(label, False, f"missing start anchor: {start_anchor!r}")
            return False
        j = self.src.find(end_anchor, i + len(start_anchor))
        if j == -1:
            self._record(label, False, f"missing end anchor: {end_anchor!r}")
            return False
        if include_end:
            j += len(end_anchor)
        self.src = self.src[:i] + new_block + self.src[j:]
        self._record(label, True)
        return True

    def sub_regex(self, pattern: str, repl: str, label: str, expected_count: int | None = None):
        new_src, count = re.subn(pattern, repl, self.src)
        if expected_count is not None and count != expected_count:
            self._record(
                label,
                False,
                f"regex count mismatch: expected {expected_count}, got {count} ({pattern!r})",
            )
            return False
        self.src = new_src
        self._record(label, True, f"count={count}")
        return True

    def failures(self):
        return [r for r in self.records if not r["ok"]]
