import sys
import time

if __name__ == "__main__":
    if len(sys.argv) <= 3:
        # missing arguments, print usage message
        print("Usage:")
        print(" $ python3 processdata.py <ref_file> <reads_file> <align_file>")
        sys.exit(0)

reference_list = open(sys.argv[1], "r") # Read reference file
reads_list = open(sys.argv[2], "r") # Read reads file
align_list = open(sys.argv[3], "w") # Create alignments file

reference = reference_list.readlines() # Read the reference 
#reference = reference[:-1] # Remove additional space (for manually created .txt)

reference = "".join(reference)
reference = reference.splitlines() # Remove newlines
reference = "".join(reference) # Reference as a string without newlines

align_cero = 0 # Initialize count of reads that align 0,1,2 times
align_one = 0
align_two = 0
read_count = 0
t0 = time.time()

for read in reads_list: # Evaluate each read in the reads list
    read_count +=1 # New read added to count
    read = read[:-1] # Take just the read string no space
    list_result = [] # List of resulting alignment indexes
    index = 0 # Initial index position to evaluate
    #print("Read :", read)
    #print("Reference : ", reference)
    index = reference.find(read,index) # First alignment search
    #print(index)
    if index != -1: # Found alignment
        list_result.append(index)  # Append position to the list of results
        index = reference.find(read, index+1) # Second alignment search starting from next consecutive index
        if index != -1: # Alignment found in second search
            list_result.append(index) # Append second alignment index to the list of results
            align_two += 1 # Count new case of two alignments
        else:
            align_one += 1 # Count new case of one alignment
    else:
        list_result.append(index) # No alignment found
        align_cero +=1 # Count new case of no alignment
        
    for i in range(len(list_result)): # Convert list_result to string
        list_result[i] = str(list_result[i])
        
    align_list.write(read + " " + " ".join(list_result) + "\n") # Write results as string in align file  

t1 = time.time()
    
align_list.close
reference_list.close
reads_list.close

t_diff = t1 - t0 # Compute elapsed time

ref_len = len(reference)
align_cero_frac = align_cero/read_count # Compute fraction of reads that align 0,1,2 times
align_one_frac = align_one/read_count
align_two_frac = align_two/read_count

print("reference length: ", ref_len) # Print reference length
print("number of reads: ", read_count) # Print number of reads
print("aligns 0: ", align_cero_frac) # Print number of zero alignments
print("aligns 1: ", align_one_frac) # Print number of one alignment
print("aligns 2: ", align_two_frac) # Print number of two alignments
print("elapsed time: ", t_diff) # Print elapsed time
