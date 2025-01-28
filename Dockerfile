FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SpaCy model and PyTorch dependencies
RUN python -m spacy download en_core_web_trf
RUN pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu

# Copy the application code into the container
COPY . /app/

# Command to run the Streamlit app
CMD ["streamlit", "run", "app/main.py"]
