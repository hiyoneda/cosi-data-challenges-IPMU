# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# working directory
workdir=$1

if [ -d ${workdir} ]; then
    #change to working directory and run job
    cd ${workdir}
    
    #conda activation
    conda activate /lustre/work/COSI/software/python_cosi
    
    #the main MEGAlib environment is sourced
    source /lustre/work/COSI/software/megalib/bin/source-megalib.sh
    python run_sims_cosima.py
    
    #the dee2022 MEGAlib environment is sourced
    source /lustre/work/COSI/software/megalib_dee2022/bin/source-megalib.sh
    python run_sims_revan.py
else
    echo "the directory ${workdir} does not exist"
fi
