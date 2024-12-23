import logging
import os
import re
from copy import copy
from typing import Dict, List, Tuple, Union

import pandas as pd
from sklearn import model_selection

from torcheeg.datasets.module.base_dataset import BaseDataset

from ..utils import get_random_dir_path

log = logging.getLogger('torcheeg')


class KFoldPerSubjectGroupbyTrial:
    r'''
    A tool class for k-fold cross-validations, to divide the training set and the test set, commonly used to study model performance in the case of subject dependent experiments. Experiments were performed separately for each subject, where the data for all trials of the subject is divided into k subsets at the trial dimension, with one subset being retained as the test set and the remaining k-1 being used as training data. In most of the literature, K is chosen as 5 or 10 according to the size of the data set.

    .. image:: _static/KFoldPerSubjectGroupbyTrial.png
        :alt: The schematic diagram of KFoldPerSubjectGroupbyTrial
        :align: center

    |

    .. code-block:: python

        from torcheeg.model_selection import KFoldPerSubjectGroupbyTrial
        from torcheeg.datasets import DEAPDataset
        from torcheeg import transforms
        from torcheeg.utils import DataLoader

        cv = KFoldPerSubjectGroupbyTrial(n_splits=5, shuffle=True)
        dataset = DEAPDataset(root_path='./data_preprocessed_python',
                              online_transform=transforms.Compose([
                                  transforms.ToTensor(),
                                  transforms.To2d()
                              ]),
                              label_transform=transforms.Compose([
                                  transforms.Select(['valence', 'arousal']),
                                  transforms.Binary(5.0),
                                  transforms.BinariesToCategory()
                              ]))

        for train_dataset, test_dataset in cv.split(dataset):
            # The total number of experiments is the number subjects multiplied by K
            train_loader = DataLoader(train_dataset)
            test_loader = DataLoader(test_dataset)
            ...
    
    :obj:`KFoldPerSubjectGroupbyTrial` allows the user to specify the index of the subject of interest, when the user need to report the performance on each subject.

    .. code-block:: python

        from torcheeg.model_selection import KFoldPerSubjectGroupbyTrial
        from torcheeg.datasets import DEAPDataset
        from torcheeg import transforms
        from torcheeg.utils import DataLoader

        cv = KFoldPerSubjectGroupbyTrial(n_splits=5, shuffle=True)
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

        for train_dataset, test_dataset in cv.split(dataset, subject=1):
            # k-fold cross-validation for subject 1
            train_loader = DataLoader(train_dataset)
            test_loader = DataLoader(test_dataset)
            ...

    Args:
        n_splits (int): Number of folds. Must be at least 2. (default: :obj:`5`)
        shuffle (bool): Whether to shuffle the data before splitting into batches. Note that the samples within each split will not be shuffled. (default: :obj:`False`)
        random_state (int, optional): When shuffle is :obj:`True`, :obj:`random_state` affects the ordering of the indices, which controls the randomness of each fold. Otherwise, this parameter has no effect. (default: :obj:`None`)
        split_path (str): The path to data partition information. If the path exists, read the existing partition from the path. If the path does not exist, the current division method will be saved for next use. If set to None, a random path will be generated. (default: :obj:`None`)
    '''

    def __init__(self,
                 n_splits: int = 5,
                 shuffle: bool = False,
                 random_state: Union[float, None] = None,
                 split_path: Union[None, str] = None):
        if split_path is None:
            split_path = get_random_dir_path(dir_prefix='model_selection')

        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state
        self.split_path = split_path

        self.k_fold = model_selection.KFold(n_splits=n_splits,
                                            shuffle=shuffle,
                                            random_state=random_state)

    def split_info_constructor(self, info: pd.DataFrame) -> None:
        subjects = list(set(info['subject_id']))
        for subject in subjects:
            subject_info = info[info['subject_id'] == subject]

            subject_train_infos = {}
            subject_test_infos = {}

            trial_ids = list(set(subject_info['trial_id']))
            for trial_id in trial_ids:
                trial_info = subject_info[subject_info['trial_id'] == trial_id]

                for i, (train_index,
                        test_index) in enumerate(self.k_fold.split(trial_info)):
                    train_info = trial_info.iloc[train_index]
                    test_info = trial_info.iloc[test_index]

                    if not i in subject_train_infos:
                        subject_train_infos[i] = []

                    if not i in subject_test_infos:
                        subject_test_infos[i] = []

                    subject_train_infos[i].append(train_info)
                    subject_test_infos[i].append(test_info)

            for i in subject_train_infos.keys():
                subject_train_info = pd.concat(subject_train_infos[i],
                                               ignore_index=True)
                subject_test_info = pd.concat(subject_test_infos[i],
                                              ignore_index=True)
                subject_train_info.to_csv(os.path.join(
                    self.split_path, f'train_subject_{subject}_fold_{i}.csv'),
                                          index=False)
                subject_test_info.to_csv(os.path.join(
                    self.split_path, f'test_subject_{subject}_fold_{i}.csv'),
                                         index=False)

    @property
    def subjects(self) -> List:
        indice_files = list(os.listdir(self.split_path))

        def indice_file_to_subject(indice_file):
            return re.findall(r'subject_(.*)_fold_(\d*).csv', indice_file)[0][0]

        subjects = list(set(map(indice_file_to_subject, indice_files)))
        subjects.sort()
        return subjects

    @property
    def fold_ids(self) -> List:
        indice_files = list(os.listdir(self.split_path))

        def indice_file_to_fold_id(indice_file):
            return int(
                re.findall(r'subject_(.*)_fold_(\d*).csv', indice_file)[0][1])

        fold_ids = list(set(map(indice_file_to_fold_id, indice_files)))
        fold_ids.sort()
        return fold_ids

    def split(
            self,
            dataset: BaseDataset,
            subject: Union[int,
                           None] = None) -> Tuple[BaseDataset, BaseDataset]:
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

        subjects = self.subjects
        fold_ids = self.fold_ids

        if not subject is None:
            assert subject in subjects, f'The subject should be in the subject list {subjects}.'

        for local_subject in subjects:
            if (not subject is None) and (local_subject != subject):
                continue

            for fold_id in fold_ids:
                train_info = pd.read_csv(
                    os.path.join(
                        self.split_path,
                        f'train_subject_{local_subject}_fold_{fold_id}.csv'))
                test_info = pd.read_csv(
                    os.path.join(
                        self.split_path,
                        f'test_subject_{local_subject}_fold_{fold_id}.csv'))

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