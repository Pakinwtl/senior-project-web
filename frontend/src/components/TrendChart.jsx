// src/components/TrendChart.jsx
import React from "react";
import { Line } from "react-chartjs-2";
import "../styles/TrendChart.css"; // Assuming you have some CSS for styling
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend
);

function TrendChart({ trend }) {
  if (!trend) {
    return (
      <div className="trend-chart">
        <p style={{ color: "#888" }}>📈 Select a trend to see details</p>
      </div>
    );
  }

  const data = {
    labels: trend.concentrations,
    datasets: [
      {
        label: "Wavelength",
        data: trend.wavelengths,
        fill: false,
        borderColor: "blue",
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: `Trend Sample`,
      },
    },
  };

  return (
    <div className="trend-chart">
      <Line data={data} options={options} />;
    </div>
  );
}

export default TrendChart;
