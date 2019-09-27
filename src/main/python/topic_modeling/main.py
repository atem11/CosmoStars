import json
import os

from com.expleague.media_space.topics.params import ProcessingParams
from com.expleague.media_space.topics.processing_manager import ProcessingManager
from com.expleague.media_space.topics.state_handler import InMemStateHandler


def main():
    embedding_file_path = os.getenv('EMBEDDING_FILE_PATH', 'lenta.vec')
    idf_file_path = os.getenv('IDF_FILE_PATH', 'idf.txt')
    cluster_centroids_file_path = os.getenv('CLUSTER_CENTROIDS_FILE_PATH', 'cluster_centroids.txt')
    cluster_names_file_path = os.getenv('CLUSTER_NAMES_FILE_PATH', 'cluster_names.txt')
    topics_matching_file_path = os.getenv('TOPICS_MATCHING_FILE_PATH', 'topics_matching.txt')
    min_sentence_len = int(os.getenv('MIN_SENTENCE_LEN', 3))
    topic_cos_threshold = float(os.getenv('TOPIC_COS_THRESHOLD', 0.5))
    news_clustering_threshold = float(os.getenv('NEWS_CLUSTERING_THRESHOLD', 0.025))
    news_clustering_min_cluster_size = int(os.getenv('NEWS_CLUSTERING_MIN_CLUSTER_SIZE', 2))
    stories_clustering_threshold = float(os.getenv('STORIES_CLUSTERING_THRESHOLD', 0.25))
    stories_clustering_min_cluster_size = int(os.getenv('STORIES_CLUSTERING_MIN_CLUSTER_SIZE', 2))
    ngrams_for_topics_labelling = int(os.getenv('NGRAMS_FOR_TOPICS_LABELLING', 3))
    stories_connecting_cos_threshold = float(os.getenv('STORIES_CONNECTING_COS_THRESHOLD', 0.9))
    story_window = int(os.getenv('STORY_WINDOW', 3))
    lexic_result_word_num = int(os.getenv('LEXIC_RESULT_WORD_NUM', 10))

    params = ProcessingParams(embedding_file_path, idf_file_path, cluster_centroids_file_path,
                              cluster_names_file_path, topics_matching_file_path, min_sentence_len,
                              topic_cos_threshold,
                              news_clustering_threshold,
                              news_clustering_min_cluster_size, stories_clustering_threshold,
                              stories_clustering_min_cluster_size, ngrams_for_topics_labelling,
                              stories_connecting_cos_threshold, story_window, lexic_result_word_num)

    state_handler = InMemStateHandler(params.story_window, params.stories_connecting_cos_threshold)
    processing_manager = ProcessingManager(params, state_handler)

    with open('data.txt') as json_file:
        data = json.load(json_file)


if __name__ == "__main__":
    main()
