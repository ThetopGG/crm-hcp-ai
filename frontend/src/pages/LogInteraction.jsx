import React, { useState } from "react";
import { Typography, Box, Grid, Snackbar, Alert } from "@mui/material";
import MainLayout from "../components/Layout/MainLayout";
import StructuredForm from "../components/LogInteraction/StructuredForm";
import AIChatPanel from "../components/LogInteraction/AIChatPanel";
import api from "../api/axios";

const emptyForm = {
  doctor_name: "",
  speciality: "",
  hospital: "",
  interaction_date: new Date().toISOString().slice(0, 10),
  interaction_type: "Visit",
  products_discussed: "",
  notes: "",
  outcome: "",
  follow_up_date: "",
};

export default function LogInteraction() {
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [currentInteractionId, setCurrentInteractionId] = useState(null);
  const [toast, setToast] = useState({ open: false, message: "", severity: "success" });

  const handleFormExtracted = (extracted, chatData) => {
    setForm((prev) => ({ ...prev, ...extracted }));
    if (chatData?.data?.interaction_id) {
      setCurrentInteractionId(chatData.data.interaction_id);
    }
    setToast({ open: true, message: "Form auto-filled by AI assistant. Review and save.", severity: "info" });
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      // First, resolve/create the HCP by name so we have a valid hcp_id.
      const hcpSearch = await api.get("/api/hcps/", { params: { search: form.doctor_name } });
      let hcpId = hcpSearch.data.find((h) => h.name.toLowerCase() === form.doctor_name.toLowerCase())?.id;

      if (!hcpId) {
        const created = await api.post("/api/hcps/", {
          name: form.doctor_name,
          speciality: form.speciality || null,
          hospital: form.hospital || null,
        });
        hcpId = created.data.id;
      }

      const payload = {
        hcp_id: hcpId,
        interaction_date: form.interaction_date,
        interaction_type: form.interaction_type,
        products_discussed: form.products_discussed || null,
        notes: form.notes || null,
        outcome: form.outcome || null,
        follow_up_date: form.follow_up_date || null,
      };

      if (currentInteractionId) {
        await api.put(`/api/interactions/${currentInteractionId}`, payload);
      } else {
        const res = await api.post("/api/interactions/", payload);
        setCurrentInteractionId(res.data.id);
      }

      setToast({ open: true, message: "Interaction saved successfully!", severity: "success" });
    } catch (err) {
      console.error(err);
      setToast({ open: true, message: "Failed to save interaction.", severity: "error" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <MainLayout>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 0.5 }}>
        Log Interaction
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Use the structured form or chat naturally with the AI assistant on the right.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <StructuredForm form={form} onChange={setForm} onSave={handleSave} saving={saving} />
        </Grid>
        <Grid item xs={12} md={6}>
          <AIChatPanel onFormExtracted={handleFormExtracted} currentInteractionId={currentInteractionId} />
        </Grid>
      </Grid>

      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({ ...toast, open: false })}>
        <Alert severity={toast.severity} onClose={() => setToast({ ...toast, open: false })}>
          {toast.message}
        </Alert>
      </Snackbar>
    </MainLayout>
  );
}
