import glob
import json
import random
import os
import math

class FacebookTrainValGen(object):
    def __init__(self, metadata_dir_path, metadata_file_pattern, ranges_dict_file, images_directory,
        image_pattern, train_factor, train_output, val_output):
        """Creates facebook train val files generator

        Args:
            metadata_dir_path (string): Path to a directory where facebook metadata are stored.
            metadata_file_pattern (string): Facebook metadata file pattern.
            ranges_dict_file (string): Path to a file with popularity class scores.
            images_directory (string): Path to a directory where facebook images are stored.
            image_pattern (string): Facebook image file pattern.
            train_factor (float): Percentage of data which are used for training.
            train_output (string): Path to a file where train data informations will be saved.
            val_output (string): Path to a file where val data informations will be saved.

        """

        self.video_files = glob.glob(os.path.join(metadata_dir_path, metadata_file_pattern))
        """array

        Array of paths to facebook metadata files.
        """

        self.ranges_dict = {}
        with open(ranges_dict_file, 'r') as r_file:
            self.ranges_dict = json.load(r_file)
        """dictionary

        Dictionary with popularity class scores.
        """

        self.ranges_number = len(self.ranges_dict.values()[0])+1
        """integer

        The number of popularity classes.
        """

        self.images_directory = images_directory
        """string

        Path to a directory where facebook images are stored.
        """

        self.image_pattern = image_pattern
        """string

        Facebook image file pattern.
        """

        self.class_dict = [ None ] * self.ranges_number
        for x in xrange(self.ranges_number):
            self.class_dict[x] = []
        """array

        Array of arrays, each array in main array stores arrays of image paths, the index in
        main array refers to the popularity class.
        """

        self.train_factor = train_factor
        """float

        Percentage of data which are used for training.
        """

        self.train_list = []
        """array

        Array with training data.
        """

        self.val_list = []
        """array

        Array with validation data.
        """

        self.train_output = train_output
        """string

        Path to a file where train data informations will be saved.
        """

        self.val_output = val_output
        """string

        Path to a file where validation data informations will be saved.
        """


    def count_video_score(self, view_count, followers_count):
        """Counts score for a video.

        Args:
            view_count (integer): The total number of video's views.
            followers_count (integer): The total number of followers.
        Return:
            (float): Calculated score.

        """
        return math.log((float(view_count+1)) / followers_count, 2)


    def get_video_popul_class(self, date, score):
        """Gets popularity class for a video.

        Args:
            date (string): The date when the video was published.
            score (float): Video's score.
        Return:
            (integer): Popularity class of the video.

        """
        for idx in xrange(self.ranges_number-1):
            if score <= self.ranges_dict[date][idx]:
                return idx;
        return self.ranges_number-1


    def get_image_paths(self, video_id):
        """Gets paths for images from a video.

        Args:
            video_id (string): Id of the video to be analyzed.
        Return:
            (array): Array of image paths.

        """
        pattern_path = os.path.join(self.images_directory, video_id, '{}'.format(self.image_pattern))
        abs_images = glob.glob(pattern_path)
        images = []
        for img in abs_images:
            images.append(os.path.join(os.path.basename(os.path.dirname(img)), os.path.basename(img))) 
        return images


    def prepare_class_dictionary(self):
        """Prepares class directory.

        """
        for video_f in self.video_files:
            with open(video_f, 'r') as f:
                videos = json.load(f)
                for v in videos:
                    view_count = v['viewsCount']
                    followers_count = v['page_likes']
                    score = self.count_video_score(view_count, followers_count)
                    date = v['created_time']['date'][:len('yyyy-mm')]
                    label = self.get_video_popul_class(date, score)
                    images = self.get_image_paths(v['id'])
                    self.class_dict[label].append(images)


    def prepare_train_val_lists(self):
        """Prepares train val lists.

        """
        for label in xrange(self.ranges_number):
            random.shuffle(self.class_dict[label])
            split_index = int(self.train_factor * len(self.class_dict[label]));
            for i in xrange(split_index):
                for p in self.class_dict[label][i]:
                    self.train_list.append((p, label))
            for i in xrange(split_index, len(self.class_dict[label])):
                for p in self.class_dict[label][i]:
                    self.val_list.append((p, label))


    def prepare_train_val_files(self):
        """Prepares train and val files.

        """
        random.shuffle(self.train_list)
        random.shuffle(self.val_list)
        with open(self.train_output, 'w') as train_file:
            for path_label in self.train_list:
                train_file.write("%s %s\n" % (path_label[0], path_label[1]))
        with open(self.val_output, 'w') as val_file:
            for path_label in self.val_list:
                val_file.write("%s %s\n" % (path_label[0], path_label[1]))


    def start(self):
        """Starts generating files.

        """
        self.prepare_class_dictionary()
        self.prepare_train_val_lists()
        self.prepare_train_val_files()


if __name__ == '__main__':

    metadata_dir_path = ''
    metadata_file_pattern = ''
    ranges_dict_file = ''
    images_directory = ''
    image_pattern = ''
    train_factor = 0.8
    train_output = ''
    val_output = ''


    facebook_train_val_gen = FacebookTrainValGen(metadata_dir_path, metadata_file_pattern, ranges_dict_file, images_directory,image_pattern,
    train_factor, train_output, val_output)
    facebook_train_val_gen.start()
