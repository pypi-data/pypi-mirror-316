from ..test import ExperimentTest, Results
from . import spm


class HasCorrectItems(ExperimentTest):
    """Passes if a `FTM_QUANTIFICATION2` resource is found and this resource
    has the expected items according to the pipeline
    [specifications](https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/pet#outputs)."""

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'
    expected_items = ['static_pet.nii.gz',
                      'optimized_static_pet.nii.gz',
                      'static_pet_t1.nii.gz',
                      'c1mri_bin.nii.gz',
                      'c2mri_bin.nii.gz',
                      'c1mri.nii.gz',
                      'c2mri.nii.gz',
                      'c3mri.nii.gz',
                      'rp_pet.txt',
                      'quantification_results.csv',
                      'wstatic_pet_scaled_cgm.nii.gz',
                      'wstatic_pet_scaled_pons.nii.gz',
                      'wstatic_pet_scaled_wcbs.nii.gz',
                      'wstatic_pet_scaled_wc.nii.gz',
                      'wstatic_pet_scaled_wm.nii.gz',
                      'woptimized_static_pet_scaled_cgm.nii.gz',
                      'woptimized_static_pet_scaled_pons.nii.gz',
                      'woptimized_static_pet_scaled_wcbs.nii.gz',
                      'woptimized_static_pet_scaled_wc.nii.gz',
                      'woptimized_static_pet_scaled_wm.nii.gz',
                      'optimized_static_pet_scaled_cgm.nii.gz',
                      'optimized_static_pet_scaled_pons.nii.gz',
                      'optimized_static_pet_scaled_wcbs.nii.gz',
                      'optimized_static_pet_scaled_wc.nii.gz',
                      'wresized_Hammers_mith_atlas_n30r83_SPM5.nii.gz',
                      'rwresized_Hammers_mith_atlas_n30r83_SPM5.nii.gz',
                      'rwresized_Hammers_mith_atlas_n30r83_SPM5_masked.nii.gz',
                      'rrwresized_Hammers_mith_atlas_n30r83_SPM5_masked.nii.gz',
                      'wAAL.nii.gz',
                      'rwAAL.nii.gz',
                      'rwAAL_masked.nii.gz',
                      'rrwAAL_masked.nii.gz',
                      'rgm_rois.nii.gz',
                      'gm_rois.nii.gz',
                      'pyscript_coregister.m',
                      'pyscript_coregister_icbm152.m',
                      'pyscript_newsegment.m',
                      'pyscript_normalize12.m',
                      'pyscript_normalize_atlas.m',
                      'pyscript_reslice_2_MRI.m',
                      'pyscript_realign_PET.m',
                      'pyscript_setorigin.m',
                      'pyscript_smooth.m']

    def run(self, experiment_id):
        e = self.xnat_instance.select.experiment(experiment_id)
        label = e.label()
        self.expected_items.append('{}.log'.format(label))
        self.expected_items.append('{}.err'.format(label))

        res = e.resource(self.resource_name)
        file_list = set([e.attributes()['Name'] for e in res.files()])
        missing = set(self.expected_items).difference(file_list)

        msg = []
        result = True
        if missing:
            result = False
            msg.append('Missing items: {}.'.format(list(missing)))

        return Results(result, data=msg)


class QuantificationResultsShape(ExperimentTest):
    """`FTM_QUANTIFICATION2` resources have quantification results stored as
    tabular data in a CSV-formatted file. This test attempts to read the CSV file
    and assert that its dimensions match the expected shape. Test fails if file
    content cannot be parsed as CSV or if data dimensions do not match the
    expected size (1192 rows x 7 columns). Passes otherwise."""

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'
    csv_shape = (1192, 7)

    def run(self, experiment_id):
        import io
        import pandas as pd
        import pandas.errors as pd_errors

        e = self.xnat_instance.select.experiment(experiment_id)
        res = e.resource(self.resource_name)

        csv_file = res.file('quantification_results.csv')
        csv_content = (self.xnat_instance.get(csv_file._uri)).text
        try:
            df = pd.read_csv(io.StringIO(csv_content))
        except pd_errors.ParserError:
            return Results(False, data=['Invalid CSV file format.'])

        if df.shape != self.csv_shape:
            return Results(False, data=['Invalid CSV file dimensions; expected:'
                                        '{}, current: {}'.format(self.csv_shape,
                                                                 df.shape)])
        return Results(True, data=[])


class HasExpectedAtlasRegions(ExperimentTest):
    """This test passes if all expected regions from `AAL` and `Hammers` atlases
    are found in the CSV-formatted file containing the `FTM_QUANTIFICATION2`
    quantification results. Fails otherwise."""

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'
    expected_hammers = {'Amygdala',
                        'Ant_TL_inf_lat',
                        'Ant_TL_med',
                        'Brainstem',
                        'CaudateNucl',
                        'Cerebellum',
                        'Corp_Callosum',
                        'FL_OFC_AOG',
                        'FL_OFC_LOG',
                        'FL_OFC_MOG',
                        'FL_OFC_POG',
                        'FL_inf_fr_G',
                        'FL_mid_fr_G',
                        'FL_precen_G',
                        'FL_strai_G',
                        'FL_sup_fr_G',
                        'FrontalHorn',
                        'G_cing_ant_sup',
                        'G_cing_post',
                        'G_occtem_la',
                        'G_paraH_amb',
                        'G_sup_temp_ant',
                        'G_sup_temp_cent',
                        'G_tem_midin',
                        'Hippocampus',
                        'Insula',
                        'NuclAccumb',
                        'OL_cuneus',
                        'OL_ling_G',
                        'OL_rest_lat',
                        'PL_postce_G',
                        'PL_rest',
                        'PL_sup_pa_G',
                        'Pallidum',
                        'PosteriorTL',
                        'Presubgen_antCing',
                        'Putamen',
                        'S_nigra',
                        'Subcall_area',
                        'Subgen_antCing',
                        'TemporaHorn',
                        'Thalamus',
                        'ThirdVentricl'}
    expected_aal = {'Amygdala',
                    'Angular',
                    'Calcarine',
                    'Caudate',
                    'Cerebelum_10',
                    'Cerebelum_3',
                    'Cerebelum_4_5',
                    'Cerebelum_6',
                    'Cerebelum_7b',
                    'Cerebelum_8',
                    'Cerebelum_9',
                    'Cerebelum_Crus1',
                    'Cerebelum_Crus2',
                    'Cingulum_Ant',
                    'Cingulum_Mid',
                    'Cingulum_Post',
                    'Cuneus',
                    'Frontal_Inf_Oper',
                    'Frontal_Inf_Orb',
                    'Frontal_Inf_Tri',
                    'Frontal_Med_Orb',
                    'Frontal_Mid',
                    'Frontal_Mid_Orb',
                    'Frontal_Sup',
                    'Frontal_Sup_Medial',
                    'Frontal_Sup_Orb',
                    'Fusiform',
                    'Heschl',
                    'Hippocampus',
                    'Insula',
                    'Lingual',
                    'Occipital_Inf',
                    'Occipital_Mid',
                    'Occipital_Sup',
                    'Olfactory',
                    'Pallidum',
                    'ParaHippocampal',
                    'Paracentral_Lobule',
                    'Parietal_Inf',
                    'Parietal_Sup',
                    'Postcentral',
                    'Precentral',
                    'Precuneus',
                    'Putamen',
                    'Rectus',
                    'Rolandic_Oper',
                    'Supp_Motor_Area',
                    'SupraMarginal',
                    'Temporal_Inf',
                    'Temporal_Mid',
                    'Temporal_Pole_Mid',
                    'Temporal_Pole_Sup',
                    'Temporal_Sup',
                    'Thalamus',
                    'Vermis_10',
                    'Vermis_1_2',
                    'Vermis_3',
                    'Vermis_4_5',
                    'Vermis_6',
                    'Vermis_7',
                    'Vermis_8',
                    'Vermis_9'}

    def run(self, experiment_id):
        import io
        import pandas as pd
        import pandas.errors as pd_errors

        e = self.xnat_instance.select.experiment(experiment_id)
        res = e.resource(self.resource_name)

        csv_file = res.file('quantification_results.csv')
        csv_content = (self.xnat_instance.get(csv_file._uri)).text
        try:
            df = pd.read_csv(io.StringIO(csv_content))
        except pd_errors.ParserError:
            return Results(False, data='Invalid CSV file format.')

        df_hammer_rois = df.query('atlas == "hammers" and region in @self.expected_hammers')
        missing_hammers = self.expected_hammers.difference(df_hammer_rois.region)

        df_aal_rois = df.query('atlas == "aal" and region in @self.expected_aal')
        missing_aal = self.expected_aal.difference(df_aal_rois.region)

        missing_regions = missing_hammers.union(missing_aal)
        if len(missing_regions) > 0:
            return Results(False, data=list(missing_regions))

        return Results(True, data=[])

    def report(self):
        report = []
        if not self.results.has_passed:
            if isinstance(self.results.data, list):
                report.append('Missing regions: {}'
                              ''.format(list(self.results.data)))
            else:
                report.append(self.results.data)
        return report


class HasCorrectFSLVersion(ExperimentTest):
    """This test checks the version of FSL used for processing the images.
    Passes if FTM_QUANTIFICATION2 outputs were created using the expected
    version (i.e. `6.0.1`)."""

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'

    def run(self, experiment_id):

        expected_version = 'FSL Version: 6.0.1'

        e = self.xnat_instance.select.experiment(experiment_id)
        res = e.resource(self.resource_name)
        log = res.file('LOGS/{}.log'.format(e.label()))
        if not log.exists():
            msg = '{} log file not found.'.format(self.resource_name)
            return Results(False, data=[msg])

        log_data = self.xnat_instance.get(log._uri).text
        version = [line for line in log_data.splitlines()
                   if line.startswith('FSL Version')]

        if not version or version[0] != expected_version:
            return Results(False, data=['{}'.format(version[0])])

        return Results(True, data=[])


class HasCorrectSPMVersion(spm.HasCorrectSPMVersion):
    __doc__ = spm.HasCorrectSPMVersion.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'FTM_QUANTIFICATION2')

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'


class HasCorrectMatlabVersion(spm.HasCorrectMatlabVersion):
    __doc__ = spm.HasCorrectMatlabVersion.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'FTM_QUANTIFICATION2')

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'


class HasCorrectOSVersion(spm.HasCorrectOSVersion):
    __doc__ = spm.HasCorrectOSVersion.__doc__
    __doc__ = __doc__.replace('SPM12_SEGMENT', 'FTM_QUANTIFICATION2')

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'


class IsMeanFDConsistent(ExperimentTest):
    """Head motion can significantly impact data quality. Mean Framewise
    Displacement (FD) is a useful metric to quantify motion. It represents the
    weighted average of combined rotational and translational displacements across
    imaging frames for all PET time-series volumes. This test passes if the mean
    FD < 1 mm. Fails otherwise."""

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource_name = 'FTM_QUANTIFICATION2'
    threshold = 1.

    def compute_fd(self, par_file):
        import numpy as np

        params = np.loadtxt(par_file)
        diffs = np.diff(params, axis=0)
        # Translational FD: sum of absolute differences for 
        fd_translation = np.abs(diffs[:, :3])
        # Rotational FD: sum of absolute differences for rotations 
        # Convert rotations from degrees to mm
        fd_rotation = 50 * (np.pi / 180) * np.abs(diffs[:, 3:])
        fd = np.sum(fd_translation, axis=1) + np.sum(fd_rotation, axis=1)
        return np.mean(fd)

    def run(self, experiment_id):
        import os
        import tempfile
        import logging as log
        
        e = self.xnat_instance.select.experiment(experiment_id)
        r = e.resource(self.resource_name)
        if not r.exists():
            msg = f'{self.resource_name} resource not found'
            log.error(msg)
            return Results(False, data=[msg])

        f = r.file('rp_pet.txt')
        if not f.exists():
            return Results(False, data=['File `rp_pet.txt` not found.'])
        fd, fp = tempfile.mkstemp(suffix='.par')
        os.close(fd)

        f.get(fp)

        mean_fd = self.compute_fd(fp)
        os.remove(fp)

        result = bool(mean_fd < self.threshold)
        return Results(result, data=mean_fd)

    def report(self):
        report = []
        if not self.results.has_passed:
            if isinstance(self.results.data, float):
                report.append('Mean FD: {}'.format(self.results.data))
            else:
                report.append(self.results.data)
        return report


class GMROISnapshot(ExperimentTest):
    """This test creates a snapshot of the GM regions derived from the Hammers
    atlas and coregistered to the native space (i.e. `gm_rois.nii`), overlaid to
    the MRI T1w image. Test passes if the snapshot is created successfully. Fails
    otherwise"""

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',  
    resource = 'FTM_QUANTIFICATION2'

    def _get_usable_t1(self, experiment_id):
        import os
        import tempfile
        from ..sanity import pet

        p = pet.HasUsableT1(self.lut, self.xnat_instance)
        mri_data = p.run(experiment_id).data[0]

        s = self.xnat_instance.select.experiment(mri_data['MR_ID']).\
            scan(mri_data['MR_scanID'])
        files = list(s.resource('NIFTI').files('*.nii.gz'))

        if len(files) < 1:
            return Results(False, data=['T1w NIfTI image not found.'])
        f = files[0]
        fd, fp = tempfile.mkstemp(suffix='.nii.gz')
        os.close(fd)
        f.get(fp)

        return fp

    def run(self, experiment_id):
        import os
        import tempfile
        import logging as log
        from nilearn import image
        from . import pet_quantification_snapshot

        if os.getenv('SKIP_SNAPSHOTS_TESTS') == 'True':
            return Results(experiment_id == self.passing[0],
                           data=['Skipping it. (SKIP_SNAPSHOTS_TESTS)'])

        r = self.xnat_instance.select.experiment(experiment_id).resource(self.resource)
        if not r.exists():
            msg = f'{self.resource} resource not found'
            log.error(msg)
            return Results(False, data=[msg])

        f = r.file('REGIONAL/gm_rois.nii.gz')
        if not f.exists():
            return Results(False,
                           data=['File `REGIONAL/gm_rois.nii.gz` not found.'])

        fd, mask_fp = tempfile.mkstemp(suffix='.nii.gz')
        os.close(fd)
        f.get(mask_fp)

        f = r.file('c1mri_bin.nii.gz')
        if not f.exists():
            return Results(False, data=['File `c1mri_bin.nii.gz` not found.'])

        fd, c1_fp = tempfile.mkstemp(suffix='.nii.gz')
        os.close(fd)
        f.get(c1_fp)
        c1 = image.load_img(c1_fp)

        t1_fp = self._get_usable_t1(experiment_id)
        t1 = image.load_img(t1_fp).get_fdata()
        t1_centered = image.new_img_like(c1, t1)

        res = pet_quantification_snapshot(mask_fp, t1_centered)

        for item in [mask_fp, c1_fp, t1_fp]:
            os.remove(item)
        return Results(True, res)

    def report(self):
        report = []
        if self.results.has_passed:
            for path in self.results.data:
                report.append('![snapshot]({})'.format(path))
        else:
            report = self.results.data

        return report
    

class PETSegmentationSnapshot(ExperimentTest):
    """This test creates a snapshot of the segmented GM mask (red) overlaid to the
    averaged PET image in T1 native space. Test passes if the snapshot is created
    successfully. Fails otherwise"""

    passing = 'BBRCDEV_E02124',
    failing = 'BBRCDEV_E03968',
    resource = 'FTM_QUANTIFICATION2'

    def run(self, experiment_id):
        import os
        import tempfile
        import logging as log
        from nilearn import plotting
        from nilearn import image

        if os.getenv('SKIP_SNAPSHOTS_TESTS') == 'True':
            return Results(experiment_id == self.passing[0],
                           data=['Skipping it. (SKIP_SNAPSHOTS_TESTS)'])

        r = self.xnat_instance.select.experiment(experiment_id).resource(self.resource)
        if not r.exists():
            msg = f'{self.resource} resource not found'
            log.error(msg)
            return Results(False, data=[msg])

        fpaths = []
        for fn in ['static_pet_t1.nii.gz', 'c1mri_bin.nii.gz']:
            f = r.file(fn)
            if not f.exists():
                return Results(False,
                               data=[f'File `{fn}` not found.'])

            fd, fp = tempfile.mkstemp(suffix='.nii.gz')
            os.close(fd)
            f.get(fp)
            fpaths.append(fp)

        # crop the static PET image for better visualization outcome
        pet_img = image.load_img(fpaths[0])
        cropped_pet_img = image.crop_img(pet_img, rtol=0.05, pad=False)

        res = []
        for each in 'xyz':
            _, path = tempfile.mkstemp(suffix='.jpg')
            res.append(path)
            im = plotting.plot_anat(cropped_pet_img,
                                    black_bg=True,
                                    bg_img=None,
                                    display_mode=each,
                                    draw_cross=False)
            im.add_overlay(fpaths[1], vmin=0, vmax=1,
                           cmap='red_transparent', alpha=0.4)

            im.savefig(path)

        for item in fpaths:
            os.remove(item)
        return Results(True, res)

    def report(self):
        report = []
        if self.results.has_passed:
            for path in self.results.data:
                report.append('![snapshot]({})'.format(path))
        else:
            report = self.results.data

        return report