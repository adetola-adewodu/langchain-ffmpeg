create table media_metadata (
   id         serial primary key,
   file_path  text not null,         -- Path of the generated file (clip or image)
   file_type  varchar(20) not null,  -- 'video_clip' or 'image'
   timestamp  int not null,          -- Start time (for clips) or extraction time (for images) in seconds
   duration   int null,               -- Duration of the video clip (NULL for images)
   created_at timestamp default current_timestamp -- Timestamp of entry creation
);


insert into media_metadata (
   file_path,
   file_type,
   timestamp,
   duration
) values ( 'output_clip.mp4',
           'video_clip',
           10,
           5 );

insert into media_metadata (
   file_path,
   file_type,
   timestamp,
   duration
) values ( 'output_image.jpg',
           'image',
           15,
           null );