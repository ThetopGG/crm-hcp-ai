import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import ProtectedRoute from "./components/Layout/ProtectedRoute";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import HCPList from "./pages/HCPList";
import InteractionHistory from "./pages/InteractionHistory";
import LogInteraction from "./pages/LogInteraction";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/hcps"
        element={
          <ProtectedRoute>
            <HCPList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <InteractionHistory />
          </ProtectedRoute>
        }
      />
      <Route
        path="/log-interaction"
        element={
          <ProtectedRoute>
            <LogInteraction />
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <Settings />
          </ProtectedRoute>
        }
      />

      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
