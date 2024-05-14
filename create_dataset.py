import pandas as pd
import numpy as np

# Define parameters for the dataset
num_properties = 1000
np.random.seed(42)

# Generate random data
latitude = np.random.uniform(low=34.0, high=38.0, size=num_properties)
longitude = np.random.uniform(low=-118.5, high=-121.5, size=num_properties)
price = np.random.uniform(low=100000, high=2000000, size=num_properties).astype(int)
size = np.random.uniform(low=500, high=5000, size=num_properties).astype(int)
property_type = np.random.choice(['House', 'Apartment', 'Condo', 'Townhouse'], size=num_properties)

# Create a DataFrame
data = {
    'latitude': latitude,
    'longitude': longitude,
    'price': price,
    'size': size,
    'type': property_type
}
df = pd.DataFrame(data)

# Save the dataset to a CSV file
df.to_csv('real_estate_data.csv', index=False)
