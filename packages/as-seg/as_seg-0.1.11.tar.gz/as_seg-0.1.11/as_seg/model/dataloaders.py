"""
This module contains the dataloaders for the main datasets in MSA: SALAMI, RWCPOP and Beatles dataset.

It loads the data, but also computes the barwise TF matrix and the bars from the audio files.
When the barwise TF matrix and bars are computed, they are saved in a cache folder to avoid recomputing them.
"""

import mirdata
import librosa
import as_seg.model.signal_to_spectrogram as signal_to_spectrogram
import pathlib
import shutil
import numpy as np
import warnings

import as_seg

eps = 1e-10

class BaseDataloader():
    def __init__(self, feature, cache_path = None, sr=44100, hop_length = 32, subdivision = 96, verbose = False):
        """
        Constructor of the BaseDataloader class.

        Parameters
        ----------
        feature : string
            The feature to compute the spectrogram. Must be a valid feature name.
        cache_path : string
            The path where to save the computed barwise TF matrices and bars. If None, the cache is not used.
            The default is None.
        sr : int
            The sampling rate of the audio files.
            The default is 44100.
        hop_length : int
            The hop length of the spectrogram.
            The default is 32.
        subdivision : int
            The number of subdivisions of a bar.
            The default is 96.
        verbose : bool
            If True, print some information about the cache.
            The default is False
        """
        self.cache_path = cache_path
        self.verbose = verbose

        self.feature_object = signal_to_spectrogram.FeatureObject(sr, feature, hop_length)

        # For barwise or beatwise processing
        self.subdivision = subdivision

    def __getitem__(self, index):
        """
        Return the data of the index-th track.
        """
        raise NotImplementedError("This method should be implemented in the child class") from None

    def __len__(self):
        """
        Return the number of tracks in the dataset.
        """
        raise NotImplementedError("This method should be implemented in the child class") from None

    def get_spectrogram(self, signal): # The spectrogram is not saved in the cache because it is too large in general
        """
        Returns the spectrogram, from the signal of a song.
        """
        return self.feature_object.get_spectrogram(signal)
    
    def get_bars(self, audio_path, index = None):
        """
        Return the bars of the song.
        They are computed from the audio file.
        If the cache is used, the bars are saved in the cache.
        An identifier of the song should be provided to save the bars in the cache.
        """
        def _compute_bars(): # Define the function to compute the bars
            return as_seg.data_manipulation.get_bars_from_audio(audio_path)

        # If a cache is set
        if self.cache_path is not None:

            # No identifier is provided for this song, hence it cannot be saved in the cache
            if index is None:
                warnings.warn("No index provided for the cache, the cache will be ignored")
            
            # An identifier is provided
            else:
                dir_save_bars_path = f"{self.cache_path}/bars"
                
                # Tries to load the bars from the cache
                try:
                    bars = np.load(f"{dir_save_bars_path}/{index}.npy", allow_pickle=True)
                    if self.verbose:
                        print("Using cached bars.")
                
                # If the file is not found, the bars are computed and saved in the cache
                except FileNotFoundError:
                    bars = _compute_bars() # Compute the bars

                    # Save the bars in the cache
                    pathlib.Path(dir_save_bars_path).mkdir(parents=True, exist_ok=True)
                    np.save(f"{dir_save_bars_path}/{index}.npy", bars)
                
                # Return the bars
                return bars
        # No cache is set, the bars are computed and returned
        return _compute_bars()

    def get_barwise_tf_matrix(self, track_path, bars, index = None):
        """
        Return the barwise TF matrix of the song.
        It is computed from the signal of the song and the bars.
        If the cache is used, the barwise TF matrix is saved in the cache.
        An identifier of the song should be provided to save the barwise TF matrix in the cache.
        """
        def _compute_barwise_tf_matrix(): # Define the function to compute the barwise TF matrix
            # Load the signal of the song
            sig, _ = librosa.load(track_path, sr=self.sr, mono=True) #torchaudio.load(track.audio_path)
            # Compute the spectrogram
            spectrogram = self.get_spectrogram(sig)
            return as_seg.barwise_input.barwise_TF_matrix(spectrogram, bars, self.hop_length/self.sr, self.subdivision) + eps
        
        # If a cache is set 
        if self.cache_path is not None:
            # No identifier is provided for this song, hence it cannot be saved in the cache
            if index is None:
                warnings.warn("No index provided for the cache, the cache will be ignored")
            
            # An identifier is provided
            else:
                cache_file_name = f"{index}_{self.feature}_subdiv{self.subdivision}"
                dir_save_barwise_tf_path = f"{self.cache_path}/barwise_tf_matrix"
                
                # Tries to load the barwise TF matrix from the cache
                try:
                    barwise_tf_matrix = np.load(f"{dir_save_barwise_tf_path}/{cache_file_name}.npy", allow_pickle=True)
                    if self.verbose:
                        print("Using cached Barwise TF matrix.")
                
                # If the file is not found, the barwise TF matrix is computed and saved in the cache
                except FileNotFoundError:
                    barwise_tf_matrix = _compute_barwise_tf_matrix() # Compute the barwise TF matrix

                    # Save the barwise TF matrix in the cache
                    pathlib.Path(dir_save_barwise_tf_path).mkdir(parents=True, exist_ok=True)
                    np.save(f"{dir_save_barwise_tf_path}/{cache_file_name}.npy", barwise_tf_matrix)
                
                # Return the barwise TF matrix
                return barwise_tf_matrix
            
        # No cache is set, the barwise TF matrix is computed and returned
        return _compute_barwise_tf_matrix()

    def save_segments(self, segments, name):
        """
        Save the segments of a song in the original folder.
        Important for reproducibility.
        """
        # mirdata_segments = mirdata.annotations.SectionData(intervals=segments, interval_unit="s")
        # jams_segments = mirdata.jams_utils.sections_to_jams(mirdata_segments)
        dir_save_path = f"{self.data_path}/estimations/segments/{self.dataset_name.lower()}"
        pathlib.Path(dir_save_path).mkdir(parents=True, exist_ok=True)
        np.save(f"{dir_save_path}/{name}.npy", segments)

    def score_flat_segmentation(self, segments, annotations):
        """
        Compute the score of a flat segmentation.
        """
        close_tolerance = as_seg.data_manipulation.compute_score_of_segmentation(annotations, segments, window_length=0.5)
        large_tolerance = as_seg.data_manipulation.compute_score_of_segmentation(annotations, segments, window_length=3)
        return close_tolerance, large_tolerance
    
    def segments_from_bar_to_seconds(self, segments, bars):
        """
        Convert the segments from bars to seconds. Wrapper for the function in data_manipulation.
        """
        # May be useful, if ever.
        return as_seg.data_manipulation.segments_from_bar_to_time(segments, bars)

class RWCPopDataloader(BaseDataloader):
    """
    Dataloader for the RWC Pop dataset.
    """
    def __init__(self, path, feature, cache_path = None, download=False, sr=44100, hop_length = 32, subdivision = 96):
        """
        Constructor of the RWCPopDataloader class.

        Parameters
        ----------
        Same then for BaseDataloader, with the addition of:

        path : string
            The path to the dataset.
        download : bool
            If True, download the dataset using mirdata.
            The default is False.
        """
        super().__init__(feature=feature, cache_path=cache_path, sr=sr, hop_length=hop_length, subdivision=subdivision)
        self.data_path = path
        rwcpop = mirdata.initialize('rwc_popular', data_home = path)
        if download:
            rwcpop.download()            
        self.all_tracks = rwcpop.load_tracks()
        self.indexes = rwcpop.track_ids

        self.dataset_name = "RWCPop"

    def __getitem__(self, index):
        """
        Return the data of the index-th track.
        """
        track_id = self.indexes[index]
        track = self.all_tracks[track_id]

        # Compute the bars
        bars = self.get_bars(track.audio_path, index=track_id)

        # Compute the barwise TF matrix
        barwise_tf_matrix = self.get_barwise_tf_matrix(track.audio_path, bars, index=track_id)

        # Get the annotationks
        annotations_intervals = track.sections.intervals

        # Return the the bars, the barwise TF matrix and the annotations
        return track_id, bars, barwise_tf_matrix, annotations_intervals
    
    def __len__(self):
        """
        Return the number of tracks in the dataset.
        """
        return len(self.indexes)
    
    def get_track_of_id(self, track_id):
        """
        Return the data of the track with the given track_id.
        """
        index = self.indexes.index(track_id)
        return self.__getitem__[index]
    
    def format_dataset(self, path_audio_files):
        """
        Format the dataset from the mirdata way of downloading information to the way of the dataloader.
        """
        # Copy audio files to the right location.
        # Suppose that the audio files are all in the same folder
        for track_num in range(len(self.all_tracks)):
            track_idx = self.indexes[track_num]
            song_file_name = self.all_tracks[track_idx].audio_path.split('/')[-1]
            src = f"{path_audio_files}/{song_file_name}" # May change depending on your file structure
            dest = self.all_tracks[track_idx].audio_path
            pathlib.Path(dest).parent.absolute().mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest)

class SALAMIDataloader(BaseDataloader):
    """
    Dataloader for the SALAMI dataset.
    """
    def __init__(self, path, feature, cache_path = None, download=False, subset = None, sr=44100, hop_length = 32, subdivision = 96):
        """
        Constructor of the SALAMIDataloader class.

        Parameters
        ----------  
        Same then for BaseDataloader, with the addition of:

        path : string
            The path to the dataset.
        download : bool
            If True, download the dataset using mirdata.
            The default is False.
        subset : string
            The subset of the dataset to use. Can be "train", "test" or "debug".
        """
        super().__init__(feature=feature, cache_path=cache_path, sr=sr, hop_length=hop_length, subdivision=subdivision)
        
        self.dataset_name = "SALAMI"

        self.data_path = path
        salami = mirdata.initialize('salami', data_home = path)
        if download:
            salami.download()            
        self.all_tracks = salami.load_tracks()
        self.indexes = salami.track_ids

        self.subset = subset
        if subset is not None:
            train_indexes, test_indexes = self.split_training_test()
            if subset == "train":
                self.indexes = train_indexes
            elif subset == "test":
                self.indexes = test_indexes
            elif subset == "debug":
                self.indexes = test_indexes[:4]
            else:
                raise ValueError("Subset should be either 'train' or 'test'")


    def __getitem__(self, index):
        """
        Return the data of the index-th track.
        """
        # Parsing through files ordered with self.indexes
        track_id = self.indexes[index]
        track = self.all_tracks[track_id]

        try:           
            # Compute the bars
            bars = self.get_bars(track.audio_path, index=track_id)

            # Compute the barwise TF matrix
            barwise_tf_matrix = self.get_barwise_tf_matrix(track.audio_path, bars, index=track_id)

            # Get the annotations
            dict_annotations = self.get_annotations(track)

            # Return the the bars, the barwise TF matrix and the annotations
            return track_id, bars, barwise_tf_matrix, dict_annotations
    
        except FileNotFoundError:
            print(f'{track_id} not found.')
            return track_id, None, None, None
            # raise FileNotFoundError(f"Song {track_id} not found, normal ?") from None
    
    def __len__(self):
        """
        Return the number of tracks in the dataset, and in particular the number of tracks in the subset.
        """
        # To handle the fact that indexes are updated with the subset
        return len(self.indexes)

    def get_track_of_id(self, track_id):
        """
        Return the data of the track with the given track_id.
        """
        try:
            index = self.indexes.index(track_id)
        except ValueError:
            try:
                index = self.indexes.index(str(track_id))
            except ValueError:
                raise ValueError(f"Track {track_id} not found in the dataset") from None
        return self.__getitem__(index)

    def get_annotations(self, track):
        """
        Return the annotations of the track, in the form of a dict.
        It returns the annotations of the first annotator, and if available, the annotations of the second annotator.
        It returns both levels of annotations (upper and lower) for each annotator.
        """
        dict_annotations = {}
        try: 
            # Trying to get the first annotator
            dict_annotations["upper_level_annotations"] = track.sections_annotator_1_uppercase.intervals
            dict_annotations["lower_level_annotations"] = track.sections_annotator_1_lowercase.intervals
            try: # Trying to load the second annotator
                dict_annotations["upper_level_annotations_2"] = track.sections_annotator_2_uppercase.intervals
                dict_annotations["lower_level_annotations_2"] = track.sections_annotator_2_lowercase.intervals
                dict_annotations["annot_number"]  = 2
            except AttributeError: # Only the first annotator was loaded
                dict_annotations["annot_number"]  = 1
        except AttributeError:
            try:
                # Trying to get the second annotator (no first one)
                dict_annotations["upper_level_annotations"] = track.sections_annotator_2_uppercase.intervals
                dict_annotations["lower_level_annotations"] = track.sections_annotator_2_lowercase.intervals
                dict_annotations["annot_number"]  = 1
            except AttributeError:
                raise AttributeError(f"No annotations found for {track.track_id}")
        
        return dict_annotations
    
    def get_this_set_annotations(self, dict_annotations, annotation_level = "upper", annotator = 1):
        """
        Return a particular set of annotations from all the annotations.
        """
        if annotator == 1:
            if annotation_level == "upper":
                annotations = dict_annotations["upper_level_annotations"]
            elif annotation_level == "lower":
                annotations = dict_annotations["lower_level_annotations"]
            else:
                raise ValueError("Invalid annotation level")
        elif annotator == 2:
            assert dict_annotations["annot_number"] == 2, "No second annotator found."
            if annotation_level == "upper":
                annotations = dict_annotations["upper_level_annotations"]
            elif annotation_level == "lower":
                annotations = dict_annotations["lower_level_annotations"]
            else:
                raise ValueError("Invalid annotation level")
        # elif annotator == "both":
        #     assert dict_annotations["annot_number"] == 2, "No second annotator found."
        #     annotations = dict_annotations["upper_level_annotations"] + dict_annotations["upper_level_annotations_2"]
        else:
            raise ValueError("Invalid annotator number")
        return annotations

    def split_training_test(self):
        """
        Split the dataset in training and test set.
        """
        indexes_train = []
        indexes_test = []
        for track_id in self.indexes:
            track = self.all_tracks[track_id]
            try:
                track.sections_annotator_1_uppercase.intervals
                track.sections_annotator_2_uppercase.intervals
                indexes_test.append(track_id)
            except AttributeError:
                indexes_train.append(track_id)
        return indexes_train, indexes_test
    
    def score_flat_segmentation(self, segments, dict_annotations, annotation_level = "upper", annotator = 1):
        """
        Score a flat segmentation.
        """
        if annotator == "both":
            assert dict_annotations["annot_number"] == 2, "No second annotator found."
            score_annot_1 = self.score_flat_segmentation(segments, dict_annotations, annotation_level = annotation_level, annotator = 1)
            score_annot_2 = self.score_flat_segmentation(segments, dict_annotations, annotation_level = annotation_level, annotator = 2)
            return score_annot_1, score_annot_2
        
        annotations = self.get_this_set_annotations(dict_annotations, annotation_level = annotation_level, annotator = annotator)
        return super().score_flat_segmentation(segments, annotations)
        
    def score_flat_segmentation_twolevel(self, segments_upper_level, segments_lower_level, dict_annotations, annotator = 1):
        """
        Score a flat segmentation at both levels of annotations.
        """
        score_upper_level = self.score_flat_segmentation(segments_upper_level, dict_annotations, annotation_level = "upper", annotator = annotator)
        score_lower_level = self.score_flat_segmentation(segments_lower_level, dict_annotations, annotation_level = "lower", annotator = annotator)
        return score_upper_level, score_lower_level
    
    def score_flat_segmentation_twolevel_best_of_several(self, list_segments_upper_level, list_segments_lower_level, dict_annotations, annotator = 1):
        """
        Score a flat segmentation at both levels of annotations, and return the best score from the different annotators.
        """
        assert annotator != "both", "Not implemented yet"
        stack_upper_scores = -np.inf * np.ones((len(list_segments_upper_level),2,3))
        for idx, segments in enumerate(list_segments_upper_level):
            stack_upper_scores[idx] = self.score_flat_segmentation(segments, dict_annotations, annotation_level = "upper", annotator = annotator)
        idx_close = np.argmax(stack_upper_scores[:,0,2]) # Selecting best f measure at 0.5s
        idx_large = np.argmax(stack_upper_scores[:,1,2]) # Selecting best f measure at 3s
        score_upper_level = (stack_upper_scores[idx_close,0,:], stack_upper_scores[idx_large,1,:])

        stack_lower_scores = -np.inf * np.ones((len(list_segments_lower_level),2,3))
        for idx, segments in enumerate(list_segments_lower_level):
            stack_lower_scores[idx] = self.score_flat_segmentation(segments, dict_annotations, annotation_level = "lower", annotator = annotator)
        idx_close = np.argmax(stack_lower_scores[:,0,2]) # Selecting best f measure at 0.5s
        idx_large = np.argmax(stack_lower_scores[:,1,2]) # Selecting best f measure at 3s
        score_lower_level = (stack_lower_scores[idx_close,0,:], stack_lower_scores[idx_large,1,:])

        return score_upper_level, score_lower_level

    def get_sizes_of_annotated_segments(self, annotation_level = "upper", annotator = 1, plot = False):
        """
        Return the lengths of the annotated segments.
        """
        lengths = []
        for track_id in self.indexes:
            track = self.all_tracks[track_id]

            try:           
                # Compute the bars
                bars = self.get_bars(track.audio_path, index=track_id)

                # Get the annotations
                dict_annotations = self.get_annotations(track)

                annotations = self.get_this_set_annotations(dict_annotations, annotation_level = annotation_level, annotator = annotator)

                barwise_annot = as_seg.data_manipulation.frontiers_from_time_to_bar(np.array(annotations)[:,1], bars) # Convert the annotations from time to bar
                for i in range(len(barwise_annot) - 1):
                    lengths.append(barwise_annot[i+1] - barwise_annot[i]) # Store the length of the annotated segment
        
            except FileNotFoundError:
                print(f'{track_id} not found.')
                # raise FileNotFoundError(f"Song {track_id} not found, normal ?") from None

        if plot:
            as_seg.model.common_plot.plot_lenghts_hist(lengths)
        return lengths
        
    # def format_dataset(self, path_audio_files): # TODO
        # # Copy audio files to the right location.
        # # Suppose that the audio files are all in the same folder
        # for track_num in range(len(self.all_tracks)):
        #     track_idx = self.indexes[track_num]
        #     song_file_name = self.all_tracks[track_idx].audio_path.split('/')[-1]
        #     src = f"{path_audio_files}/{song_file_name}" # May change depending on your file structure
        #     dest = self.all_tracks[track_idx].audio_path
        #     pathlib.Path(dest).parent.absolute().mkdir(parents=True, exist_ok=True)
        #     shutil.copy(src, dest)
    

class BeatlesDataloader(BaseDataloader):
    """
    Dataloader for the Beatles dataset.
    """
    def __init__(self, path, feature, cache_path = None, download=False, sr=44100, hop_length = 32, subdivision = 96):
        """
        Constructor of the BeatlesDataloader class.

        Parameters
        ----------
        Same then for BaseDataloader, with the addition of:

        path : string
            The path to the dataset.
        download : bool
            If True, download the dataset using mirdata.
            The default is False
        """
        super().__init__(feature, cache_path, sr, hop_length, subdivision)
        self.data_path = path
        beatles = mirdata.initialize('beatles', data_home = path)
        if download:
            beatles.download()            
        self.all_tracks = beatles.load_tracks()
        self.indexes = beatles.track_ids

        self.dataset_name = "Beatles"

    def __getitem__(self, index):
        """
        Return the data of the index-th track.
        """
        track_id = self.indexes[index]
        track = self.all_tracks[track_id]

        # Compute the bars
        bars = self.get_bars(track.audio_path, index=track_id)

        # Compute the barwise TF matrix
        barwise_tf_matrix = self.get_barwise_tf_matrix(track.audio_path, bars, index=track_id)

        # Get the annotationks
        annotations_intervals = track.sections.intervals

        # Return the the bars, the barwise TF matrix and the annotations
        return track_id, bars, barwise_tf_matrix, annotations_intervals
    
    def __len__(self):
        """
        Return the number of tracks in the dataset.
        """
        return len(self.all_tracks)
    
    def get_track_of_id(self, track_id):
        """
        Return the data of the track with the given track_id.
        """
        try:
            index = self.indexes.index(track_id)
        except ValueError:
            try:
                index = self.indexes.index(str(track_id))
            except ValueError:
                raise ValueError(f"Track {track_id} not found in the dataset") from None
        return self.__getitem__(index)

if __name__ == "__main__":
    # rwcpop = RWCPopDataloader('/home/a23marmo/datasets/rwcpop', feature = "mel", cache_path = "/home/a23marmo/Bureau/data_persisted/rwcpop")
    # # rwcpop.format_dataset('/home/a23marmo/Bureau/Audio samples/rwcpop/Entire RWC')
    # for spectrogram, bars, barwise_tf_matrix, track_id, annotations in rwcpop:
    #     print(spectrogram.shape, track_id)

    salami = SALAMIDataloader('/home/a23marmo/datasets/salami', feature = "mel", cache_path = "/home/a23marmo/Bureau/data_persisted/salami", subset = "train")

    for spectrogram, bars, barwise_tf_matrix, track_id, annotations in salami:
        try:
            print(track_id)
        except FileNotFoundError:
            print(f'{track_id} not found.')
