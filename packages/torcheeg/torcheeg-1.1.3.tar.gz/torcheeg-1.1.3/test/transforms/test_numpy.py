import unittest

import numpy as np

from torcheeg.datasets.constants import (DEAP_CHANNEL_LIST,
                                         DEAP_CHANNEL_LOCATION_DICT,
                                         M3CV_CHANNEL_LOCATION_DICT)
from torcheeg.transforms import (ARRCoefficient, BandApproximateEntropy,
                                 BandBinPower,
                                 BandDetrendedFluctuationAnalysis,
                                 BandDifferentialEntropy,
                                 BandHiguchiFractalDimension, BandHjorth,
                                 BandHurst, BandKurtosis,
                                 BandMeanAbsoluteDeviation,
                                 BandPetrosianFractalDimension,
                                 BandPowerSpectralDensity, BandSampleEntropy,
                                 BandSignal, BandSkewness, BandSpectralEntropy,
                                 BandSVDEntropy, Compose, Concatenate,
                                 CWTSpectrum, Downsample, DWTDecomposition,
                                 Flatten, MapChunk, MeanStdNormalize,
                                 MinMaxNormalize, OrderElectrode,
                                 PearsonCorrelation, PhaseLockingCorrelation,
                                 PickElectrode, RearrangeElectrode,
                                 SetSamplingRate, To2d, ToGrid,
                                 ToInterpolatedGrid, HorizontalFlip)


class TestNumpyTransforms(unittest.TestCase):

    def test_horizontal_flip(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = HorizontalFlip(
            location_dict=DEAP_CHANNEL_LOCATION_DICT, channel_dim=0)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 128))

    def test_flatten(self):
        eeg = np.random.randn(62, 5)
        transformed_eeg = Flatten()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (310,))

    def test_dwt_decomposition(self):
        eeg = np.random.randn(32, 1000)
        transformed_eeg = DWTDecomposition()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (2, 32, 500))

    def test_cwt_spectrum(self):
        eeg = np.random.randn(32, 1000)
        transformed_eeg = CWTSpectrum()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 128, 1000))

        transformed_eeg = CWTSpectrum(contourf=True)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 480, 640, 4))

    def test_order_electrode(self):
        eeg = np.random.rand(6, 3000)
        source_electrodes = ['F3', 'F4', 'C3', 'C4', 'O1', 'O2']
        target_electrodes = ['F3', 'F4', 'C3']
        transformed_eeg = OrderElectrode(
            source_electrodes=source_electrodes, target_electrodes=target_electrodes)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (3, 3000))

    def test_pick_electrode(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = PickElectrode([1, 2])(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (2, 128))

        pick = [
            'FP1', 'AF3', 'F3', 'F7', 'FC5', 'FC1', 'C3', 'T7', 'CP5', 'CP1',
            'P3', 'P7', 'PO3', 'O1', 'FP2', 'AF4', 'F4', 'F8', 'FC6', 'FC2',
            'C4', 'T8', 'CP6', 'CP2', 'P4', 'P8', 'PO4', 'O2'
        ]
        pick_list = PickElectrode.to_index_list(pick, DEAP_CHANNEL_LIST)
        self.assertEqual(len(pick_list), 28)

        transformed_eeg = PickElectrode(
            PickElectrode.to_index_list(pick, DEAP_CHANNEL_LIST))(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (28, 128))

    def test_to_2d(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = To2d()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (1, 32, 128))

    def test_to_grid(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = ToGrid(DEAP_CHANNEL_LOCATION_DICT)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (128, 9, 9))

    def test_to_interpolated_grid(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = ToInterpolatedGrid(DEAP_CHANNEL_LOCATION_DICT)(
            eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (128, 9, 9))

        eeg = np.random.randn(64, 128)
        transformed_eeg = ToInterpolatedGrid(M3CV_CHANNEL_LOCATION_DICT)(
            eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (128, 9, 11))

        pos_array = list(M3CV_CHANNEL_LOCATION_DICT.values())
        for i, channel_signal in enumerate(eeg):
            x, y = pos_array[i]
            self.assertTrue(
                np.abs(transformed_eeg['eeg'][:, x, y] - channel_signal).sum() < 1e-6)

    def test_mean_std_normalize(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = MeanStdNormalize(axis=None)(eeg=eeg)
        self.assertEqual(eeg.shape, transformed_eeg['eeg'].shape)

        eeg = np.random.randn(32, 128)
        transformed_eeg = MeanStdNormalize(axis=0)(eeg=eeg)
        self.assertEqual(eeg.shape, transformed_eeg['eeg'].shape)

        eeg = np.random.randn(32, 128)
        transformed_eeg = MeanStdNormalize(axis=1)(eeg=eeg)
        self.assertEqual(eeg.shape, transformed_eeg['eeg'].shape)

    def test_min_max_normalize(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = MinMaxNormalize(axis=None)(eeg=eeg)
        self.assertEqual(eeg.shape, transformed_eeg['eeg'].shape)

        eeg = np.random.randn(32, 128)
        transformed_eeg = MinMaxNormalize(axis=0)(eeg=eeg)
        self.assertEqual(eeg.shape, transformed_eeg['eeg'].shape)

        eeg = np.random.randn(32, 128)
        transformed_eeg = MinMaxNormalize(axis=1)(eeg=eeg)
        self.assertEqual(eeg.shape, transformed_eeg['eeg'].shape)

    def test_band_signal(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandSignal()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (4, 32, 128))

    def test_band_differential_entropy(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandDifferentialEntropy()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_band_power_spectral_density(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandPowerSpectralDensity()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_band_mean_absolute_deviation(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandMeanAbsoluteDeviation()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_band_kurtosis(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandKurtosis()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_band_skewness(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandSkewness()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_arr_coefficient(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = ARRCoefficient(order=4)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_concat(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = Concatenate(
            [BandSkewness(), BandBinPower()])(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 8))

        transformed_eeg = Concatenate(
            [Compose([MinMaxNormalize(), BandSkewness()]),
             BandBinPower()])(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 8))

    def test_map_chunk(self):
        eeg = np.random.randn(64, 1000)
        transformed_eeg = MapChunk(BandDifferentialEntropy(),
                                   chunk_size=250,
                                   overlap=0)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (64, 16))

        transformed_eeg = Concatenate([
            MapChunk(BandDifferentialEntropy(), chunk_size=250, overlap=0),
            MapChunk(BandDifferentialEntropy(), chunk_size=500, overlap=0),
            BandDifferentialEntropy()
        ])(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (64, 28))

        transformed_eeg = Concatenate([
            MapChunk(BandDifferentialEntropy(), chunk_size=250, overlap=0),
            MapChunk(BandDifferentialEntropy(), chunk_size=500, overlap=0),
            BandDifferentialEntropy(),
            BandPowerSpectralDensity()
        ])(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (64, 32))

    def test_pearson_correlation(self):
        eeg = np.random.randn(32, 4)
        transformed_eeg = PearsonCorrelation()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (1, 32, 32))

    def test_phase_locking_correlation(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = PhaseLockingCorrelation()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (1, 32, 32))

    def test_ap_entropy(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandApproximateEntropy()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_samp_entropy(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandSampleEntropy()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_svd_entropy(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandSVDEntropy()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_dfa(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandDetrendedFluctuationAnalysis()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_hfd(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandHiguchiFractalDimension()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_hjorth(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandHjorth()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_hurst(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandHurst()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_pdf(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandPetrosianFractalDimension()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_bin_power(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandBinPower()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 4))

    def test_spectral_entropy(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = BandSpectralEntropy()(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 1))

    def test_downsample(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = Downsample(num_points=32, axis=-1)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 32))

    def test_set_sampling_rate(self):
        eeg = np.random.randn(32, 128)
        transformed_eeg = SetSamplingRate(
            origin_sampling_rate=128, target_sampling_rate=64)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 64))

        eeg = np.random.randn(32, 128)
        transformed_eeg = SetSamplingRate(
            origin_sampling_rate=64, target_sampling_rate=128)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 256))

        eeg = np.random.randn(32, 128, 4)
        transformed_eeg = SetSamplingRate(
            origin_sampling_rate=128, target_sampling_rate=256, axis=1)(eeg=eeg)
        self.assertEqual(transformed_eeg['eeg'].shape, (32, 256, 4))

    def test_rearrange_electrode(self):
        src_eeg = np.random.rand(3, 128)
        tgt_eeg = RearrangeElectrode(source=['FP1', 'F3', 'F7'],
                                     target=['F3', 'F7', 'FP1', 'AF2'],
                                     missing='mean')(eeg=src_eeg)['eeg']
        self.assertEqual(tgt_eeg.shape, (4, 128))

        self.assertEqual(src_eeg[0, :].tolist(), tgt_eeg[2, :].tolist())
        self.assertEqual(src_eeg[1, :].tolist(), tgt_eeg[0, :].tolist())
        self.assertEqual(src_eeg[2, :].tolist(), tgt_eeg[1, :].tolist())


if __name__ == '__main__':
    unittest.main()
