from typing import List, Set
from scipy.sparse import csr_matrix
import numpy as np
from .collections import SortedSet

class FeatureStore:

    def __init__(self):
        self.user_features: SortedSet[str] = SortedSet()
        self.item_features: SortedSet[str] = SortedSet()
        self.user_feature_map: dict[int, List[int]] = {}
        self.item_feature_map: dict[int, List[int]] = {}

    def put_user_feature(self, user_id: int, user_tags: List[str]) -> None:
        """
        Add a list of user features to the user features set.
        Replace the existing user features if the user ID already exists.
        """
        user_feature_ids = []
        for tag in user_tags:
            tag_id = self.user_features.add(tag)
            if tag_id not in user_feature_ids:
                user_feature_ids.append(tag_id)
        self.user_feature_map[user_id] = user_feature_ids

    def put_item_feature(self, item_id: int, item_tags: List[str]) -> None:
        """
        Add a list of item features to the item features set.
        Replace the existing item features if the item ID already exists.
        """
        item_feature_ids = []
        for tag in item_tags:
            tag_id = self.item_features.add(tag)
            if tag_id not in item_feature_ids:
                item_feature_ids.append(tag_id)
        self.item_feature_map[item_id] = item_feature_ids

    def get_user_feature_repr(self, user_tags: List[str]) -> csr_matrix:
        """
        Returns:
            csr_matrix: User feature representation of shape (1, n_features)
        """
        user_feature_ids = []
        for tag in user_tags:
            tag_id = self.user_features.index(tag)
            if tag_id >= 0:
                user_feature_ids.append(tag_id)

        cols = np.array(user_feature_ids)
        rows = np.zeros(len(user_feature_ids))
        data = np.ones(len(user_feature_ids))
        return csr_matrix((data, (rows, cols)), shape=(1, len(self.user_features)))

    def get_item_feature_repr(self, item_tags: List[str]) -> csr_matrix:
        """
        Returns:
            csr_matrix: Item feature representation of shape (1, n_features)
        """
        item_feature_ids = []
        for tag in item_tags:
            tag_id = self.item_features.index(tag)
            if tag_id >= 0:
                item_feature_ids.append(tag_id)

        cols = np.array(item_feature_ids)
        rows = np.zeros(len(item_feature_ids))
        data = np.ones(len(item_feature_ids))
        return csr_matrix((data, (rows, cols)), shape=(1, len(self.item_features)))

    def build_user_features_matrix(self) -> csr_matrix:
        """
        Returns:
            csr_matrix: User features matrix of shape (n_users, n_features)
        """

        rows, cols, data = [], [], []

        for user_id, feature_ids in self.user_feature_map.items():
            for feature_id in feature_ids:
                rows.append(user_id)
                cols.append(feature_id)
                data.append(1)

        return csr_matrix((data, (rows, cols)), shape=(len(self.user_feature_map), len(self.user_features)))

    def build_item_features_matrix(self) -> csr_matrix:
        """
        Returns:
            csr_matrix: Item features matrix of shape (n_items, n_features)
        """

        rows, cols, data = [], [], []

        for item_id, feature_ids in self.item_feature_map.items():
            for feature_id in feature_ids:
                rows.append(item_id)
                cols.append(feature_id)
                data.append(1)

        return csr_matrix((data, (rows, cols)), shape=(len(self.item_feature_map), len(self.item_features)))
