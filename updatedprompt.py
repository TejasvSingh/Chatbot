import json

# Input and output file paths
input_file = "training_data.jsonl"  # Replace with your actual file path
output_file = "updatedprompt.jsonl"

# System message content
system_message = {
    "role": "system",
    "content": "You are a helpful assistant specializing in guiding students around the Texas A&M University-Corpus Christi campus."
}

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        # Parse each line as JSON
        data = json.loads(line.strip())
        
        # Convert to the new format, adding "content" fields and the system message
        chat_format = {
            "messages": [
                system_message,  # Add the system message at the start
                {"role": "user", "content": data["prompt"]},
                {"role": "assistant", "content": data["completion"]}
            ]
        }
        
        # Write the new format to the output file
        outfile.write(json.dumps(chat_format) + "\n")

print(f"Data has been successfully converted and saved to {output_file} with system messages added.")
