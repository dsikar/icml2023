#!/bin/bash
#SBATCH -D /users/aczd097/git/icml2023/scripts    # Working directory
#SBATCH --job-name icml2024                      # Job name
#SBATCH --mail-type=ALL                 # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=daniel.sikar@city.ac.uk         # Where to send mail
#SBATCH --nodes=4                                # Run on 4 nodes (each node has 48 cores)
#SBATCH --ntasks-per-node=48
#SBATCH --exclusive                              # Exclusive use of nodes
#SBATCH --mem=0                                  # Expected memory usage (0 means use all available memory)
#SBATCH --time=24:00:00                          # Time limit hrs:min:sec
#SBATCH -e outputs/%x_%j.e                         # Standard output and error log [%j is replaced with the jobid]
#SBATCH -o outputs/%x_%j.o                         # [%x with the job name], make sure 'results' folder exists.

#Enable modules command
source /opt/flight/etc/setup.sh
flight env activate gridware

#Remove any unwanted modules
module purge

#Modules required
#module load python/3.7.12 # now loading through pipenv
module add gnu
#Run script
start=$(date +%s) # Record the start time in seconds since epoch

#python mnist_cnn_train.py #--save-model todo
python semantic_scholar_runner.py


end=$(date +%s) # Record the end time in seconds since epoch
diff=$((end-start)) 

# Convert seconds to hours, minutes, and seconds
hours=$((diff / 3600))
minutes=$(( (diff % 3600) / 60 ))
seconds=$((diff % 60))

echo "semantic_scholar_runner - Script execution time: $hours hours, $minutes minutes, $seconds seconds"

