library(rjson)

DEPTH = 1

video_directory = ''
video_files <- list.files(path = video_directory, pattern = '')

do_split <- function(scores, depth)
{
    if(depth == 1 || length(scores) < 2)
        return(c(median(scores)))
    
    med <- median(scores)
    left_scores <- scores[which(scores  < med)]
    right_scores <- scores[which(scores  >= med)]
    
    left_med <- do_split(left_scores, depth-1)
    right_med <- do_split(right_scores, depth-1)
    return(c(left_med, med, right_med))
}


views_count <- list()
for (vid_file in video_files)
{
    file_path <- file.path(video_directory, vid_file)
    json_videos <- fromJSON(file = file_path)
    for (video_info in json_videos)
    {
        key = substr(video_info$created_time_readable, 1, nchar('yyyy-mm'))
        viewCount_numerical = as.numeric(video_info$views_total)
        followersCount_numerical = as.numeric(video_info$user_likes)
        value = log2((viewCount_numerical+1) / followersCount_numerical)
        if (exists(key, where = views_count))
            views_count[[key]] <- c(views_count[[key]], value)
        else
            views_count[[key]] <- c(value)
    }
}


PROPER_LEN = 2^DEPTH - 1
is_ok = 0
keys <- c()
split_list <- list()
for (i in 1: length(views_count))
{
    split_values <- do_split(views_count[[i]], DEPTH)
    if(anyNA(split_values))
        next
    if(length(split_values) != PROPER_LEN)
        next
    is_ok = is_ok + 1
    split_list[[length(split_list)+1]] <- as.list(split_values)
    keys <- c(keys, names(views_count)[[i]])
}

names(split_list) <- keys

json_val <- toJSON(split_list)
write(json_val, paste('dailymotion_DEPTH_',DEPTH ,'.json', sep=''))

print(paste(is_ok, length(views_count), sep='/'))

