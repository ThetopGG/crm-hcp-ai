import React, { useEffect, useState } from "react";
import {
  Grid,
  Typography,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
} from "@mui/material";
import GroupsIcon from "@mui/icons-material/GroupsOutlined";
import ForumIcon from "@mui/icons-material/ForumOutlined";
import EventAvailableIcon from "@mui/icons-material/EventAvailableOutlined";
import WarningAmberIcon from "@mui/icons-material/WarningAmberOutlined";
import MainLayout from "../components/Layout/MainLayout";
import StatCard from "../components/Dashboard/StatCard";
import api from "../api/axios";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const { data } = await api.get("/api/dashboard/stats");
        setStats(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  return (
    <MainLayout>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 0.5 }}>
        Dashboard
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Overview of your CRM activity and AI-driven insights.
      </Typography>

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 8 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <Grid container spacing={2.5}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard label="Total HCPs" value={stats?.total_hcps ?? 0} icon={<GroupsIcon />} color="primary.main" />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard label="Total Interactions" value={stats?.total_interactions ?? 0} icon={<ForumIcon />} color="secondary.main" />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard label="Pending Follow-ups" value={stats?.pending_follow_ups ?? 0} icon={<EventAvailableIcon />} color="#F5A623" />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard label="Overdue Follow-ups" value={stats?.overdue_follow_ups ?? 0} icon={<WarningAmberIcon />} color="#E5484D" />
            </Grid>
          </Grid>

          <Grid container spacing={2.5} sx={{ mt: 0.5 }}>
            <Grid item xs={12} md={7}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Recent Interactions
                </Typography>
                <List>
                  {(stats?.recent_interactions ?? []).length === 0 && (
                    <Typography variant="body2" color="text.secondary">
                      No interactions logged yet.
                    </Typography>
                  )}
                  {(stats?.recent_interactions ?? []).map((item) => (
                    <ListItem key={item.id} divider>
                      <ListItemText
                        primary={`${item.hcp?.name || "Unknown Doctor"} — ${item.interaction_type}`}
                        secondary={`${item.interaction_date} • ${item.outcome || "No outcome recorded"}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={5}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Top Products Discussed
                </Typography>
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                  {(stats?.top_products ?? []).length === 0 && (
                    <Typography variant="body2" color="text.secondary">
                      No product data yet.
                    </Typography>
                  )}
                  {(stats?.top_products ?? []).map((p) => (
                    <Chip key={p.product} label={`${p.product} (${p.count})`} color="primary" variant="outlined" />
                  ))}
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </>
      )}
    </MainLayout>
  );
}
