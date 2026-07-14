import React from "react";
import { Paper, Typography, TextField, MenuItem, Button, Grid, Box } from "@mui/material";
import SaveIcon from "@mui/icons-material/Save";

const INTERACTION_TYPES = ["Visit", "Call", "Email", "Video"];

export default function StructuredForm({ form, onChange, onSave, saving }) {
  const handleChange = (field) => (e) => onChange({ ...form, [field]: e.target.value });

  return (
    <Paper sx={{ p: 3, height: "100%" }}>
      <Typography variant="h6" sx={{ mb: 0.5 }}>
        Interaction Details
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Fill manually, or let the AI assistant auto-fill this from your conversation.
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField fullWidth label="Doctor Name" value={form.doctor_name || ""} onChange={handleChange("doctor_name")} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField fullWidth label="Speciality" value={form.speciality || ""} onChange={handleChange("speciality")} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField fullWidth label="Hospital" value={form.hospital || ""} onChange={handleChange("hospital")} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            type="date"
            label="Interaction Date"
            InputLabelProps={{ shrink: true }}
            value={form.interaction_date || ""}
            onChange={handleChange("interaction_date")}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            select
            fullWidth
            label="Interaction Type"
            value={form.interaction_type || "Visit"}
            onChange={handleChange("interaction_type")}
          >
            {INTERACTION_TYPES.map((t) => (
              <MenuItem key={t} value={t}>
                {t}
              </MenuItem>
            ))}
          </TextField>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="Products Discussed"
            placeholder="e.g. CardX, Renovax"
            value={form.products_discussed || ""}
            onChange={handleChange("products_discussed")}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField fullWidth multiline minRows={2} label="Notes" value={form.notes || ""} onChange={handleChange("notes")} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField fullWidth label="Outcome" value={form.outcome || ""} onChange={handleChange("outcome")} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            type="date"
            label="Follow-up Date"
            InputLabelProps={{ shrink: true }}
            value={form.follow_up_date || ""}
            onChange={handleChange("follow_up_date")}
          />
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: "flex", justifyContent: "flex-end" }}>
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={onSave}
          disabled={saving || !form.doctor_name}
          size="large"
        >
          {saving ? "Saving..." : "Save Interaction"}
        </Button>
      </Box>
    </Paper>
  );
}
