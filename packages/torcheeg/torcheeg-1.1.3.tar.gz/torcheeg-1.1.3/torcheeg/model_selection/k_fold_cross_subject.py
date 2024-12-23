import logging
import os
import re
from copy import copy
from typing import Callable, Dict, Tuple, Union

import numpy as np
import pandas as pd
from sklearn import model_selection

from torcheeg.datasets.module.base_dataset import BaseDataset

from ..utils import get_random_dir_path

log = logging.getLogger('torcheeg')


class KFoldCrossSubject:
    r'''
    A tool class for k-fold cross-validations, to divide the training set and the test set. One of the most commonly used data partitioning methods, where the data set is divided into k subsets of subjects, with one subset subjects being retained as the test set and the remaining k-1 subset subjects being used as training data. In most of the literature, K is chosen as 5 or 10 according to the size of the data set.

    .. image:: _static/KFoldCrossSubject.png
        :alt: The schematic diagram of KFoldCrossSubject
        :align: center

    |

    .. code-block:: python

        from torcheeg.model_selection import KFoldCrossSubject
        from torcheeg.datasets import DEAPDataset
        from torcheeg import transforms
        from torcheeg.utils import DataLoader

        cv = KFoldCrossSubject(n_splits=5, shuffle=True)
        dataset = DEAPDataset(root_path='./data_preprocessed_python',
                              online_transform=transforms.Compose([
                                  transforms.To2d(),
                                  transforms.ToTensor()
                              ]),
                              label_transform=transforms.Compose([
                                  transforms.Select(['valence', 'arousal']),
                                  transforms.Binary(5.0),
                                  transforms.BinariesToCategory()
                              ]))

        for train_dataset, test_dataset in cv.split(dataset):
            train_loader = DataLoader(train_dataset)
            test_loader = DataLoader(test_dataset)
            ...

    Args:
        n_splits (int): Number of folds. Must be at least 2. (default: :obj:`5`)
        shuffle (bool): Whether to shuffle the data before splitting into batches. Note that samples within each split will not be shuffled. (default: :obj:`False`)
        label_transform (Callable, optional): Function that returns the stratified label for each sample. If set to None, it will not be stratified. (default: :obj:`None`)
        random_state (int, optional): When shuffle is :obj:`True`, :obj:`random_state` affects the ordering of the indices, which controls the randomness of each fold. If shuffle is :obj:`False`, this parameter has no effect. (default: :obj:`None`)
        split_path (str): Path to data partition information. If the path exists, the existing partition will be read from it. If the path does not exist, the current division method will be saved for future use. If set to None, a random path will be generated. (default: :obj:`None`)
    '''

    def __init__(self,
                 n_splits: int = 5,
                 shuffle: bool = False,
                 label_transform: Callable = None,
                 random_state: Union[None, int] = None,
                 split_path: Union[None, str] = None):
        if split_path is None:
            split_path = get_random_dir_path(dir_prefix='model_selection')

        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state
        self.split_path = split_path
        self.label_transform = label_transform

        if n_splits < 2:
            raise ValueError(
                f'Number of splits must be at least 2, but got {n_splits}.')

        if label_transform:
            self.k_fold = model_selection.StratifiedKFold(n_splits=n_splits,
                                                          shuffle=shuffle,
                                                          random_state=random_state)
        else:
            self.k_fold = model_selection.KFold(n_splits=n_splits,
                                                shuffle=shuffle,
                                                random_state=random_state)

    def split_info_constructor(self, info: pd.DataFrame) -> None:
        subject_ids = list(set(info['subject_id']))

        if self.label_transform:
            subject_labels = []
            for subject_id in subject_ids:
                subject_info = info[info['subject_id'] == subject_id]
                subject_label = subject_info.apply(
                    lambda info: self.label_transform(y=info.to_dict())['y'], axis=1).mean()
                subject_labels.append(subject_label)
            enumerater = enumerate(
                self.k_fold.split(subject_ids, subject_labels))
        else:
            enumerater = enumerate(self.k_fold.split(subject_ids))

        for fold_id, (train_index_subject_ids,
                      test_index_subject_ids) in enumerater:

            if len(train_index_subject_ids) == 0 or len(
                    test_index_subject_ids) == 0:
                raise ValueError(
                    f'The number of training or testing subjects is zero.')

            train_subject_ids = np.array(
                subject_ids)[train_index_subject_ids].tolist()
            test_subject_ids = np.array(
                subject_ids)[test_index_subject_ids].tolist()

            train_info = []
            for train_subject_id in train_subject_ids:
                train_info.append(info[info['subject_id'] == train_subject_id])
            train_info = pd.concat(train_info, ignore_index=True)

            test_info = []
            for test_subject_id in test_subject_ids:
                test_info.append(info[info['subject_id'] == test_subject_id])
            test_info = pd.concat(test_info, ignore_index=True)

            train_info.to_csv(os.path.join(self.split_path,
                                           f'train_fold_{fold_id}.csv'),
                              index=False)
            test_info.to_csv(os.path.join(self.split_path,
                                          f'test_fold_{fold_id}.csv'),
                             index=False)

    @property
    def fold_ids(self):
        indice_files = list(os.listdir(self.split_path))

        def indice_file_to_fold_id(indice_file):
            return int(re.findall(r'fold_(\d*).csv', indice_file)[0])

        fold_ids = list(set(map(indice_file_to_fold_id, indice_files)))
        fold_ids.sort()
        return fold_ids

    def split(self, dataset: BaseDataset) -> Tuple[BaseDataset, BaseDataset]:
        if not os.path.exists(self.split_path):
            log.info(
                f'📊 | Create the split of train and test set.'
            )
            log.info(
                f'😊 | Please set \033[92msplit_path\033[0m to \033[92m{self.split_path}\033[0m for the next run, if you want to use the same setting for the experiment.'
            )
            os.makedirs(self.split_path)
            self.split_info_constructor(dataset.info)
        else:
            log.info(
                f'📊 | Detected existing split of train and test set, use existing split from {self.split_path}.'
            )
            log.info(
                f'💡 | If the dataset is re-generated, you need to re-generate the split of the dataset instead of using the previous split.'
            )

        fold_ids = self.fold_ids

        for fold_id in fold_ids:
            train_info = pd.read_csv(
                os.path.join(self.split_path, f'train_fold_{fold_id}.csv'), low_memory=False)
            test_info = pd.read_csv(
                os.path.join(self.split_path, f'test_fold_{fold_id}.csv'), low_memory=False)

            train_dataset = copy(dataset)
            train_dataset.info = train_info

            test_dataset = copy(dataset)
            test_dataset.info = test_info

            yield train_dataset, test_dataset

    @property
    def repr_body(self) -> Dict:
        return {
            'n_splits': self.n_splits,
            'shuffle': self.shuffle,
            'random_state': self.random_state,
            'split_path': self.split_path
        }

    def __repr__(self) -> str:
        # init info
        format_string = self.__class__.__name__ + '('
        for i, (k, v) in enumerate(self.repr_body.items()):
            # line end
            if i:
                format_string += ', '
            # str param
            if isinstance(v, str):
                format_string += f"{k}='{v}'"
            else:
                format_string += f"{k}={v}"
        format_string += ')'
        return format_string
