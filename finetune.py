import openai
import time

# Replace with your OpenAI API key
openai.api_key = 'sk-vFey-R3pjo-cjOpALdmoP0pa7QhVDaVydpntGUQ2X9T3BlbkFJAeHyrr4PaFCXJoMm8qTuKzlr4M5QmaUDWgqJfZo2EA'

# Step 1: Upload Dataset
def upload_dataset(file_path):
    try:
        # Upload the dataset for fine-tuning
        with open(file_path, "rb") as f:
            response = openai.File.create(
                file=f,
                purpose='fine-tune'
            )
        print(f"Dataset uploaded successfully! File ID: {response['id']}")
        return response['id']
    except Exception as e:
        print(f"Error uploading dataset: {e}")
        return None


# Step 2: Fine-Tune the Model
def fine_tune_model(training_file_id):
    try:
        # Fine-tune the model
        fine_tune_response = openai.FineTune.create(
            training_file=training_file_id,
            model="davinci"  # You can choose other models like "curie", "babbage", etc.
        )
        print(f"Fine-tuning started! Fine-tune Job ID: {fine_tune_response['id']}")
        return fine_tune_response['id']
    except Exception as e:
        print(f"Error during fine-tuning: {e}")
        return None


# Step 3: Monitor Fine-Tuning Job
def monitor_fine_tuning_job(fine_tune_job_id):
    try:
        # Monitor the fine-tuning job status
        while True:
            status = openai.FineTune.retrieve(id=fine_tune_job_id)
            if status['status'] == 'succeeded':
                print("Fine-tuning completed successfully!")
                return status['fine_tuned_model']
            elif status['status'] == 'failed':
                print("Fine-tuning failed!")
                return None
            else:
                print("Fine-tuning in progress...")
                time.sleep(30)  # Check every 30 seconds
    except Exception as e:
        print(f"Error monitoring fine-tuning job: {e}")
        return None


# Step 4: Use Fine-Tuned Model
def use_fine_tuned_model(model_id, prompt):
    try:
        # Use the fine-tuned model to get a response
        response = openai.Completion.create(
            model=model_id,
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error using the fine-tuned model: {e}")
        return None


# Main Function
def main():
    # Step 1: Upload the dataset (your `training_data.jsonl`)
    file_path = "training_data.jsonl"  # Path to your dataset file
    training_file_id = upload_dataset(file_path)
    
    if training_file_id:
        # Step 2: Fine-tune the model
        fine_tune_job_id = fine_tune_model(training_file_id)
        
        if fine_tune_job_id:
            # Step 3: Monitor the fine-tuning process
            fine_tuned_model_id = monitor_fine_tuning_job(fine_tune_job_id)
            
            if fine_tuned_model_id:
                # Step 4: Use the fine-tuned model for generating a response
                prompt = "Where is Island Hall?"  # Example prompt
                response = use_fine_tuned_model(fine_tuned_model_id, prompt)
                
                if response:
                    print(f"Response from fine-tuned model: {response}")
                else:
                    print("Failed to get a response from the fine-tuned model.")
            else:
                print("Fine-tuning process failed.")
        else:
            print("Fine-tuning job failed to start.")
    else:
        print("Dataset upload failed.")


if __name__ == '__main__':
    main()
