import React, { useEffect, useState } from "react";
import {
  Typography,
  Box,
  TextField,
  InputAdornment,
  Grid,
  Card,
  CardContent,
  Avatar,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import AddIcon from "@mui/icons-material/Add";
import LocalHospitalIcon from "@mui/icons-material/LocalHospitalOutlined";
import { useDispatch, useSelector } from "react-redux";
import MainLayout from "../components/Layout/MainLayout";
import api from "../api/axios";
import { setHCPs, setLoading } from "../store/slices/hcpSlice";

export default function HCPList() {
  const dispatch = useDispatch();
  const { hcps, loading } = useSelector((state) => state.hcp);
  const [search, setSearch] = useState("");
  const [openDialog, setOpenDialog] = useState(false);
  const [form, setForm] = useState({ name: "", speciality: "", hospital: "", city: "", phone: "", email: "" });

  const fetchHCPs = async (query = "") => {
    dispatch(setLoading(true));
    try {
      const { data } = await api.get("/api/hcps/", { params: query ? { search: query } : {} });
      dispatch(setHCPs(data));
    } catch (err) {
      console.error(err);
    } finally {
      dispatch(setLoading(false));
    }
  };

  useEffect(() => {
    fetchHCPs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
    fetchHCPs(e.target.value);
  };

  const handleCreate = async () => {
    try {
      await api.post("/api/hcps/", form);
      setOpenDialog(false);
      setForm({ name: "", speciality: "", hospital: "", city: "", phone: "", email: "" });
      fetchHCPs(search);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <MainLayout>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3, flexWrap: "wrap", gap: 2 }}>
        <Box>
          <Typography variant="h5" fontWeight={700}>
            HCP List
          </Typography>
          <Typography variant="body2" color="text.secondary">
            All health care professionals in your territory.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => setOpenDialog(true)}>
          Add HCP
        </Button>
      </Box>

      <TextField
        fullWidth
        placeholder="Search by name, hospital, or speciality..."
        value={search}
        onChange={handleSearchChange}
        sx={{ mb: 3, maxWidth: 480 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon fontSize="small" />
            </InputAdornment>
          ),
        }}
      />

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 6 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={2.5}>
          {hcps.length === 0 && (
            <Grid item xs={12}>
              <Typography color="text.secondary">No HCPs found. Add one to get started.</Typography>
            </Grid>
          )}
          {hcps.map((hcp) => (
            <Grid item xs={12} sm={6} md={4} key={hcp.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: "flex", gap: 1.5, alignItems: "center", mb: 1.5 }}>
                    <Avatar sx={{ bgcolor: "primary.main" }}>
                      <LocalHospitalIcon fontSize="small" />
                    </Avatar>
                    <Box>
                      <Typography fontWeight={600}>{hcp.name}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {hcp.speciality || "Speciality not set"}
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {hcp.hospital || "Hospital not set"} {hcp.city ? `• ${hcp.city}` : ""}
                  </Typography>
                  <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                    {hcp.phone && <Chip size="small" label={hcp.phone} />}
                    {hcp.email && <Chip size="small" label={hcp.email} />}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} fullWidth maxWidth="sm">
        <DialogTitle>Add New HCP</DialogTitle>
        <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: 1 }}>
          <TextField label="Name" fullWidth value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <TextField label="Speciality" fullWidth value={form.speciality} onChange={(e) => setForm({ ...form, speciality: e.target.value })} />
          <TextField label="Hospital" fullWidth value={form.hospital} onChange={(e) => setForm({ ...form, hospital: e.target.value })} />
          <TextField label="City" fullWidth value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
          <TextField label="Phone" fullWidth value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <TextField label="Email" fullWidth value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleCreate} disabled={!form.name}>
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </MainLayout>
  );
}
