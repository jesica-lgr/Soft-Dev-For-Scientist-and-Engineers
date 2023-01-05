import sys
import random
import math

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        # missing arguments, print usage message
        print("Usage:")
        print(" $ python3 generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>")
        sys.exit(0)

ref_length = int(sys.argv[1]) # Given Length of the reference
nreads = int(sys.argv[2]) # Numer of reads
read_len = int(sys.argv[3]) # Length of the reads
ref_file = open(sys.argv[4], "w") # String - reference_file name
reads_file = open(sys.argv[5], "w") # String - reads file name


# Generate random part of the reference 

sevfive_ref_pos = int(math.ceil(ref_length*0.75)) - 1 # End position for third quarters of reference_list 
reference_list = list(0 for i in range(sevfive_ref_pos + 1)) # Create initial reference list

for i in range(int(sevfive_ref_pos)): # Fill seventy five percent of the reference list
    reference_list[i] = random.randint(0,3) # Assign random numbers between 0 and 3
#print(reference_list)

reference_list = ['A' if data == 0 else data for data in reference_list] # Susbtitute numerical values with letters
reference_list = ['C' if data == 1 else data for data in reference_list]
reference_list = ['G' if data == 2 else data for data in reference_list]
reference_list = ['T' if data == 3 else data for data in reference_list]

twenfive_ref = ref_length - sevfive_ref_pos - 1 # Number of elements to duplicate
#print("Number of elements to duplicate (twenty five_ref)", twenfive_ref)

duplicate_list = reference_list[- int(twenfive_ref):] # List of elements to duplicate
reference_list = reference_list + duplicate_list # Concatenate lists to create the complete reference list
#ref_file.write(str(reference_list))
#print(reference_list)

reference_string = "".join(reference_list) # Convert list to string
ref_file.write(reference_string) # write reference string to the ref_file

# Generate reads from the reference

current_n_reads = 0  # Initialize number of reads
reads = [0]*nreads # Create list of length read_len
fifty_ref_pos = int(math.floor(ref_length*0.5))-1 # Position corresponding to half of the length of the reference list

align_one = 0 # Initialize count of read that align 0, 1 and 2 times
align_two = 0
align_cero = 0

#reference_string = "".join(reference_list)

while current_n_reads < nreads: # Run generate read process n_reads -1 times 
    type_of_read = random.random() # Select the type of read to generate
    if type_of_read <= 0.75: 
        # Generate a read that align once
        #print("Case 1")
        initial_pos_read = random.randint(0, fifty_ref_pos - read_len) # Random position in the first half of the reference list
        final_pos_read = initial_pos_read + read_len -1  # Final position on the reference list given the length of the read
        #print("Initial : ", initial_pos_read)
        #print("Final: ", final_pos_read)
        #print("Ref_length : ", ref_length)
        
        read = reference_list[initial_pos_read : final_pos_read + 1] # Insert read in pos i of reads list
        read_string = "".join(read)
        reads[current_n_reads] = read_string # Add read_string to the list of reads
        align_one += 1  # Count new read that align once
    elif type_of_read > 0.75 and type_of_read <= 0.85:
        # Generate a read that align twice
        #print("Case 2")
        initial_pos_read = random.randint(sevfive_ref_pos +1, ref_length - read_len ) # Initial position for read from the last 25% of the reference
        final_pos_read = initial_pos_read + read_len -1
        #print("Ïnitial position : ", initial_pos_read)
        #print("Final position : ", final_pos_read)
        read = reference_list[initial_pos_read : final_pos_read + 1]
        read_string = "".join(read)
        reads[current_n_reads] = read_string
        align_two += 1 # Count new read that aligns twice
    else:
        # Generate a read that does not align
        #print("Caso 3")
        read_in_ref = 0 # Value to determine if an alignment was found
        while read_in_ref != -1: # While new read is found in the reference
            read = list(0 for i in range(read_len)) # Generate a read list with the corresponding letters
            for i in range(read_len): # Fill the read list randomly
                read[i] = random.randint(0,3)
                read = ['A' if data == 0 else data for data in read]
                read = ['C' if data == 1 else data for data in read]
                read = ['G' if data == 2 else data for data in read]
                read = ['T' if data == 3 else data for data in read]
                #reference_string = ""
            #for k in reference_list:
                #reference_string += str(k) + ""
                
            reference_string = str(reference_string)
            #print("Printing reference string: ", reference_string)
            read_string = "".join(read)
            #print("Printing read string : ", read_string)
            read_in_ref = reference_string.find(read_string) # If read find in the reference, then != 1
            
        reads[current_n_reads] = read_string 
        align_cero +=1 # Count new read that does not align
        
    #print("Printing new read string : ", reads[current_n_reads])    
    reads_file.write(reads[current_n_reads] + "\n")
    current_n_reads += 1


reads_file.close
ref_file.close

align_cero_frac = align_cero/nreads
align_one_frac = align_one/nreads
align_two_frac = align_two/nreads

print("reference length: ", ref_length)
print("number reads: ", nreads)
print("read length: ", read_len)
print("aligns 0: ", align_cero_frac)
print("aligns_1: ", align_one_frac)
print("aligns_2: ", align_two_frac)
#print("reference_string: ", reference_string)


        

        

        
