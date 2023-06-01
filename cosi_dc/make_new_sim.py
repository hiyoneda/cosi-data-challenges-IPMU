import os
import cosi_dc

install_dir = os.path.split(cosi_dc.__file__)[0]

def main():

    # Copy starting files to new analysis directory:
    new_dir = os.getcwd()
    os.system("scp %s/inputs.yaml %s/run_sim_setup.py %s" %(install_dir,install_dir,new_dir))

########################
if __name__=="__main__":
        main(sys.argv)

