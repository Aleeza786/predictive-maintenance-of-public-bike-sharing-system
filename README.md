# predictive-maintenance-of-public-bike-sharing-system
1. Introduction
The Predictive Maintenance for Public Bike Sharing System project is developed to forecast potential failures in shared bike components such as brakes, chains, and tires. By predicting failures before they occur, the system helps in reducing downtime, increasing operational efficiency, and minimizing maintenance costs.
2. Objective
To build a machine learning-based predictive model that estimates failure probabilities for various bike components and integrates it with a web-based dashboard for visualization and maintenance management.
3. Tools and Technologies Used
• Frontend: React.js (Vite) for interactive dashboard
• Backend: FastAPI for serving APIs
• Database: PostgreSQL for data storage
• Machine Learning: Scikit-learn, Pandas, NumPy, XGBoost
• Programming Languages: Python, JavaScript
4. System Architecture
The system consists of:
• Frontend Dashboard – built with React and Tailwind CSS
• Backend Server – built with FastAPI to handle API requests
• Machine Learning Module – processes input data and predicts failure probabilities
• Database – stores bike details, component risk levels, and maintenance records
5. Features
• Predicts failure probability of each bike component
• Displays real-time maintenance risk dashboard
• Allows visualization through pie charts and tables
• Stores and retrieves maintenance data efficiently
• Provides component-specific risk analysis
6. Dataset
A synthetic dataset (train.csv) was generated using Python scripts under 'data-gen' folder. It simulates component performance metrics and failure outcomes to train machine learning models.
7. Model Development
An XGBoost Classifier was used for component-wise failure prediction. The model was trained using labeled data and evaluated with ROC-AUC metrics to ensure prediction reliability.
8. Results
The dashboard visualizes component risk levels in an easily understandable format. It highlights high-risk bikes for timely maintenance actions and supports decision-making for efficient operations.
9. Conclusion
The system successfully predicts potential failures, visualizes component risk, and enhances the maintenance process. It demonstrates the power of AI in optimizing public bike-sharing systems through predictive analytics.
10. Future Enhancements
• Integration with IoT sensors for live monitoring
• Cloud deployment for scalability
• Mobile app version for real-time access
• Deep learning models for improved accuracy
