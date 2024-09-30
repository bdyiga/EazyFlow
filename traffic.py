import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from datetime import datetime, timedelta


class TrafficLightAI:
    def __init__(self):
        self.model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000)
        self.scaler = StandardScaler()
        
    def preprocess_data(self, data):
        # Extract features: hour, day of week, vehicle count
        features = []
        for entry in data:
            dt = entry['timestamp']
            features.append([
                dt.hour,
                dt.weekday(),
                entry['vehicle_count']
            ])
        return np.array(features)
    
    def train(self, historical_data):
        X = self.preprocess_data(historical_data)
        y = np.array([entry['optimal_green_time'] for entry in historical_data])
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict_green_time(self, current_data):
        X = self.preprocess_data([current_data])
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)[0]

def simulate_traffic():
    # Simulate traffic data for demonstration
    now = datetime.now()
    return {
        'timestamp': now,
        'vehicle_count': np.random.randint(0, 50)
    }

def main():
    ai = TrafficLightAI()
    
    # Simulate historical data
    historical_data = []
    start_date = datetime.now() - timedelta(days=30)
    for i in range(1000):
        timestamp = start_date + timedelta(minutes=30*i)
        historical_data.append({
            'timestamp': timestamp,
            'vehicle_count': np.random.randint(0, 50),
            'optimal_green_time': np.random.randint(30, 120)
        })
    
    # Train the model
    ai.train(historical_data)
    
    # Simulate real-time prediction
    current_data = simulate_traffic()
    predicted_green_time = ai.predict_green_time(current_data)
    
    print(f"Current time: {current_data['timestamp']}")
    print(f"Vehicle count: {current_data['vehicle_count']}")
    print(f"Predicted optimal green light duration: {predicted_green_time:.2f} seconds")

# Call the function.
if __name__ == "__main__":
    main()