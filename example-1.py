import ffmpeg
import psycopg2
from langchain.chains import SequentialChain
from langchain.tools import StructuredTool, Tool

# Step 1: Extract clip or image from video
def extract_clip(video_path, output_path, start_time, duration):
    ffmpeg.input(video_path, ss=start_time, t=duration).output(output_path).run()
    return {"file_path": output_path, "start_time": start_time, "duration": duration}

extract_tool = StructuredTool.from_function(func=extract_clip, name="extract_clip", description="Extract clip from video")


# Step 2: Insert metadata into PostgreSQL
def insert_metadata(file_path: str, file_type: str, timestamp: int, duration=None):
    conn = psycopg2.connect("dbname=your_database user=your_username password=your_password host=localhost")
    cur = conn.cursor()
    query = """
        INSERT INTO media_metadata (file_path, file_type, timestamp, duration)
        VALUES (%s, %s, %s, %s)
        """
    print(query)
    cur.execute(query, (file_path, file_type, timestamp, duration))
    conn.commit()
    cur.close()
    conn.close()
    return "Metadata inserted successfully"

insert_tool = StructuredTool.from_function(func=insert_metadata, name="insert_metadata", description="Insert metadata into PostgreSQL")

# Define LangChain tools for each step
# clip_tool = Tool.from_function(lambda params: create_video_clip(params["input_file"], params["output_file"], params["start_time"], params["duration"]))
# image_tool = Tool.from_function(lambda params: extract_image(params["input_file"], params["output_file"], params["timestamp"]))
# db_tool = Tool.from_function(lambda params: insert_metadata_to_db(params["file_path"], params["file_type"], params["timestamp"], params.get("duration")))


# Step 3: Create LangChain SequentialChain
# chain = SequentialChain(
#     chains=[extract_tool, insert_tool],
#     input_variables=["video_path", "output_path", "file_type", "start_time", "timestamp", "duration"]
# )

# Run the ffmpeg chain
response = extract_tool.invoke({
    "video_path": "movie.mp4",
    "output_path": "clip.mp4",
    "start_time": "00:00:05",
    "duration": 10
})

# Run the insert tool chain
response = insert_tool.invoke({
    "file_path": "clip.mp4",
    "file_type": "video",
    "timestamp": 5,  # Extract from 10 seconds
    "duration": 10
})

# # # Run the chain
# response = chain.invoke({
#     "video_path": "input.mp4",
#     "output_path": "clip.mp4",
#     "file_type": "video",
#     "start_time": "00:00:05",
#     "timestamp": 5,  # Extract from 10 seconds
#     "duration": 10
# })


print(response)