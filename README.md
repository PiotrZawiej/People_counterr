# Body_counter

This project implements an asynchronous image processing system using FastAPI and RabbitMQ. It allows users to submit image URLs for people detection, which are then processed in the background by a worker. The system tracks the progress of each task and provides a way to check the status and result of the detection.

#Key Features:
  Submit image URLs for people detection: Users can send image URLs to the system to detect the number of people in the image.
  Asynchronous task processing: The tasks are added to a RabbitMQ queue and processed by a worker in the background.
  Task status tracking: Users can check the status of the task and retrieve the number of detected people once processing is complete.
  Error handling: In case of errors, the system handles failed tasks and provides appropriate feedback.
  
#Tech Stack:
  FastAPI: Used for building the REST API to interact with users.
  RabbitMQ: Handles task queuing and background processing.
  Python: The core programming language for implementing the logic.
  
#How it Works:
  Add a Task: Use the /add_task endpoint to submit a URL of an image for processing.
  Task Processing: The image is processed asynchronously by the worker. The number of detected people is stored in a global result store.
  Get Result: Use the /get_result endpoint to check the status of the task or retrieve the number of detected people once the task is completed.
  
#Usage:
  Start the RabbitMQ service.
  Run the FastAPI application.
  Use the /add_task endpoint to submit an image URL.
  Use the /get_result endpoint to check the status of the task and retrieve the result.
