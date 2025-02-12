import ffmpeg
import psycopg2
import os
from langchain.chains import SequentialChain
from langchain.tools import Tool

# Database connection setup
DB_CONFIG = {
    "dbname": "your_database",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432",
}

# Function to create a video clip using ffmpeg
def create_video_clip(input_file: str, output_file: str, start_time: int, duration: int):
    try:
        ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file).run(overwrite_output=True)
        return {"output_file": output_file, "start_time": start_time, "duration": duration}
    except Exception as e:
        return {"error": str(e)}

# Function to extract an image from a video
def extract_image(input_file: str, output_file: str, timestamp: int):
    try:
        ffmpeg.input(input_file, ss=timestamp).output(output_file, vframes=1).run(overwrite_output=True)
        return {"output_file": output_file, "timestamp": timestamp}
    except Exception as e:
        return {"error": str(e)}

# Function to insert metadata into PostgreSQL
def insert_metadata_to_db(file_path: str, file_type: str, timestamp: int, duration=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO media_metadata (file_path, file_type, timestamp, duration)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (file_path, file_type, timestamp, duration))
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        return {"error": str(e)}

# Define LangChain tools for each step
clip_tool = Tool.from_function(lambda params: create_video_clip(params["input_file"], params["output_file"], params["start_time"], params["duration"]))
image_tool = Tool.from_function(lambda params: extract_image(params["input_file"], params["output_file"], params["timestamp"]))
db_tool = Tool.from_function(lambda params: insert_metadata_to_db(params["file_path"], params["file_type"], params["timestamp"], params.get("duration")))

# Define LangChain SequentialChain
chain = SequentialChain(
    chains=[clip_tool, db_tool],  # Chain tools (Clip → DB Entry)
    input_variables=["input_file", "output_file", "start_time", "duration"]
)

# Example Usage for Video Clip
video_params = {
    "input_file": "input.mp4",
    "output_file": "output_clip.mp4",
    "start_time": 10,  # Extract from 10 seconds
    "duration": 5  # 5-second clip
}

response = chain.invoke(video_params)
print(response)

# Example Usage for Image Extraction
image_chain = SequentialChain(
    chains=[image_tool, db_tool],  # Chain tools (Image → DB Entry)
    input_variables=["input_file", "output_file", "timestamp"]
)

image_params = {
    "input_file": "input.mp4",
    "output_file": "output_image.jpg",
    "timestamp": 15  # Extract frame at 15 seconds
}

response = image_chain.invoke(image_params)
print(response)
