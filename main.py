import pickle as pkl
from pathlib import Path
from shutil import rmtree
from os import system
from visualiser.mesh_visualiser import MeshVisualiser

def readPickle(name, pkl_fname, output_dir="output_dir"):
     '''
     Unpickle files
     '''
     p = Path(output_dir) / name / pkl_fname
     print(p)
     result = pkl.load(open(p, "rb"))
     print("Pickle Output of {}:\t{}".format(pkl_fname, result))
     return


def main(output_dir ,view, name, data_dir = Path("data/runData"), exclude_vtk=False, show_plots=False):
     '''
     Main function for interacting with the pipeline
     '''

     plotFlag = "--show_plots" if show_plots else ""
     exclude_vtk = "--exclude_vtk" if exclude_vtk else ""

     # Delete folder of previous .vtk slices before creating new ones 
     delPath = output_dir / "{}/vtk".format(name)
     try:
          rmtree(delPath)
     except OSError as e:
          print("Error: %s - %s." % (e.filename, e.strerror))

     
     system("python create_seg_dataset.py \
          --image_mode noisy \
          --save_vtk_slices \
          --verbose \
          --rotation_type random \
          --num_slices 3 \
          --vtk_data_dir {} \
          --output_dir {} \
          --name {} \
          --view_name {} \
          {} \
          {} \
          ".format(data_dir, output_dir, name, view, exclude_vtk, plotFlag))

     return


if __name__ == "__main__":
     # Define directories and slices 
     view= "v4" 
     name= view
     output_dir  = Path("exp_output_dir")

     # Generate slices 
     main(output_dir =output_dir , view=view, name=name, exclude_vtk=False, show_plots=False)


     # Plot the .vtk files using the mesh_visualiser
     #sliceDir = output_dir / name
     #vis = MeshVisualiser(sliceDir)
     #vis.verificationView(modelNum=(1,))


     # Unpickle output files
     #readPickle(name, pkl_fname="img_DF_0.pck", output_dir= output_dir)
     #readPickle(name, pkl_fname="vtk_df_0.pck", output_dir= output_dir)

     

# TODO What do the images look like when you align slices?
     # NO images are generated when this is the case
# TODO How do the transforms in export_..py affect the final pseudo images?
     # they can change appearance, alignment and other aspsects of the p-images
# TODO Are the a4ch slices aligned to be in a specific plane like it seems when plotted?
     # Their alignment is definitely decided in export_config.py but not necessarilly to a specific plane
# TODO What standard are you aiming for when creating pseudos?
# TODO Generate good looking pseudos for a TEE view