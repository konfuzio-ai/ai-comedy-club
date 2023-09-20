def filter_lines(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    filtered_lines = [line for line in lines if '?' in line]

    with open(output_file, 'w') as file:
        file.writelines(filtered_lines)

input_filename = './data/chatgpt_jokes.txt'  # Replace with your input file name
output_filename = './data/chatgpt_jokes_cleaned.txt'  # Replace with your output file name

filter_lines(input_filename, output_filename)
print(f"Filtered lines have been saved to {output_filename}")
