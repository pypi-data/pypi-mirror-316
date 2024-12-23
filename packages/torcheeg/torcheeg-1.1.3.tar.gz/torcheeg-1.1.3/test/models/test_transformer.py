import unittest

import torch

from torcheeg.models import (ArjunViT, ATCNet, Conformer, SimpleViT, TCNet,
                             VanillaTransformer, ViT, LaBraM)


class TestTransformer(unittest.TestCase):
    def test_labram(self):
        eeg = torch.randn(2, 6, 8, 200)
        model = LaBraM.base_patch200_200(num_classes=4)
        pred = model(eeg, electrodes=['FP1', 'FPZ', 'FP2',
    'AF9', 'AF7', 'AF5'])
        model = LaBraM.large_patch200_200(num_classes=4)
        pred = model(eeg, electrodes=['FP1', 'FPZ', 'FP2',
    'AF9', 'AF7', 'AF5'])
        model = LaBraM.huge_patch200_200(num_classes=4)
        pred = model(eeg, electrodes=['FP1', 'FPZ', 'FP2',
    'AF9', 'AF7', 'AF5'])
        self.assertEqual(tuple(pred.shape), (2, 4))

    def test_tcnet(self):
        eeg = torch.randn(2, 22, 1000)
        model = TCNet(num_classes=4,
                      num_electrodes=22,
                      F1=8,
                      D=2)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (2, 4))

    def test_simple_vit(self):
        eeg = torch.randn(1, 128, 9, 9)
        model = SimpleViT(chunk_size=128, t_patch_size=32,
                          s_patch_size=(3, 3), num_classes=2)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (1, 2))

    def test_arjun_vit(self):
        eeg = torch.randn(1, 32, 128)
        model = ArjunViT(chunk_size=128, t_patch_size=32, num_classes=2)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (1, 2))

    def test_vanilla_transformer(self):
        eeg = torch.randn(1, 32, 128)
        model = VanillaTransformer(chunk_size=128,
                                   t_patch_size=32,
                                   hid_channels=32,
                                   depth=3,
                                   heads=4,
                                   head_channels=64,
                                   mlp_channels=64,
                                   num_classes=2)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (1, 2))

    def test_vit(self):
        eeg = torch.randn(1, 128, 9, 9)
        model = ViT(chunk_size=128, t_patch_size=32,
                    s_patch_size=(3, 3), num_classes=2)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (1, 2))

    def test_conformer(self):
        eeg = torch.randn(2, 1, 32, 128)
        model = Conformer(num_electrodes=32, sampling_rate=128, num_classes=2)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (2, 2))

    def test_atcnet(self):
        eeg = torch.randn(2, 1, 32, 1000)
        model = ATCNet(num_classes=3, num_electrodes=32, chunk_size=1000)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (2, 3))

        # other shape
        eeg = torch.randn(2, 1, 64, 512)
        model = ATCNet(num_classes=4, num_electrodes=64, chunk_size=512)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (2, 4))

        # other shape
        eeg = torch.rand(2, 1, 96, 256)
        model = ATCNet(num_classes=4, num_electrodes=96, chunk_size=256)
        pred = model(eeg)
        self.assertEqual(tuple(pred.shape), (2, 4))


if __name__ == '__main__':
    unittest.main()
