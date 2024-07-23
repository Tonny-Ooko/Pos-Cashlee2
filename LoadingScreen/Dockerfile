FROM python:3.10-slim                                                                                         

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \                          
    libmariadb-dev \                      
    libmariadb-dev-compat \       
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app                                      
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app            

CMD ["python", "app.py"]
