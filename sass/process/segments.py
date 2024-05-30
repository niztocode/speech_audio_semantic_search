from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from weaviate.collections.classes.internal import Object


def group_segments(segments: list["Object"]) -> dict[str, list["Object"]]:
    unique_clips = {
        c.references["belongsToAudioClip"].objects[0].properties["title"]
        for c in segments
    }
    grouped_results = {clip: [] for clip in unique_clips}
    for seg in segments:
        seg_title = seg.references["belongsToAudioClip"].objects[0].properties["title"]
        grouped_results[seg_title].append(seg)

    return grouped_results
