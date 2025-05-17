# AI-based Data Analysis for Optical Fiber Sensor in VOC Biomarker Detection (https://senior-project-website.onrender.com/)

This project is a web-based application for detecting VOC (Volatile Organic Compounds) using optical fiber sensor data. It allows users to upload experimental data and select the detection methods to detect redshift-based trends.
**FOR MORE DETAIL FOLLOW PDF FILE**

## Project Overview

- **Frontend**: React.js
- **Backend**: FastAPI (Python)
- **ML Models**: Support Vector Machine (SVM), K-Nearest Neighbors (KNN)
- **Data**: Light Intensity VS wavelength from optical fiber sensor
- **Use Case**: Helps analyze spectroscopic data from sensors to identify diabetes (VOC presence)

## Features

- Upload Excel file containing right format sensor data
- Choose between Algorithmic or AI-based trend detection
- Visualize detected trend on interactive graphs
- View and switch between detected trend samples

## How it works

1. Users upload `.xlsx` file with data in specific template format
2. Backend processes the data using a smoothing algorithm
3. Either:
   - **Simple Algorithm**: detects trend by observing redshift in transmittance minimum points
   - **SVM Model**: classifies the trend based on learned patterns
4. Results are shown as a list of detected trend, with each one visualized in a graph

## Why Not Deep Learning 

Although deep learning (CNN, LSTM) was initially considered, it was ruled out due to:
- Limited data (~20,000 samples)
- Low complexity of the trend pattern
- Excellent performance already achieved by SVM

## Project Structure

backend/
└── app/
├── main.py
├── services/
├── utils/
└── models/
frontend/
└── src/
├── components/
├── App.jsx
├── styles/

## Technologies Used

| Frontend        | Backend     | ML Libraries          |
|----------------|-------------|------------------------|
| React.js       | FastAPI     | scikit-learn, joblib   |
| Chart.js       | Uvicorn     | pandas, numpy          |
| Axios          | CORS        | statsmodels, scipy     |

## Deployment

Backend and frontend can be deployed via services **Render**

## Author

Pakin Wattaleela (Tar) -- Chulalongkorn University ISE, Nano
With guidance from academic advisors and inspiration from VOC sensing research:
https://doi.org/10.3390/s23187916

