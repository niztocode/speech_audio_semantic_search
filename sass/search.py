import json

import sass.extract.weaviate as we
import sass.process.frames as procfr

while True:
    query_text = input("Text query:  ")
    frames = we.get_similar_frames(query_text, limit=20)

    for frame in frames:
        frame_id = frame["_additional"]["id"]
        audio_clip = we.get_frame_clip(frame_id)
        frame["clip_title"] = audio_clip["title"]
    result = procfr.group_frames(frames)
    print()
    print(json.dumps(result, indent=4))
