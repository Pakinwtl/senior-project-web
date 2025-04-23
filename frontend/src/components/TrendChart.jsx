// src/components/TrendChart.jsx
import React from "react";
import { Line } from "react-chartjs-2";
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
  if (!trend) return null;
  console.log("Trend data:", trend);

  const data = {
    labels: trend.wavelengths,
    datasets: [
      {
        label: "Transmittance",
        data: trend.transmittance,
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
        text: `Trend Sample ${trend.sample_index}`,
      },
    },
  };

  return <Line data={data} options={options} />;
}

export default TrendChart;
