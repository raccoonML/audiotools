from argparse import Namespace

hparams = Namespace(sample_rate = 24000,
                    n_fft = 2048,
                    num_mels = 80,
                    hop_size = 300,
                    win_size = 1200,
                    fmin = 0,
                    fmax = 12000,
                    min_level_db = -100,
                    ref_level_db = 20,
                    max_abs_value = 4.,
                    preemphasis = 0.97,
                    preemphasize = True,
                    symmetric_mels = True,
                    signal_normalization = True,
                    allow_clipping_in_normalization = True,
                    power = 1.2,
                    griffin_lim_iters = 100)
