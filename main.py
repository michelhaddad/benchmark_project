import getopt
import sys

from DatabaseManager import *
from functions import *
from SpecRatioFunctions import *

try:
    opts, args = getopt.getopt(sys.argv, "n:", ["name="])
except getopt.GetoptError:
    print('main.py -n <pc name>')
    sys.exit(2)

# Get the name of the pc/user and add to database
pc_name = args[2]

# Initialize connection with AWS RDS database
db = DatabaseManager()

# Add user to the pc table
pc_id = db.add_pc_to_db(pc_name)

# Get the runtime for each benchmark (benchmarks are sorted by their id in the database)
ordered_runtimes = get_ordered_runtimes()

# Get the reference runtime for each benchmark
reference_runtimes = db.get_reference_times()
if not reference_runtimes:
    exit(500)

# Add the result for each benchmark in the results table
spec_ratios = []
for i in range(1, 8):
    benchmark_runtime = ordered_runtimes[i - 1]
    reference_runtime = reference_runtimes[i - 1]['execution_time']
    spec_ratio = get_spec_ratio(reference_runtime, benchmark_runtime)
    spec_ratios.append(spec_ratio)
    db.add_benchmark_result(pc_id, i, benchmark_runtime, spec_ratio)

# # Update the average spec ratio of the pc in the pc table
geometric_avg_spec_ratio = avg_spec_ratio(spec_ratios)
db.update_avg_spec_ratio(pc_id, geometric_avg_spec_ratio)

# Display avg spec ratio and ranking of pc
pc_results = db.get_pc_ranking(pc_id)
print("You ranked %s out of %s pcs with a SPEC RATIO of %s!"
      % (pc_results['rank'], db.get_total_pc_count(), pc_results['avg']))
