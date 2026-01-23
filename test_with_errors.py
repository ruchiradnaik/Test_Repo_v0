"""
This file has intentional errors to test CodeSentinel's fixing capabilities.
"""
import pandas as pd
import numpy as np
import cv2
from user_service import UserService

def test_user_creation():
    """Test creating a user - this function has an error."""
    service = UserService()
    # Fixed: added the required argument 'email'
    user = service.create_user("testuser", "testuser@example.com")
    return user

def process_data():
    """Process some data using pandas and numpy."""
    # This will work if pandas and numpy are installed
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    result = np.mean(df['a'])
    return result

def image_processing():
    """Process an image using OpenCV."""
    # This will work if opencv-python is installed
    img = cv2.imread('test.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

if __name__ == '__main__':
    # This will now work after fixing the error in test_user_creation
    user = test_user_creation()
    print(f"Created user: {user}")

# CodeSentinal: created for you by RuchirAdnaik.