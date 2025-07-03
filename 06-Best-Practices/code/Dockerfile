FROM public.ecr.aws/lambda/python:3.9

# Upgrade pip and install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Set working directory (optional but recommended)
WORKDIR /var/task

# Copy Pipenv files and install dependencies system-wide
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

# Copy application files
COPY lambda_function.py model.py ./

# Command to run Lambda
CMD [ "lambda_function.lambda_handler" ]
