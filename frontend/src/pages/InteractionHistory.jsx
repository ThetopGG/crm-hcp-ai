import React, { useEffect, useState } from "react";
import {
  Typography,
  Box,
  Paper,
  Grid,
  TextField,
  Button,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  CircularProgress,
} from "@mui/material";
import MainLayout from "../components/Layout/MainLayout";
import api from "../api/axios";

export default function InteractionHistory() {
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ doctor: "", product: "", keyword: "" });

  const fetchAll = async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/api/interactions/");
      setInteractions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filters.doctor) params.doctor = filters.doctor;
      if (filters.product) params.product = filters.product;
      if (filters.keyword) params.keyword = filters.keyword;
      const { data } = await api.get("/api/search/interactions", { params });
      setInteractions(data.results);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAll();
  }, []);

  return (
    <MainLayout>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 0.5 }}>
        Interaction History
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Browse and search all logged interactions.
      </Typography>

      <Paper sx={{ p: 2.5, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              label="Doctor"
              size="small"
              value={filters.doctor}
              onChange={(e) => setFilters({ ...filters, doctor: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              label="Product"
              size="small"
              value={filters.product}
              onChange={(e) => setFilters({ ...filters, product: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              label="Keyword"
              size="small"
              value={filters.keyword}
              onChange={(e) => setFilters({ ...filters, keyword: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} sm={3} sx={{ display: "flex", gap: 1 }}>
            <Button variant="contained" onClick={handleSearch} fullWidth>
              Search
            </Button>
            <Button variant="outlined" onClick={fetchAll}>
              Reset
            </Button>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 0, overflow: "hidden" }}>
        {loading ? (
          <Box sx={{ display: "flex", justifyContent: "center", py: 6 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Doctor</TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Products</TableCell>
                <TableCell>Outcome</TableCell>
                <TableCell>Follow-up</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {interactions.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    No interactions found.
                  </TableCell>
                </TableRow>
              )}
              {interactions.map((i) => (
                <TableRow key={i.id} hover>
                  <TableCell>{i.hcp?.name || i.doctor_name || "—"}</TableCell>
                  <TableCell>{i.interaction_date}</TableCell>
                  <TableCell>
                    <Chip size="small" label={i.interaction_type} />
                  </TableCell>
                  <TableCell>{i.products_discussed || "—"}</TableCell>
                  <TableCell>{i.outcome || "—"}</TableCell>
                  <TableCell>{i.follow_up_date || "—"}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Paper>
    </MainLayout>
  );
}
