import React from "react";
import { useSelector } from "react-redux";
import { Typography, Paper, Grid, TextField, Box, Chip } from "@mui/material";
import MainLayout from "../components/Layout/MainLayout";

export default function Settings() {
  const user = useSelector((state) => state.auth.user);

  return (
    <MainLayout>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 0.5 }}>
        Settings
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Manage your account and view AI configuration.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Profile
            </Typography>
            <TextField fullWidth label="Full Name" value={user?.full_name || ""} margin="normal" disabled />
            <TextField fullWidth label="Email" value={user?.email || ""} margin="normal" disabled />
            <TextField fullWidth label="Role" value={user?.role || ""} margin="normal" disabled />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              AI Configuration
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              Current LLM provider: <b>Groq</b>
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Model is configured on the backend via the <code>GROQ_MODEL</code> environment variable.
            </Typography>
            <Box sx={{ display: "flex", gap: 1 }}>
              <Chip label="gemma2-9b-it (default)" color="primary" variant="outlined" />
              <Chip label="llama-3.3-70b-versatile" variant="outlined" />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </MainLayout>
  );
}
