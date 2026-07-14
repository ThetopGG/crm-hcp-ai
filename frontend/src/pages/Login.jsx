import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  Tabs,
  Tab,
  CircularProgress,
} from "@mui/material";
import MedicalServicesIcon from "@mui/icons-material/MedicalServicesOutlined";
import api from "../api/axios";
import { setCredentials } from "../store/slices/authSlice";

export default function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [tab, setTab] = useState(0); // 0 = login, 1 = register
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const endpoint = tab === 0 ? "/api/auth/login" : "/api/auth/register";
      const payload =
        tab === 0
          ? { email, password }
          : { full_name: fullName, email, password };

      const { data } = await api.post(endpoint, payload);
      dispatch(setCredentials(data));
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #3454D1 0%, #17B890 100%)",
        p: 2,
      }}
    >
      <Paper sx={{ p: 5, width: 420, borderRadius: 4 }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.2, mb: 1 }}>
          <MedicalServicesIcon color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>
            CRM HCP AI
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          AI-first CRM for pharmaceutical field representatives
        </Typography>

        <Tabs value={tab} onChange={(e, v) => setTab(v)} sx={{ mb: 3 }}>
          <Tab label="Login" />
          <Tab label="Register" />
        </Tabs>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          {tab === 1 && (
            <TextField
              fullWidth
              required
              label="Full Name"
              margin="normal"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
          )}
          <TextField
            fullWidth
            required
            type="email"
            label="Email"
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            fullWidth
            required
            type="password"
            label="Password"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button
            fullWidth
            type="submit"
            variant="contained"
            size="large"
            disabled={loading}
            sx={{ mt: 3, py: 1.2 }}
          >
            {loading ? <CircularProgress size={22} color="inherit" /> : tab === 0 ? "Login" : "Create Account"}
          </Button>
        </Box>

        <Typography variant="caption" color="text.secondary" sx={{ mt: 3, display: "block", textAlign: "center" }}>
          Demo tip: Register a new account, then log in to explore the AI assistant.
        </Typography>
      </Paper>
    </Box>
  );
}
