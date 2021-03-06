library(argparse)
library(rjson)
parser <- ArgumentParser(description = 'Histogram creator for vimeo')
parser$add_argument('--date', help = 'Year and month, format: yyyy-mm(,yyyy-mm,...)', required = T)
parser$add_argument('--directory', help = 'Path to directory with vimeo data', required = T)
parser$add_argument('--video_pattern', help = 'Pattern for JSON file with videos data', required = T)
args <- parser$parse_args()

r_path <- dirname(getwd())
dir.create(file.path(r_path, 'results'), showWarnings = FALSE)

video_files <- list.files(path = args$directory, pattern = args$video_pattern)

dates <- strsplit(args$date, ',')[[1]]

views_count <- vector()
channel_likes <- vector()
total_videos <- 0

for (vid_file in video_files)
{
    file_path <- file.path(args$directory, vid_file)
    json_videos <- fromJSON(file = file_path)
    for (video_info in json_videos)
    {
        video_date <- substr(video_info$created_time, 1, nchar('yyyy-mm'))
        if (any(dates == video_date))
        {
            views_count <- c(views_count, video_info$stats$plays)
            channel_likes <- c(channel_likes, video_info$channel_likes)
            total_videos <- total_videos + 1
        }
    }
}

points <- (views_count+1) / channel_likes
norm_points <- log2(points)

wd = getwd()
setwd(file.path(r_path, 'results'))
png(filename = paste('v_', gsub(',', '_', args$date), '_', total_videos, '_views.png', sep = ''))
hist(norm_points, breaks = 50)
dev.off()
setwd(wd)

