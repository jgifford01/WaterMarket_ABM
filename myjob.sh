#!/bin/bash
#SBATCH --partition=kamiak	# Partition/Queue to use
#SBATCH --job-name=myJob	# Job name
#SBATCH --output=output/%x_%j.out	# Output file (stdout)
#SBATCH --error=output/%x_%j.err	# Error file (stderr)
#SBATCH --time=1-00:00:00	# Wall clock time limit Days-HH:MM:SS
##SBATCH --mail-type=ALL	# Email notification: BEGIN,END,FAIL,ALL
##SBATCH --mail-user=jacob.gifford1@wsu.edu	# Email address for notifications

#SBATCH --nodes=1		# Number of nodes (min-max) 
#SBATCH --ntasks-per-node=1	# Number of tasks per node (processes)
#SBATCH --cpus-per-task=40	# Number of cores per task (threads)
##SBATCH --mem-per-cpu=8G	# Memory per core (gigabytes)

echo "I am job $SLURM_JOBID running on nodes $SLURM_JOB_NODELIST"
source venv/bin/activate
module load python3		# Load software module from Kamiak repository


#python main.py
#python main_SM_uniform_random.py
#python fig4_sup_dem_plot.py
#python fig5_pmax_3panel_plot.py
#python summary_stats.py
#python pmax_bar_charts.py
#python fig6_price_plot.py
#python fig7_nonpec_3panel_plot.py
python non_pec_bar_charts.py
deactivate

echo "Completed job on node $HOSTNAME"

#==== END OF FILE

# code to run script: sbatch filename.sh
# check queue: squeue -u jacob.gifford1
# cancel all jobs: scancel -u jacob.gifford1
