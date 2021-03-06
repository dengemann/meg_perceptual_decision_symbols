import os
import os.path as op

# PATHS ########################################################################
base_path = op.dirname(op.dirname(__file__))

data_path = op.join(base_path, 'data', 'ambiguity')

""" Data path notes

link your data against data_path

the directory structure should look like this

# MEG directory containing MEG data for each subject
./data/ambiguity/MEG/subject1
./data/ambiguity/MEG/...
./data/ambiguity/MEG/subjectN

# freesurfer directory containing MR data for each subject
./data/ambiguity/subjects/subject1
./data/ambiguity/subjects/...
./data/ambiguity/subjects/subjectN

# other stuff
./data/ambiguity/behavioral/
"""

results_dir = op.join(base_path, 'results')

if not op.exists(results_dir):
    os.mkdir(results_dir)

# SUBJECTS #####################################################################
# subjects = XXX write your list of subjects here

exclude_subjects = []  # XXX add subject names here if you wan't to exclude

runs = list(range(1, 10, 1))  # 6 runs


# FILRERING ####################################################################
lowpass = 40
highpass = 1
filtersize = 16384
decim = 1

# FILENAMES ####################################################################
# XXX update file name templates
raw_fname_tmp = 'run_{:02d}_sss.fif'
raw_fname_filt_tmp = 'run_{:02d}_filt-%d-%d_sss_raw.fif' % (
    highpass, lowpass)
events_fname_filt_tmp = 'run_{:02d}_filt-%d-%d_sss-eve.fif' % (
    highpass, lowpass)
forward_fname_tmp = '{}-meg-oct-6-fwd.fif'
morph_mat_fname_tmp = '{}-morph_mat.mat'

# SELECTION ####################################################################
ch_types_used = ['meg']

# ICA ##########################################################################

# XXX check EOG channels, definitions might differ for subjects
use_ica = True
n_components = 'rank'
n_max_ecg = 4
n_max_eog = 2
ica_reject = dict(mag=5e-12, grad=5000e-13, eeg=300e-6)
ica_decim = 15  # XXX adjust depdning on data

# REPORT
open_browser = False

# EPOCHS #######################################################################

# XXX write function to select epochs
event_id = None  # use all for master epochs
epochs_tmin, epochs_tmax = -0.2, 0.8
epochs_reject = dict(grad=4000e-13, mag=4e-12, eog=180e-6)
epochs_baseline = None
epochs_decim = 3

# COV ##########################################################################
cov_method = ['shrunk', 'empirical']

# INVERSE ######################################################################

fsave_grade = 4

fwd_fname_tmp = 'sub{:02d}-meg-oct-6-fwd.fif'  #

make_inverse_params = {'loose': 0.2,
                       'depth': 0.8,
                       'fixed': False,
                       'limit_depth_chs': True}
snr = 3
lambda2 = 1.0 / snr ** 2
apply_inverse_params = {'method': "dSPM", 'pick_ori': None, 'pick_normal': None}

# MAIN #########################################################################

# XXX parameters for your main analysis

# STATS ########################################################################

clu_sigma = 1e3
clu_n_permutations = 1024
clu_threshold = 0.05
