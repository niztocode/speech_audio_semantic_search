import sass.extract.weaviate as we
import sass.process.segments as process

while True:
    query_text = input("Text query:  ")

    segments = we.get_similar_segments(query_text, limit=20)

    unique_audiclips = process.group_segments(segments.objects)
    for title, seg_objs in unique_audiclips.items():
        print(f"Clip title: {title}")
        for seg in seg_objs:
            print(f" Distance: {seg.metadata.distance} Segment: {seg.properties}")
