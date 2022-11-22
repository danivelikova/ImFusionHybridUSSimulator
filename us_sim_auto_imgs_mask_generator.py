import os
import random
import configargparse
from configargparse_arguments import build_configargparser

# ------------------------
# CONFIG ARGUMENTS
# ------------------------
parser = configargparse.ArgParser(
    config_file_parser_class=configargparse.YAMLConfigFileParser)
parser.add('-c', is_config_file=True, help='config file path')
parser, hparams = build_configargparser(parser)

SAVE_DIR_US_SIM = hparams.save_dir_us_sim

placeholders = ['CT', 'NrImgs', 'InputLabelMap', 'OutputSweep', 'OutputSweepMask', 'Output2dImgsDir',
                'Output2dMasksDir', 'InputMaskVolume',
                'TransdSpline', 'DirSpline']

FOLDER_CATH_DATA = hparams.base_folder_data_path
sub_folders_cath = [sub_f for sub_f in sorted(os.listdir(FOLDER_CATH_DATA))]
folder_catheter_data = [FOLDER_CATH_DATA + s for s in sub_folders_cath]

if __name__ == "__main__":

    for folder in folder_catheter_data:
        csvs_file = folder + hparams.splines_file
        with open(csvs_file, "r") as f:
            lines = f.readlines()
        trans_splines = []
        dir_splines = []
        for l in lines[1:]:
            trans_splines.append(l.split(";")[0])
            dir_splines.append(l.split(";")[1])

        folder_full_labelmaps = folder + hparams.full_labelmap_path
        labelmaps = sorted(os.listdir(folder_full_labelmaps), reverse=True)

        for _ in range(hparams.nr_labelmap):
            i = random.randint(0, len(labelmaps))  # get random labelmaps
            full_labelmap = labelmaps[i]

            folder_output_sweep = folder + SAVE_DIR_US_SIM + full_labelmap.split('.')[0] + '_' + '.imf'
            if os.path.exists(folder_output_sweep):
                print('EXISTS: ', folder_output_sweep)
            else:
                output_2d_imgs_dir = folder + SAVE_DIR_US_SIM + hparams.save_dir_us_sim_imgs
                output_2d_masks_dir = folder + SAVE_DIR_US_SIM + hparams.save_dir_us_sim_masks
                if not os.path.exists(output_2d_imgs_dir):
                    os.makedirs(output_2d_imgs_dir, exist_ok=True)
                if not os.path.exists(output_2d_masks_dir):
                    os.makedirs(output_2d_masks_dir, exist_ok=True)

                for t_nr, t in enumerate(trans_splines[1:]):
                    transd_spline = t

                    for d_nr, d in enumerate(dir_splines[1:]):
                        dir_spline = d

                        values = []
                        arguments = ""
                        spline_nr = str(t_nr) + '_' + str(d_nr)
                        for p in placeholders:
                            if p == 'NrImgs':
                                value = str(hparams.nr_imgs)
                            if p == 'CT':
                                value = full_labelmap.split('.')[0] + '_'
                            if p == 'InputLabelMap':
                                value = folder_full_labelmaps + full_labelmap
                            if p == 'OutputSweep':
                                value = folder + SAVE_DIR_US_SIM + 'sweep_' + full_labelmap.split('.')[
                                    0] + '_' + spline_nr + '.imf'
                            if p == 'OutputSweepMask':
                                value = folder_output_sweep.split('.')[0] + spline_nr + '_' + '.imf'
                            if p == 'Output2dImgsDir':
                                value = output_2d_imgs_dir + full_labelmap.split('.')[0] + '_' + spline_nr
                            if p == 'Output2dMasksDir':
                                value = output_2d_masks_dir
                            if p == 'InputMaskVolume':
                                value = folder + hparams.input_labelmap_path + full_labelmap
                            if p == 'TransdSpline':
                                value = '"' + transd_spline + '"'
                            if p == 'DirSpline':
                                value = '"' + dir_spline + '"'

                            arguments += p + "=" + value + " "
                        print('ARGUMENTS: ', arguments)
                        os.system("ImFusionConsole" + " " + hparams.iws_file + " " + arguments)
                        print('################################################### ')
