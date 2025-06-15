import React from "react";
import AppSidebar from "./AppSidebar"; // Importa el sidebar
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

const App = () => {
  return (
    <Router>
      <div style={{ display: "flex" }}>
        <AppSidebar /> {/* Sidebar fijo */}
        <div style={{ flexGrow: 1, padding: "20px" }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/tiempo-real" element={<TiempoReal />} />
            <Route path="/tendencias" element={<Tendencias />} />
            <Route path="/estadisticas" element={<Estadisticas />} />
            <Route path="/factor-carga" element={<FactorCarga />} />
            <Route path="/iec-61000-4-30" element={<ReportesIEC />} />
            <Route path="/otros-reportes" element={<OtrosReportes />} />
            <Route path="/perfil" element={<Perfil />} />
            <Route path="/accesos" element={<Accesos />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
