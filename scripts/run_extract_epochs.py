# Author: Denis A. Engemann <denis.engemann@gmail.com>
# License: BSD (3-clause)

import mkl
import sys
import os.path as op
import numpy as np
import mne
from mne.io import Raw
from mne.io.pick import _picks_by_type as picks_by_type
from mne.preprocessing import read_ica
from mne.viz import plot_drop_log

from minmax.utils import setup_provenance, set_eog_ecg_channels

from config import (
    data_path,
    subjects,
    runs,
    results_dir,
    raw_fname_filt_tmp,
    events_fname_filt_tmp,
    event_id,
    ch_types_used,
    epochs_params,  # XXX list of dict
    epochs_tmin,
    epochs_tmax,
    epochs_reject,
    epochs_baseline,
    epochs_decim,
    use_ica
)

report, run_id, results_dir, logger = setup_provenance(
    script=__file__, results_dir=results_dir)


mne.set_log_level('INFO')

if len(sys.argv) > 1:
    subjects = [sys.argv[1]]
    mkl.set_num_threads(1)

for subject in subjects:
    this_path = op.join(data_path, 'MEG', subject)
    epochs_list_stim = list()
    epochs_list_resp = list()

    icas = list()
    if use_ica is True:
        for ch_type in ch_types_used:
            icas.append(read_ica(
                op.join(this_path, '{}-ica.fif'.format(ch_type))))
    for run in runs:
        fname = op.join(this_path, raw_fname_filt_tmp.format(run))
        if not op.isfile(fname):
            logger.info('Could not find %s. Skipping' % fname)
            continue

        raw = Raw(fname)
        set_eog_ecg_channels(raw)
        if 'eeg' in ch_types_used and len(raw.info['bads']) > 0:
            raw.interpolate_bad_channels()

        picks = np.concatenate(
            [p for k, p in picks_by_type(raw.info, meg_combined=True)
             if k in ch_types_used])
        picks = np.concatenate(
            [picks, mne.pick_types(raw.info, meg=False, eeg=False, eog=True)])

        events = mne.read_events(
            op.join(this_path, events_fname_filt_tmp.format(run)))

        # epochs = mne.Epochs(  # XXX deal with response VS stim locking
        #     raw=raw, events=events, event_id=event_id, tmin=epochs_tmin,
        #     picks=picks, tmax=epochs_tmax, baseline=epochs_baseline,
        #     reject=epochs_reject, decim=epochs_decim, preload=True)
        for ep, epochs_list in zip(epochs_params,
                                   [epochs_list_stim, epochs_list_resp]):
            epochs = mne.Epochs(raw=raw, **ep)
            if use_ica is True:
                for ica in icas:
                    ica.apply(epochs)

            epochs_list.append(epochs)

    for name, epochs_list in zip(['stim', 'resp'],
                                 [epochs_list_stim, epochs_list_resp]):
        epochs = mne.epochs.concatenate_epochs(epochs_list)
        report.add_figs_to_section(
            plot_drop_log(epochs.drop_log), 'total dropped {}'.format(
                name), subject)
        epochs.save(op.join(this_path, '{}-{}-epo.fif'.format(name, subject)))

report.save()
