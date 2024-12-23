import unittest

import numpy as np
import torch

from torcheeg.datasets.constants import DEAP_CHANNEL_LOCATION_DICT
from torcheeg.transforms import (BandDifferentialEntropy, BaselineCorrection,
                                 BaselineRemoval, Binary, Compose, Lambda,
                                 MeanStdNormalize, RandomMask, RandomNoise,
                                 Resize, Select, ToGrid, ToTensor)


class TestAnyTransforms(unittest.TestCase):
    def test_to_baseline_removal(self):
        transform = Compose([
            ToTensor(apply_to_baseline=True),
            Resize(size=(64, 64), apply_to_baseline=True),
            RandomNoise(p=0.1),
            RandomMask(p=0.1),
            BaselineRemoval()
        ])
        transformed_eeg = transform(eeg=np.random.randn(128, 9, 9),
                                    baseline=np.random.randn(128, 9, 9))['eeg']
        self.assertEqual(tuple(transformed_eeg.shape), (128, 64, 64))

        eeg = np.random.randn(128, 9, 9)
        transform = BaselineRemoval()
        transformed_eeg = transform(eeg=eeg, baseline=np.ones(
            (128, 9, 9)))['eeg']
        self.assertTrue(np.abs(eeg - (transformed_eeg + 1.0)).sum() < 1e-6)
        
        transform = BaselineRemoval()
        transformed_eeg = transform(eeg=eeg)['eeg']
        self.assertTrue(np.abs(eeg - transformed_eeg).sum() < 1e-6)

    def test_lambda(self):
        # label
        transform = Lambda(lambd=lambda x: x + 1)
        self.assertEqual(transform(y=1)['y'], 2)
        # torch
        transform = Lambda(targets=['eeg'], lambd=lambda x: x + 1)
        self.assertEqual(
            tuple(transform(eeg=torch.randn(32, 128))['eeg'].shape), (32, 128))
        # numpy
        self.assertEqual(
            transform(eeg=np.random.randn(32, 128))['eeg'].shape, (32, 128))

    def test_compose(self):
        # torch
        transform = Compose([
            ToTensor(),
            Resize(size=(64, 64)),
            RandomNoise(p=0.1),
            RandomMask(p=0.1)
        ])

        self.assertEqual(
            tuple(transform(eeg=np.random.randn(128, 9, 9))['eeg'].shape),
            (128, 64, 64))

        # numpy
        transform = Compose([
            BandDifferentialEntropy(),
            MeanStdNormalize(),
            ToGrid(DEAP_CHANNEL_LOCATION_DICT)
        ])
        self.assertEqual(
            tuple(transform(eeg=np.random.randn(32, 128))['eeg'].shape),
            (4, 9, 9))

        # label
        info = {'valence': 4.5, 'arousal': 5.5, 'subject_id': 7}
        transform = Compose([Select(key='valence'), Binary(threshold=5.0)])
        self.assertEqual(transform(y=info)['y'], 0)
    
    def test_baseline_correction(self):
        #torch
        transform = Compose([
            ToTensor(apply_to_baseline=True),
            Resize(size=(64, 64), apply_to_baseline=True),
            RandomNoise(p=0.1),
            RandomMask(p=0.1),
            BaselineCorrection()
        ])
        transformed_eeg,transformed_baseline = transform(eeg= np.random.randn(128, 9, 9),
                                    baseline= np.random.randn(128, 9, 9)).values()
        self.assertEqual(tuple(transformed_eeg.shape), (128, 64, 64))
        self.assertEqual(tuple(transformed_baseline.shape), (128, 64, 64))
        
        #numpy
        eeg = np.random.randn(128, 9, 9)
        transform = BaselineCorrection()
        transformed_eeg = transform(eeg=eeg, baseline=np.ones(
            (128, 9, 9)))['eeg']
        self.assertTrue(np.abs(eeg - (transformed_eeg + 1.0)).sum() < 1e-6)
        
        transform = BaselineCorrection()
        transformed_eeg = transform(eeg=eeg)['eeg']
        self.assertTrue(np.abs(eeg - transformed_eeg).sum() < 1e-6)


if __name__ == '__main__':
    unittest.main()
