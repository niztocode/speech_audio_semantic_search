from typing import Any, Dict, List


def unique_in_order(seq: List):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def group_frames(frames: List[Dict[str, Any]]) -> Dict[str, Any]:
    unique_titles = unique_in_order([f["clip_title"] for f in frames])
    grouped_frames = {}
    for t in unique_titles:
        clip_frames = [f for f in frames if f["clip_title"] == t]
        sorted_clip_frames = sorted(clip_frames, key=lambda x: x["start"])
        grouped_frames[t] = sorted_clip_frames
    return grouped_frames
