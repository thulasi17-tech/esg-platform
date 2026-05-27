import { useEffect, useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

import {
  FaLeaf,
  FaCloud,
  FaChartBar,
  FaExclamationTriangle,
  FaUpload,
} from "react-icons/fa";

import "./App.css";

function App() {

  const [summary, setSummary] = useState({});
  const [topCategories, setTopCategories] = useState([]);
  const [flagged, setFlagged] = useState(0);

  const [alerts, setAlerts] = useState([]);

  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {

    if (!token) {
      window.location.href = "/";
    }

    fetchSummary();
    fetchTopCategories();
    fetchFlaggedRecords();
    fetchAlerts();

  }, []);

  const handleLogout = () => {

    localStorage.removeItem("token");

    window.location.href = "/";
  };

  const fetchSummary = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/api/emissions/summary/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setSummary(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  const fetchTopCategories = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/api/emissions/top-categories/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setTopCategories(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  const fetchFlaggedRecords = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/api/emissions/flagged-records/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setFlagged(response.data.flagged_records);

    } catch (error) {

      console.log(error);
    }
  };

  const fetchAlerts = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/api/emissions/alerts/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setAlerts(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  const handleFileUpload = async () => {

    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append("company_id", 1);
    formData.append("source_type", "SAP");

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/api/ingestion/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setUploadMessage(response.data.message);

      fetchSummary();
      fetchTopCategories();
      fetchFlaggedRecords();
      fetchAlerts();

    } catch (error) {

      console.log(error);

      setUploadMessage("Upload failed");
    }
  };

  return (

    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background: "#001233",
        color: "white",
      }}
    >

      {/* SIDEBAR */}

      <div
        style={{
          width: "250px",
          background: "#001845",
          padding: "30px 20px",
        }}
      >

        <h2 style={{ color: "#00d084" }}>
          <FaLeaf /> ESG Platform
        </h2>

        <div style={{ marginTop: "50px" }}>

          <p style={{ marginBottom: "30px", fontSize: "22px" }}>
            <FaCloud /> Dashboard
          </p>

          <p style={{ marginBottom: "30px", fontSize: "22px" }}>
            <FaLeaf /> Emissions
          </p>

          <p style={{ marginBottom: "30px", fontSize: "22px" }}>
            <FaChartBar /> Analytics
          </p>

          <p style={{ marginBottom: "30px", fontSize: "22px" }}>
            <FaExclamationTriangle /> Alerts
          </p>

        </div>

        <button
          onClick={handleLogout}
          style={{
            marginTop: "50px",
            padding: "12px",
            width: "100%",
            background: "#ff4d4f",
            border: "none",
            color: "white",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "18px",
          }}
        >
          Logout
        </button>

      </div>

      {/* MAIN CONTENT */}

      <div
        style={{
          flex: 1,
          padding: "40px",
        }}
      >

        <h1
          style={{
            textAlign: "center",
            marginBottom: "40px",
            fontSize: "60px",
          }}
        >
          ESG Analytics Dashboard
        </h1>

        {/* CSV Upload */}

        <div
          style={{
            background: "#1b2a41",
            padding: "30px",
            borderRadius: "20px",
            marginBottom: "40px",
            textAlign: "center",
          }}
        >

          <h2>
            <FaUpload /> Upload ESG CSV
          </h2>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            style={{
              marginTop: "20px",
            }}
          />

          <br />

          <button
            onClick={handleFileUpload}
            style={{
              marginTop: "20px",
              padding: "12px 30px",
              background: "#00d084",
              border: "none",
              color: "white",
              borderRadius: "10px",
              cursor: "pointer",
              fontSize: "18px",
            }}
          >
            Upload CSV
          </button>

          <p style={{ marginTop: "20px" }}>
            {uploadMessage}
          </p>

        </div>

        {/* KPI CARDS */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: "20px",
          }}
        >

          <div className="card">
            <h2>Total Emissions</h2>

            <h1 style={{ color: "#00d084" }}>
              {summary.total_emissions?.toFixed(2)}
            </h1>
          </div>

          <div className="card">
            <h2>Scope 1</h2>

            <h1 style={{ color: "#00d084" }}>
              {summary.scope1?.toFixed(2)}
            </h1>
          </div>

          <div className="card">
            <h2>Scope 2</h2>

            <h1 style={{ color: "#00d084" }}>
              {summary.scope2?.toFixed(2)}
            </h1>
          </div>

          <div className="card">
            <h2>Scope 3</h2>

            <h1 style={{ color: "#00d084" }}>
              {summary.scope3?.toFixed(2)}
            </h1>
          </div>

          <div className="card">
            <h2>Flagged Records</h2>

            <h1 style={{ color: "red" }}>
              {flagged}
            </h1>
          </div>

        </div>

        {/* ALERTS PANEL */}

        <div
          style={{
            marginTop: "40px",
            background: "#1b2a41",
            padding: "25px",
            borderRadius: "20px",
          }}
        >

          <h1 style={{ color: "#ff4d4f" }}>
            ESG Alerts
          </h1>

          {
            alerts.length === 0 ? (
              <p>No active alerts</p>
            ) : (
              alerts.map((alert, index) => (

                <div
                  key={index}
                  style={{
                    background: "#2a3d5f",
                    padding: "15px",
                    marginTop: "15px",
                    borderRadius: "10px",
                  }}
                >

                  <h3>
                    ⚠ {alert.category}
                  </h3>

                  <p>{alert.reason}</p>

                  <p>Scope: {alert.scope}</p>

                  <p>CO2e: {alert.co2e}</p>

                </div>
              ))
            )
          }

        </div>

        {/* CHART */}

        <div
          style={{
            marginTop: "50px",
            background: "#1b2a41",
            padding: "30px",
            borderRadius: "20px",
          }}
        >

          <h1
            style={{
              textAlign: "center",
              marginBottom: "30px",
            }}
          >
            Top Emission Categories
          </h1>

          <ResponsiveContainer width="100%" height={400}>

            <BarChart data={topCategories}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="category" />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="total_emissions"
                fill="#00d084"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

    </div>
  );
}

export default App;