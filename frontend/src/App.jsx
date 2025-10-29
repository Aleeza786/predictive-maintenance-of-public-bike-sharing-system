import React, { useEffect, useState } from "react";
import Header from "./components/Header";
import RiskPieChart from "./components/RiskPieChart";
import RiskTable from "./components/RiskTable";
import MaintenanceTable from "./components/MaintenanceTable";
import axios from "axios";

const App = () => {
  const [riskData, setRiskData] = useState([]);
  const [maintenance, setMaintenance] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/scores/at-risk")
      .then(res => setRiskData(res.data))
      .catch(() => console.log("Error loading risk data"));
    axios.get("http://127.0.0.1:8000/maintenance/records")
      .then(res => setMaintenance(res.data))
      .catch(() => console.log("Error loading maintenance"));
  }, []);

  return (
    <div className="min-h-screen p-6 bg-background">
      <Header />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <div className="bg-white p-6 rounded-2xl shadow-lg">
          <h2 className="text-xl font-semibold text-primary mb-4">Bike Component Risk Overview</h2>
          <RiskPieChart data={riskData} />
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-lg">
          <h2 className="text-xl font-semibold text-accent mb-4">Recent Maintenance Records</h2>
          <MaintenanceTable data={maintenance} />
        </div>
      </div>
      <div className="bg-white p-6 mt-6 rounded-2xl shadow-lg">
        <h2 className="text-xl font-semibold text-success mb-4">High Risk Bikes</h2>
        <RiskTable data={riskData} />
      </div>
    </div>
  );
};

export default App;
